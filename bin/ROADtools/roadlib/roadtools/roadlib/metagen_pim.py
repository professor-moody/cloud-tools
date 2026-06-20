import xml.etree.ElementTree as ET
import sys
tree = ET.parse(sys.argv[1])
root = tree.getroot()

CLASS_PREFIX = 'PIM'

def trl_prop(prop):
    if 'Collection(' in prop:
        return 'Collection'
    prop = prop.replace('Microsoft.Identity.Governance.Common.Data.ExternalModels.V1.', CLASS_PREFIX)
    return prop

allprops = []

etout = []

ethdr = '''from roadtools.roadlib.metadef.basetypes import Edm, Collection
from roadtools.roadlib.metadef.complextypes_pim import *
'''
etout.append(ethdr)

ns = {'edm':'http://docs.oasis-open.org/odata/ns/edm'}
for entitytype in root.iter('{http://docs.oasis-open.org/odata/ns/edm}EntityType'): # root.findall('edm:EntityType', ns):
    etname = entitytype.get('Name')
    if not etname.startswith(CLASS_PREFIX):
        etname = CLASS_PREFIX + etname
    basetype = entitytype.get('BaseType')
    if basetype:
        basetype = basetype.replace('Microsoft.Identity.Governance.Common.Data.ExternalModels.V1.', CLASS_PREFIX)
    else:
        basetype = 'object'
    out = '''
class %s(%s):
    props = {
%s
    }
    rels = [
%s
    ]

'''
    props = []

    for prop in entitytype.iter('{http://docs.oasis-open.org/odata/ns/edm}Property'):
        props.append("        '%s': %s," % (prop.get('Name'), trl_prop(prop.get('Type'))))
        allprops.append(trl_prop(prop.get('Type')))

    rels = []
    for relout in entitytype.iter('{http://docs.oasis-open.org/odata/ns/edm}NavigationProperty'):
        rels.append("        '%s'," % (relout.get('Name')))

    etout.append(out % (etname, basetype, '\n'.join(props), '\n'.join(rels)))

# Simple classes, no references
ctsout = []
# Complex classes, possibly references
ctcout = []
# All classes, to resolve references
allclass = []
cthdr = '''from roadtools.roadlib.metadef.basetypes import Edm, Collection
import enum
'''
ctsout.append(cthdr)

# Enums

for entitytype in root.iter('{http://docs.oasis-open.org/odata/ns/edm}EnumType'): # root.findall('edm:EntityType', ns):
    ctname = CLASS_PREFIX + entitytype.get('Name')
    out = '''
{entname}_data = {{
{entdict}
}}
{entname} = enum.Enum('{entname}', {entname}_data)

'''
    values = []
    for prop in entitytype.iter('{http://docs.oasis-open.org/odata/ns/edm}Member'):
        # Possibly complex type, these should come last
        values.append("    '%s': %s," % (prop.get('Name'), trl_prop(prop.get('Value'))))

    # Do these first
    ctsout.append(out.format(entname=ctname, entdict='\n'.join(values)))
    allclass.append(ctname)


re_iter = []
for entitytype in root.iter('{http://docs.oasis-open.org/odata/ns/edm}ComplexType'): # root.findall('edm:EntityType', ns):
    ctname = entitytype.get('Name')
    if not ctname.startswith(CLASS_PREFIX):
        ctname = CLASS_PREFIX + ctname
    basetype = 'object'
    out = '''
class %s(%s):
    props = {
%s
    }

'''
    props = []
    hascomplex = False
    proptypes = []
    for prop in entitytype.iter('{http://docs.oasis-open.org/odata/ns/edm}Property'):
        # Possibly complex type, these should come last
        translated = trl_prop(prop.get('Type'))
        if not translated in allclass and not translated.startswith('Collection') and not 'Edm.' in translated:
            hascomplex = True
        props.append("        '%s': %s," % (prop.get('Name'), trl_prop(prop.get('Type'))))
        proptypes.append(translated)
        allprops.append(translated)

    if hascomplex:
        re_iter.append((ctname, basetype, props, proptypes))
    else:
        ctsout.append(out % (ctname, basetype, '\n'.join(props)))
        allclass.append(ctname)

# Try to filter out the ones resolved now
for i in range(10):
    for item in re_iter.copy():
        ctname, basetype, props, proptypes = item
        unref = False
        for translated in proptypes:
            if not translated in allclass and not translated.startswith('Collection') and not 'Edm.' in translated:
                unref = True
        if not unref:
            print('Resolved', ctname)
            ctsout.append(out % (ctname, basetype, '\n'.join(props)))
            allclass.append(ctname)
            re_iter.remove(item)

# Final chunks, init later because they self-reference or circle reference
out = '''
class %s(%s):
    props = {}
    def __init__(self):
        self.__class__.props = {
    %s
        }

'''
print(f"Unresolved left: {len(re_iter)}")
for item in re_iter:
    ctname, basetype, props, proptypes = item
    ctcout.append(out % (ctname, basetype, '\n    '.join(props)))

with open('metadef/entitytypes_pim.py', 'w') as fout:
    fout.write(''.join(etout))

with open('metadef/complextypes_pim.py', 'w') as fout:
    fout.write(''.join(ctsout))
    fout.write(''.join(ctcout))


# raprops = set(allprops)
# print raprops
