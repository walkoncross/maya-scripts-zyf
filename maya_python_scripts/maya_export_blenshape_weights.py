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


def export_blendshape_weights(blendshape_node_name, save_dir='./'):
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
        save_dir, '{}.blendshape_weights.{}.json'.format(scene_name, blendshape_node_name))

    blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=False)

    bs_weights_list = cmds.getAttr(blendshape_node_name + '.weight')[0] # getAttr returns: [tuple(weights),]
    bs_weights_dict = dict(zip(blendshape_keys_list, bs_weights_list))

    for idx, blendshape in enumerate(blendshape_keys_list):
        pprint('---> {}: {} {}'.format(idx+1, blendshape, bs_weights_list[idx]))

    pprint('\n===> {} blendshape keys in total'.format(len(blendshape_keys_list)))

    pprint('\n===> save blendshape weights into file: ')
    pprint(blendshape_keys_filename)
    fp = open(blendshape_keys_filename, 'w')
    json.dump(bs_weights_dict, fp, indent=2, sort_keys=True)
    fp.close()


if __name__ == '__main__':
    blendshape_node_name = r'head_lod0_mesh_blendShape'
    save_dir = r'D:/zhaoyafei/maya_exports'

    export_blendshape_weights(blendshape_node_name, save_dir)
