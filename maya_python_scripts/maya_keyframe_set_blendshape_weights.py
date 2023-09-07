# coding=utf-8
# """
# Set keyframe blendshape weights in Maya.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import json
import maya.cmds as cmds
import maya.mel as mel

from pprint import pprint


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


def set_blendshape_keyframe(mesh_node_name, blendshape_node_name,
                            frame_number, blendshape_values_dict, blendshape_keys_list=None):
    """
    Set blendshape keyframe at frame #frame_number.

    Args:
        mesh_node_name: str
            Name of mesh/shape in Maya;
        blendshape_node_name: str
            Name of blendshape deformer in Maya;
        frame_number: int
            Frame number (>0)
        blendshape_values_dict: dict
            Values for blendshape weights, a dict
        blendshape_keys_list: list of str or None
            List of blendshape keys (weight names);

    Returns: 
        None.
    """

    if blendshape_keys_list is None:
        blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=True)

    cmds.currentTime(frame_number)
    cmds.select(mesh_node_name, replace=True)

    # 0. Reset to Neutral pose.
    # for k in blendshape_keys_list:
    #     key_name = "{}.{}".format(blendshape_node_name, k)
    #     v = 0.
    #     cmds.setAttr(key_name, v)

    # 1. Set values for bs weights
    for k, v in blendshape_values_dict.iteritems():
        # if v < 0.01:
        #     v = 0
        if not k in blendshape_keys_list:
            continue

        key_name = "{}.{}".format(blendshape_node_name, k)
        try:
            cmds.setAttr(key_name, v)
        except:
            pprint('---> skip locked key: ' + key_name)

    # cmds.setKeyframe(mesh_node_name)
    cmds.setKeyframe(blendshape_node_name)


if __name__ == '__main__':
    mesh_node_name = r'nature'
    blendshape_node_name = r'blendShape1'
    save_dir = r'/Users/zhaoyafei/Downloads/3D_model_assets/zhizao'

    keyframe_json_filename = r'/Users/zhaoyafei/Downloads/3D_model_assets/zhizao/034_200271_20200923_control.json'

    fp = open(keyframe_json_filename, 'r')
    keyframe_values_list = json.load(fp)
    fp.close()

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=True)

    for idx, blendshape in enumerate(blendshape_keys_list):
        pprint('===> {}: {}'.format(idx+1, blendshape))

    blendshape_keys_filename = save_dir + '/00_bs_keys.txt'
    fp = open(blendshape_keys_filename, 'w')
    fp.write('\n'.join(blendshape_keys_list) + '\n')
    fp.close()

    for frame in keyframe_values_list:
        set_blendshape_keyframe(
            mesh_node_name,
            blendshape_node_name,
            frame['frame_id'],
            frame,
            blendshape_keys_list
        )
