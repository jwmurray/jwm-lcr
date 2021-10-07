#!/usr/bin/env python3

import json
from lcr import API as LCR

username = "gardenway"
password = "lancer83"
unit_number = 259950
lcr = LCR(username, password, unit_number)

# months = 5
# move_ins = lcr.members_moved_in(months)
ward = lcr.member_list()

# for member in move_ins:
#     print("{}: {}".format(member, member['textAddress']))


for member in ward:
    jsonstr1 = json.dumps(member, indent=4)
    print(jsonstr1 )
    print ("")
    if member['email'] == 'john@gardenway.org':
        print("stop")

