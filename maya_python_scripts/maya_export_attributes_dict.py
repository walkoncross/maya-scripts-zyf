# coding=utf-8
# """
# Export attributes list of a node in Maya.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import json
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint


def get_current_scene_name():
    """
    Get current scene name.

    Args: 
        None.

    Returns: 
        str
            Scene name.
    """

    scene_name = cmds.file(query=True, sceneName=True, shortName=True)
    scene_name = osp.splitext(scene_name)[0]

    return scene_name


def get_attributes_list(node_name, attribute_name_pattern=None):
    """
    Get attributes list of a node.

    Args:
        node_name: str 
            Node Name in Maya.
        attribute_name_pattern: str
            List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

    Returns: 
        list of str
            Attribute name list of the input node.

    """

    # Maya Mel cmd
    # cmd = 'listAttr -k -m -st "weight" ' + node_name
    # attributes_list = mel.eval(cmd)

    # Maya python cmd
    if attribute_name_pattern is None:
        attributes_list = cmds.listAttr(node_name, multi=True, keyable=True)
    else:
        attributes_list = cmds.listAttr(
            node_name, st=attribute_name_pattern, multi=True, keyable=True)

    attributes_list.sort()

    return attributes_list


def export_attributes_list(node_name, save_dir='./', attribute_name_pattern=None):
    """
    Get and save attributes list of a node.

    Args:
        node_name: str
            Node Name in Maya.
        save_dir: str
            Directory to save attributes list.
        attribute_name_pattern: str
            List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

    Returns: 
        None.
    """

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    attributes_filename = osp.join(
        save_dir, '{}.{}.attributes_dict.json'.format(scene_name, node_name))

    attributes_list = get_attributes_list(node_name, attribute_name_pattern)
    attributes_dict = {}

    for idx, attribute in enumerate(attributes_list):
        # cmds.setAttr( node_name + '.' + attribute, 0)
        attribute_value = cmds.getAttr( node_name + '.' + attribute )
        attributes_dict[attribute] =  attribute_value
        pprint('---> {}: {} {}'.format(idx+1, attribute, attribute_value))

        # cmds.setAttr( node_name + '.' + attribute, 0)
        # attribute_value = cmds.getAttr( node_name + '.' + attribute )
        # attributes_dict[attribute] =  attribute_value
        # pprint('---> {}: {} {}'.format(idx+1, attribute, attribute_value))      

    pprint('\n===> {} attributes in total'.format(len(attributes_list)))

    pprint('\n===> save attributes values dict into file: ')
    pprint(attributes_filename)
    fp = open(attributes_filename, 'w')
    json.dump(attributes_dict, fp, indent=2)
    fp.close()


if __name__ == '__main__':
    node_name = r'Root_M'
    save_dir = r'D:/zhaoyafei/maya_exports'
    attribute_name_pattern = None

    export_attributes_list(node_name, save_dir, attribute_name_pattern)
