from json import JSONEncoder

import itglue
import json
import re


class Auth:
    itglue.connection.api_url = 'https://api.itglue.com'
    itglue.connection.api_key = 'Token'


class MyEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


assets = itglue.FlexibleAsset.filter(flexible_asset_type_id=XXX, size=1000, number=1)
transform = MyEncoder().encode(assets)
assets_json = json.loads(transform)

result = []
for line in assets_json:
    name = line.get('attributes').get('organization_name')
    link = line.get('attributes').get('traits').get('mac-mdm-enrollment-link')
    man = line.get('attributes').get('traits').get('applications-to-manually-install')
    auto = line.get('attributes').get('traits').get('applications-installed-via-mdm')
    reggie = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    if man:
        man = re.sub(reggie, '', man.replace('><', '>, <'))
    if auto:
        auto = re.sub(reggie, '', auto.replace('><', '>, <'))

    my_dict = {'organization_name': name,
               'mac-mdm-enrollment-link': link,
               'applications-to-manually-install': man,
               'applications-installed-via-mdm': auto}
    # print(my_dict)
    result.append(my_dict)

back_json = json.dumps(result)
f = open('gloo.json', 'w')
f.write(back_json)
f.close()
