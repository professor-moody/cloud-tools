"""
WebAuthn client logic for FIDO authentication using Windows Hello RSA keys and passkeys
"""
import base64
import hashlib
import json
import struct
import uuid
import cbor2
import codecs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class WebAuthnClient:
    """
    WebAuthn client that uses RSA keys (Windows Hello format) for FIDO2 authentication
    Compatible with Microsoft Entra ID

    Supports both Windows Hello keys (calculated userHandle) and software passkeys (provided userHandle)
    """

    def __init__(self, deviceauth, hellokey=None, hellokeydata=None):
        """
        Initialize with a DeviceAuthentication instance that has a loaded hello key

        Args:
            deviceauth: DeviceAuthentication instance with loaded hellokey
        """
        self.deviceauth = deviceauth
        if hellokey:
            self.hellokey = hellokey
        else:
            self.hellokey = deviceauth.hellokey
        if hellokeydata:
            self.hellokeydata = hellokeydata
        else:
            self.hellokeydata = deviceauth.hellokeydata
        self._sign_count = 0  # Track signature count

    def get_credential_id(self):
        """
        Generate a credential ID based on the public key
        Uses SHA256 hash of the public key, similar to how ROADtools calculates kid

        Returns:
            str: Base64url-encoded credential ID (no padding)
        """
        key = self.hellokey
        pubkeycngblob = self.deviceauth.create_pubkey_blob_from_key(key)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(pubkeycngblob)
        kid = digest.finalize()
        return base64.urlsafe_b64encode(kid).decode('utf-8').rstrip('=')

    def generate_user_handle(self, tenant_id, user_id):
        """
        Generate Microsoft Entra ID userHandle for Windows Hello keys
        Format: "ON:" + tenantId (bytes_le) + SHA256(userId bytes_le)

        Args:
            tenant_id: Azure AD tenant ID (GUID string)
            user_id: Azure AD user objectId (GUID string)

        Returns:
            str: Base64url-encoded userHandle (no padding)
        """
        # Start with "ON:" prefix (3 bytes)
        handle_bytes = bytearray(b"ON:")

        # Add tenantId as Little-Endian GUID bytes (16 bytes)
        if isinstance(tenant_id, str):
            tenant_guid = uuid.UUID(tenant_id)
            tenant_bytes_le = tenant_guid.bytes_le
        else:
            tenant_bytes_le = tenant_id

        handle_bytes.extend(tenant_bytes_le)

        # Add SHA256 hash of the USER ID bytes (32 bytes)
        if isinstance(user_id, str):
            user_guid = uuid.UUID(user_id)
            user_bytes_le = user_guid.bytes_le
        else:
            user_bytes_le = user_id

        user_hash = hashlib.sha256(user_bytes_le).digest()
        handle_bytes.extend(user_hash)

        # Encode as base64url without padding
        return base64.urlsafe_b64encode(bytes(handle_bytes)).decode('utf-8').rstrip('=')

    def create_authenticator_data(self, rp_id, flags=0x05, sign_count=None):
        """
        Create authenticator data structure for assertion

        Args:
            rp_id: Relying party ID (e.g., "login.microsoft.com")
            flags: Authenticator data flags (default 0x05 = UP + UV)
                   - 0x01: User Present (UP)
                   - 0x04: User Verified (UV)
            sign_count: Signature counter (auto-increments if None)

        Returns:
            bytes: Authenticator data (37 bytes for assertion)
        """
        # RP ID hash (32 bytes)
        rp_id_hash = hashlib.sha256(rp_id.encode('utf-8')).digest()

        # Auto-increment sign count if not provided
        if sign_count is None:
            sign_count = self._sign_count
            self._sign_count += 1

        # Build authenticator data: rpIdHash || flags || signCount
        auth_data = bytearray()
        auth_data.extend(rp_id_hash)           # 32 bytes
        auth_data.append(flags)                 # 1 byte
        auth_data.extend(struct.pack('>I', sign_count))  # 4 bytes, big-endian

        return bytes(auth_data)

    def create_client_data_json(self, challenge, origin, type_="webauthn.get"):
        """
        Create client data JSON matching Microsoft's format

        Args:
            challenge: Challenge from server (will be base64url encoded if needed)
            origin: Origin of the RP (e.g., "https://login.microsoft.com")
            type_: Operation type ("webauthn.get" for assertion)

        Returns:
            tuple: (client_data_json_bytes, client_data_hash)
        """

        # Ensure challenge is a string (base64url encode if bytes)
        if type_ == "webauthn.get":
            if not isinstance(challenge, bytes):
                challenge = challenge.encode('utf-8')
            challenge_str = base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
        else:
            # Ensure challenge is base64url string
            if isinstance(challenge, bytes):
                challenge_str = base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
            else:
                challenge_str = challenge
        # Create client data JSON (exact format Microsoft expects)
        client_data = {
            "type": type_,
            "challenge": challenge_str,
            "origin": origin,
            "crossOrigin": False  # Microsoft includes this
        }

        # Encode to JSON bytes (no extra whitespace)
        client_data_json = json.dumps(client_data, separators=(',', ':')).encode('utf-8')

        # Calculate SHA256 hash
        digest = hashes.Hash(hashes.SHA256())
        digest.update(client_data_json)
        client_data_hash = digest.finalize()

        return client_data_json, client_data_hash

    def sign_assertion(self, client_data_hash, authenticator_data):
        """
        Sign the assertion using the RSA private key (RS256 algorithm)

        Args:
            client_data_hash: SHA256 hash of client data JSON (32 bytes)
            authenticator_data: Authenticator data bytes

        Returns:
            bytes: Signature
        """
        # WebAuthn signature is over: authenticatorData || hash(clientDataJSON)
        to_sign = authenticator_data + client_data_hash

        # Sign with RSA-PKCS1-v1_5 with SHA256 (RS256)
        signature = self.hellokey.sign(
            to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return signature

    def get_assertion(self, challenge,
                      rp_id="login.microsoft.com",
                      origin="https://login.microsoft.com",
                      user_handle=None,
                      tenant_id=None,
                      user_id=None,
                      user_present=True,
                      user_verified=True):
        """
        Create a WebAuthn assertion response matching Microsoft's exact format

        Args:
            challenge: Challenge from Entra ID (base64url string or bytes)
            rp_id: Relying party ID (default: "login.microsoft.com")
            origin: Origin URL (default: "https://login.microsoft.com")
            user_handle: Pre-calculated userHandle (for software passkeys) - optional
            tenant_id: Azure AD tenant ID (GUID string) - required if user_handle not provided
            user_id: Azure AD user objectId (GUID string) - required if user_handle not provided
            user_present: User presence flag
            user_verified: User verification flag

        Returns:
            dict: WebAuthn assertion response in Microsoft's format
        """
        # Determine userHandle: either provided or calculated from tenant_id + user_id
        if user_handle is None:
            if tenant_id is None or user_id is None:
                raise ValueError("Either user_handle must be provided, or both tenant_id and user_id")
            user_handle = self.generate_user_handle(tenant_id, user_id)

        # Create client data JSON and hash
        client_data_json, client_data_hash = self.create_client_data_json(
            challenge, origin, "webauthn.get"
        )

        # Create flags
        flags = 0x00
        if user_present:
            flags |= 0x01  # UP
        if user_verified:
            flags |= 0x04  # UV

        # Create authenticator data
        authenticator_data = self.create_authenticator_data(rp_id, flags)

        # Sign the assertion
        signature = self.sign_assertion(client_data_hash, authenticator_data)

        # Get credential ID
        credential_id = self.get_credential_id()

        # Return assertion in Microsoft's exact format (flat structure)
        assertion = {
            "id": credential_id,
            "clientDataJSON": base64.urlsafe_b64encode(client_data_json).decode('utf-8').rstrip('='),
            "authenticatorData": base64.urlsafe_b64encode(authenticator_data).decode('utf-8').rstrip('='),
            "signature": base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('='),
            "userHandle": user_handle
        }

        return assertion

    def create_attestation_object(self, rp_id_hash, flags, sign_count, attested_credential_data, client_data_hash):
        """
        Create attestation object for credential registration

        Args:
            rp_id_hash: SHA256 hash of RP ID (32 bytes)
            flags: Authenticator flags
            sign_count: Signature counter
            attested_credential_data: Attested credential data bytes
            client_data_hash: SHA256 hash of client data JSON

        Returns:
            bytes: CBOR-encoded attestation object
        """

        # Create authenticator data
        auth_data = bytearray()
        auth_data.extend(rp_id_hash)
        auth_data.append(flags)
        auth_data.extend(struct.pack('>I', sign_count))
        auth_data.extend(attested_credential_data)

        auth_data_bytes = bytes(auth_data)

        # Create signature over authenticatorData || clientDataHash
        to_sign = auth_data_bytes + client_data_hash
        signature = self.hellokey.sign(
            to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # Create attestation object (packed format, self-attestation)
        attestation_object = {
            "fmt": "none",
            "authData": auth_data_bytes,
            "attStmt": {
                # "alg": -257,  # RS256
                # "sig": signature
            }
        }

        return cbor2.dumps(attestation_object)

    def create_attested_credential_data(self, aaguid, credential_id_bytes, public_key_cose):
        """
        Create attested credential data for registration

        Args:
            aaguid: 16-byte AAGUID (authenticator identifier)
            credential_id_bytes: Raw credential ID bytes
            public_key_cose: COSE-encoded public key

        Returns:
            bytes: Attested credential data
        """
        data = bytearray()
        data.extend(aaguid)
        data.extend(struct.pack('>H', len(credential_id_bytes)))
        data.extend(credential_id_bytes)
        data.extend(public_key_cose)

        return bytes(data)

    def encode_public_key_cose(self):
        """
        Encode RSA public key in COSE format for attestation

        Returns:
            bytes: CBOR-encoded COSE key
        """

        pubkey = self.hellokey.public_key()
        pubnumbers = pubkey.public_numbers()

        # Convert to bytes
        n_bytes = pubnumbers.n.to_bytes(
            (pubnumbers.n.bit_length() + 7) // 8,
            byteorder='big'
        )
        e_bytes = pubnumbers.e.to_bytes(
            (pubnumbers.e.bit_length() + 7) // 8,
            byteorder='big'
        )

        # COSE key for RSA (alg -257)
        cose_key = {
            1: 3,        # kty: RSA
            3: -257,     # alg: RS256
            -1: n_bytes, # n: modulus
            -2: e_bytes  # e: exponent
        }

        return cbor2.dumps(cose_key)

    def make_credential(self, challenge, rp_id, rp_name, user_id, user_name,
                       user_display_name, origin="https://login.microsoft.com",
                       aaguid=None):
        """
        Create a credential registration response (attestation)

        Args:
            challenge: Challenge from Entra ID (base64url string or bytes)
            rp_id: Relying party ID (e.g., "login.microsoft.com")
            rp_name: Relying party name (e.g., "Microsoft")
            user_id: User ID bytes or base64url string (from registration request)
            user_name: Username string
            user_display_name: User display name
            origin: Origin URL
            aaguid: 16-byte AAGUID (defaults to zeros for software authenticator)

        Returns:
            dict: Credential registration response for Entra ID
        """
        if aaguid is None:
            aaguid = b'\x00' * 16

        # Ensure challenge is base64url string
        if isinstance(challenge, bytes):
            challenge_str = base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
        else:
            challenge_str = challenge

        # Create client data JSON
        client_data_json, client_data_hash = self.create_client_data_json(
            challenge_str, origin, "webauthn.create"
        )

        # Get credential ID
        credential_id_str = self.get_credential_id()
        credential_id_bytes = base64.urlsafe_b64decode(credential_id_str + '==')

        # Create COSE-encoded public key
        public_key_cose = self.encode_public_key_cose()

        # Create attested credential data
        attested_cred_data = self.create_attested_credential_data(
            aaguid, credential_id_bytes, public_key_cose
        )

        # Create RP ID hash
        rp_id_hash = hashlib.sha256(rp_id.encode('utf-8')).digest()

        # Flags: UP (0x01) | UV (0x04) | AT (0x40) = 0x45
        flags = 0x01 | 0x04 | 0x40

        # Create attestation object
        attestation_object = self.create_attestation_object(
            rp_id_hash, flags, 0, attested_cred_data, client_data_hash
        )

        # Return in Microsoft Graph API format
        return {
            "id": credential_id_str,
            # "rawId": credential_id_str,
            "response": {
                "clientDataJSON": base64.urlsafe_b64encode(client_data_json).decode('utf-8').rstrip('='),
                "attestationObject": base64.urlsafe_b64encode(attestation_object).decode('utf-8').rstrip('=')
            },
            # "type": "public-key"
        }

    @staticmethod
    def create_software_passkey(passkey_file, rp_id="login.microsoft.com",
                                tenant_id=None, user_id=None, user_handle=None,
                                user_name=None, user_display_name=None):
        """
        Generate a new software passkey and save it to a .rtpk file

        Args:
            passkey_file: Path to save the .rtpk file (should end in .rtpk)
            rp_id: Relying party ID
            tenant_id: Azure AD tenant ID (for Windows Hello-style userHandle)
            user_id: Azure AD user objectId (for Windows Hello-style userHandle)
            user_handle: Pre-calculated userHandle (alternative to tenant_id/user_id)
            user_name: Username
            user_display_name: User display name

        Returns:
            tuple: (private_key, credential_id, user_handle)
        """

        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Calculate credential ID (SHA256 of public key)
        pubkey = private_key.public_key()
        pubkey_der = pubkey.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        digest = hashes.Hash(hashes.SHA256())
        digest.update(pubkey_der)
        cred_id_bytes = digest.finalize()
        credential_id = base64.urlsafe_b64encode(cred_id_bytes).decode('utf-8').rstrip('=')

        # Generate or use provided userHandle
        if user_handle is None:
            if tenant_id and user_id:
                # Generate Windows Hello-style userHandle
                handle_bytes = bytearray(b"ON:")
                tenant_guid = uuid.UUID(tenant_id)
                handle_bytes.extend(tenant_guid.bytes_le)
                user_guid = uuid.UUID(user_id)
                user_hash = hashlib.sha256(user_guid.bytes_le).digest()
                handle_bytes.extend(user_hash)
                user_handle = base64.urlsafe_b64encode(bytes(handle_bytes)).decode('utf-8').rstrip('=')
            else:
                raise ValueError("Either user_handle or both tenant_id and user_id must be provided")

        # Encode private key to PEM
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode('utf-8')

        # Create passkey metadata
        passkey_data = {
            "version": 1,
            "type": "software-passkey",
            "rp_id": rp_id,
            "credential_id": credential_id,
            "user_handle": user_handle,
            "private_key": private_key_pem,
            "algorithm": "RS256",
            "created": None,  # Will be set on first use/registration
        }

        # Add optional metadata
        if tenant_id:
            passkey_data["tenant_id"] = tenant_id
        if user_id:
            passkey_data["user_id"] = user_id
        if user_name:
            passkey_data["user_name"] = user_name
        if user_display_name:
            passkey_data["user_display_name"] = user_display_name

        # Save to .rtpk file
        if not passkey_file.endswith('.rtpk'):
            passkey_file += '.rtpk'

        with codecs.open(passkey_file, 'w', 'utf-8') as f:
            json.dump(passkey_data, f, indent=2)

        print(f"Created software passkey: {passkey_file}")
        print(f"Credential ID: {credential_id}")
        print(f"User handle: {user_handle}")

        return private_key, passkey_data

    @staticmethod
    def load_software_passkey(passkey_file):
        """
        Load a software passkey from a .rtpk file

        Args:
            passkey_file: Path to the .rtpk file

        Returns:
            dict: Passkey metadata including private_key object
        """

        with codecs.open(passkey_file, 'r', 'utf-8') as f:
            passkey_data = json.load(f)

        # Load private key from PEM
        private_key_pem = passkey_data['private_key'].encode('utf-8')
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None
        )

        passkey_data['private_key_object'] = private_key

        return passkey_data

    @staticmethod
    def from_software_passkey(deviceauth, passkey_file):
        """
        Create a WebAuthnClient instance from a software passkey file

        Args:
            passkey_file: Path to the .rtpk file

        Returns:
            tuple: (WebAuthnClient instance, passkey_metadata dict)
        """
        # Load passkey
        passkey_data = WebAuthnClient.load_software_passkey(passkey_file)

        # Create WebAuthnClient
        client = WebAuthnClient(deviceauth, passkey_data['private_key_object'], passkey_data['private_key'].encode('utf-8'))

        return client, passkey_data

    @staticmethod
    def from_passkey_dict(deviceauth, passkey_data):
        """
        Create a WebAuthnClient instance from a software passkey file

        Args:
            passkey_file: Path to the .rtpk file

        Returns:
            tuple: (WebAuthnClient instance, passkey_metadata dict)
        """
        # Load private key from PEM
        private_key_pem = passkey_data['private_key'].encode('utf-8')
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None
        )

        passkey_data['private_key_object'] = private_key

        # Create WebAuthnClient
        client = WebAuthnClient(deviceauth, passkey_data['private_key_object'], passkey_data['private_key'].encode('utf-8'))

        return client, passkey_data

class EntraIDFIDOAuthenticator:
    """
    Helper class for Entra ID / Azure AD specific FIDO authentication flow
    Integrates with ROADtools Authentication and DeviceAuthentication classes

    Supports both Windows Hello keys and software passkeys
    """

    def __init__(self, deviceauth=None, webauthn_client=None, tenant_id=None, user_id=None, user_handle=None):
        """
        Initialize with ROADtools components

        Args:
            deviceauth: DeviceAuthentication instance with loaded hellokey
            webauthn_client: WebAuthnClient instance
            tenant_id: Azure AD tenant ID (GUID string) - required for Windows Hello keys
            user_id: Azure AD user objectId (GUID string) - required for Windows Hello keys
            user_handle: Pre-calculated userHandle (for software passkeys) - optional

        Note: Either provide (tenant_id + user_id) OR user_handle
        """
        if webauthn_client:
            self.webauthn_client = webauthn_client
        elif deviceauth:
            self.webauthn_client = WebAuthnClient(deviceauth)
        else:
            raise ValueError("Either a webauthn_client or a deviceauth instance must be specified")
        self.deviceauth = deviceauth
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.user_handle = user_handle

        # Validate configuration
        if user_handle is None and (tenant_id is None or user_id is None):
            raise ValueError("Either user_handle must be provided, or both tenant_id and user_id")

    def authenticate_with_fido(self, challenge, rp_id="login.microsoft.com",
                               origin="https://login.microsoft.com"):
        """
        Perform FIDO authentication with Entra ID

        Args:
            challenge: Challenge from Entra ID (base64url string or raw bytes)
            rp_id: Relying party ID
            origin: Origin URL

        Returns:
            dict: WebAuthn assertion response ready to send to Entra ID
        """
        assertion = self.webauthn_client.get_assertion(
            challenge=challenge,
            rp_id=rp_id,
            origin=origin,
            user_handle=self.user_handle,
            tenant_id=self.tenant_id,
            user_id=self.user_id,
            user_present=True,
            user_verified=True
        )

        return assertion

    def parse_entra_challenge(self, challenge_response):
        """
        Parse FIDO challenge from Entra ID response

        Args:
            challenge_response: Response from Entra ID containing FIDO challenge
                Can be a dict with 'challenge' key or a raw challenge string

        Returns:
            dict: Parsed challenge data with 'challenge', 'rp_id', etc.
        """
        if isinstance(challenge_response, dict):
            # Challenge is in a dict
            return {
                'challenge': challenge_response.get('challenge') or challenge_response.get('Challenge'),
                'rp_id': challenge_response.get('rpId', 'login.microsoft.com'),
            }
        else:
            # Challenge is a raw string
            return {
                'challenge': challenge_response,
                'rp_id': 'login.microsoft.com',
            }

    def register_credential(self, challenge, user_id_b64, user_name, user_display_name,
                           rp_id="login.microsoft.com", rp_name="Microsoft",
                           origin="https://login.microsoft.com", aaguid=None):
        """
        Register a new FIDO credential with Entra ID

        Args:
            challenge: Challenge from Entra ID registration request
            user_id_b64: User ID from registration request (base64url encoded)
            user_name: Username
            user_display_name: User display name
            rp_id: Relying party ID
            rp_name: Relying party name
            origin: Origin URL

        Returns:
            dict: Credential registration response ready for Microsoft Graph API
        """
        return self.webauthn_client.make_credential(
            challenge=challenge,
            rp_id=rp_id,
            rp_name=rp_name,
            user_id=user_id_b64,
            user_name=user_name,
            user_display_name=user_display_name,
            origin=origin,
            aaguid=uuid.UUID(aaguid).bytes
        )
