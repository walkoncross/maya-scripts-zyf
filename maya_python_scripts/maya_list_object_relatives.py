# coding=utf-8
# """
# Maya python scripts.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
from __future__ import print_function
from maya import cmds

selection = cmds.ls(selection=True)
print('===> selection: ', selection)

if len(selection) == 0:
  selection = cmds.ls(dag=True, long=True)

selection.sort(key=len, reverse=True)
print('===> selection: ', selection)

for obj in selection:
  shortName = obj.split("|")[-1]
  # Lets create a new variable to store the relatives:
  # We want to list the relatives, we only want the children, and we want the full path
  children = cmds.listRelatives(obj, children=True, fullPath=True)
  # Lets print the new variable on each iteration through the loop
  print("---> children", children)