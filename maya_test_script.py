import maya.cmds as cmds
from pprint import pprint

# list_ = cmds.ls(tr=True)
list_ = cmds.allNodeTypes()

for item in list_:
    if 'exp' in item:
        print item
# pprint(list_)