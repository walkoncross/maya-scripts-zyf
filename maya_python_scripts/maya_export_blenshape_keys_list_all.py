# coding=utf-8
# """
# Export name list (or blendshape keys) for target shapes of a blendshape node in Maya.

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

def get_all_blendshape_nodes(show_type=False):
    """
    Get name list of all blendshape nodes.

    Args:
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all blendshape nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    # blendshape_nodes_list = cmds.lsType("blendShape")
    blendshape_nodes_list = cmds.ls(type="blendShape", showType=show_type)

    if not show_type:
        blendshape_nodes_list.sort()

    return blendshape_nodes_list


def get_blendshape_keys_list(blendshape_node_name, sort_keys=False):
    """
    Get name list (blendshape keys) of target-shapes/morphing-targets of blendshape.

    Args:
        blendshape_node_name: str 
            Name of blend shape deformer (blendShape Node) in Maya.
        sort_keys: bool
            Whether to sort the keys by name.

    Returns: 
        list of str
            Name list of target shapes of the input blendshape node.

    """

    # Maya Mel cmd
    # cmd = 'listAttr -k -m -st "weight" ' + blendshape_node_name
    # blendshape_keys_list = mel.eval(cmd)

    # Maya python cmd
    blendshape_keys_list = cmds.listAttr(
        blendshape_node_name, st='weight', multi=True, keyable=True)

    if sort_keys:
        blendshape_keys_list.sort()

    return blendshape_keys_list


def export_blendshape_keys(blendshape_node_name, save_dir='./'):
    """
    Get and save name list of blendshape keys (name of target-shapes/morphing-targets).

    Args:
        blendshape_node_name: str
            Name of blend shape deformer (blendShape Node) in Maya.
        save_dir: str
            Directory to save blendshape keys list.

    Returns: 
        None.
    """

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    blendshape_keys_filename = osp.join(
        save_dir, '{}.blendshape.{}.txt'.format(scene_name, blendshape_node_name))

    blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=True)

    for idx, blendshape in enumerate(blendshape_keys_list):
        pprint('---> {}: {}'.format(idx+1, blendshape))

    pprint('\n===> {} blendshape keys in total'.format(len(blendshape_keys_list)))

    pprint('\n===> save blendshape keys into file: ')
    pprint(blendshape_keys_filename)
    fp = open(blendshape_keys_filename, 'w')
    fp.write('\n'.join(blendshape_keys_list) + '\n')
    fp.close()


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/maya_exports'

    blendshape_node_list = get_all_blendshape_nodes()
    for node in blendshape_node_list:
        export_blendshape_keys(node, save_dir)
