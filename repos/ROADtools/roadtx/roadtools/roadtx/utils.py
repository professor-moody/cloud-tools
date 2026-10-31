import os
import codecs
import json
import re
import base64, binascii, argparse, textwrap, uuid
from urllib.parse import urlparse

def find_redirurl_for_client(client, interactive=True, broker=False):
    '''
    Get valid redirect URLs for specified client. Interactive means a https URL is preferred.
    In practice roadtx often prefers non-interactive URLs even with interactive flows since it rewrites
    the URLs on the fly anyway
    '''
    current_dir = os.path.abspath(os.path.dirname(__file__))
    datafile = os.path.join(current_dir, 'firstpartyscopes.json')
    with codecs.open(datafile,'r','utf-8') as infile:
        data = json.load(infile)
    try:
        app = data['apps'][client.lower()]
    except KeyError:
        return 'https://login.microsoftonline.com/common/oauth2/nativeclient'
    if broker:
        brokerurl = f'ms-appx-web://Microsoft.AAD.BrokerPlugin/{client.lower()}'
        if brokerurl in app['redirect_uris']:
            return brokerurl
        return app['preferred_noninteractive_redirurl']
    if interactive and app['preferred_interactive_redirurl'] is not None:
        return app['preferred_interactive_redirurl']
    if app['preferred_noninteractive_redirurl']:
        return app['preferred_noninteractive_redirurl']
    # Return default URL even if it might not work since some follow up functions break when called with a None value
    return 'https://login.microsoftonline.com/common/oauth2/nativeclient'

def autobroker(args, auth, tokenobject=None):
    # Automatic broker app selection

    # Load scope data - contains redirect URLs for the broker
    current_dir = os.path.abspath(os.path.dirname(__file__))
    datafile = os.path.join(current_dir, 'firstpartyscopes.json')
    with codecs.open(datafile,'r','utf-8') as infile:
        data = json.load(infile)
    if not args.client:
        print('Client ID is required for autobroker flag, please specify with -c')
        return False
    if hasattr(args, 'broker_client') and args.broker_client:
        originclient = auth.lookup_client_id(args.broker_client)
    elif tokenobject and '_clientId' in tokenobject:
        originclient = auth.lookup_client_id(tokenobject['_clientId'])
    else:
        if tokenobject:
            # don't print this if we are in the interactiveauth flow
            print('Could not determine client, guessing the client based on redirect URL found')
        originclient = 'guess'
    try:
        targetclient = data['apps'][auth.lookup_client_id(args.client)]
    except KeyError:
        print(f'Unknown client with ID {args.client} is not found in roadtx built-in client list. Please specify broker parameters manually.')
        return False
    validru = False
    for redirect_url in targetclient['redirect_uris']:
        if originclient == 'guess' and redirect_url.startswith('brk-'):
            validru = True
            finalru = redirect_url
            break
        if redirect_url.startswith(f'brk-{originclient}'):
            validru = True
            finalru = redirect_url
            break
    if not validru:
        print(f'Could not find a valid broker redirect URL on this client matching the original client ID {originclient}')
        return False
    parsed = urlparse(finalru)
    if originclient == 'guess':
        # We know the client ID now
        originclient = parsed.scheme.lower()[4:]
    # Copy correct origin
    auth.set_origin_value(f'https://{parsed.hostname}')
    args.broker_redirect_url = finalru
    args.broker_client = originclient
    return originclient, finalru

# Refresh token analysis by @blurbdust
def guid_to_string(binary_guid):
    return str(uuid.UUID(bytes_le=binary_guid)).lower()

def b64_d(string):
    return base64.b64decode(string + '=' * (-len(string) % 4))
def b64_url_d(string):
    return base64.urlsafe_b64decode(string + '=' * (-len(string) % 4))

def sanitize_name(inname):
    return re.sub('[^A-Za-z0-9]+', '_', inname)

def parse_encrypted_token(rhdata):
    refresh = rhdata.split(".")
    rh = refresh[1]
    print("Parsing encrypted token header")
    print(f"Version: {refresh[0]}")
    print(f"Preamble: {binascii.hexlify(b64_url_d(rh)[:3])}")
    tenant = b64_url_d(rh)[3:3+16]
    tenant = guid_to_string(tenant)
    print(f"Tenant ID: {tenant}")
    app = b64_url_d(rh)[3+16:3+16+16]
    app = guid_to_string(app)
    print(f"App ID: {app}")
    print(f"Postamble: {binascii.hexlify(b64_url_d(rh)[-5:])}")
    if len(refresh) > 2 and refresh[2] != '':
        print("Parsing encrypted token")
        a = b64_url_d(refresh[2])[:16]
        b = b64_url_d(refresh[2])[16:32]
        print(f"Possible type ID\n03=refresh_token, 04=auth_code {guid_to_string(a)}")
        print(f"Unknown data {guid_to_string(b)}")
        print("Dumping encrypted part")
        print(Hexdump(b64_url_d(refresh[2])[32:]))

class Hexdump(object):
    def __init__(self, buf, off=0):
        self.buf = buf
        self.off = off

    def __iter__(self):
        last_bs, last_line = None, None
        for i in range(0, len(self.buf), 16):
            bs = bytearray(self.buf[i : i + 16])
            line = "{:08x}  {:23}  {:23}  |{:16}|".format(
                self.off + i,
                " ".join(("{:02x}".format(x) for x in bs[:8])),
                " ".join(("{:02x}".format(x) for x in bs[8:])),
                "".join((chr(x) if 32 <= x < 127 else "." for x in bs)),
            )
            if bs == last_bs:
                line = "*"
            if bs != last_bs or line != last_line:
                yield line
            last_bs, last_line = bs, line
        yield "{:08x}".format(self.off + len(self.buf))

    def __str__(self):
        return "\n".join(self)

    def __repr__(self):
        return "\n".join(self)
