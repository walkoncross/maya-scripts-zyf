# coding=utf-8
# """
# Export .obj files for target shapes for a blendshape node in Maya.

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


def get_all_blendshape_nodes(show_type=True):
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


def get_blendshape_keys_list(blendshape_node_name):
    """
    Get name list (blendshape keys) of target-shapes/morphing-targets of blendshape.

    Args:
        blendshape_node_name: str 
            Name of blend shape deformer (blendShape Node) in Maya.

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

    # blendshape_keys_list.sort()

    return blendshape_keys_list


def get_blendshape_geometry_name(blendshape_node_name):
    """
    Get the geometry name binded with the specified blendshape.

    Args:
        blendshape_node_name: str 
            Name of blend shape deformer (blendShape Node) in Maya.

    Returns: 
        list of str
            Name list of geometry of the input blendshape node.

    """
    # Maya python cmd
    geometry_list = cmds.blendShape(
        blendshape_node_name, query=True, geometry=True)

    geometry_list.sort()

    return geometry_list


def export_keyframe_blendshape_weight_values(blendshape_node_name, save_dir='./',
                                     start_frame=1, end_frame=10):
    """
    Export keyframe meshes into .json files.

    Args:
        blendshape_node_name: str or list of str
            Name of blendshape node;
        save_dir: str
            Directory to save .json files for weight values of a blendshape node.

    Returns: 
        None.
    """
    pprint("===> blendshape_node_name: {}".format(blendshape_node_name))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()

    if isinstance(blendshape_node_name, str):
        blendshape_node_name = [blendshape_node_name]

    # Export keyframe blendshape weight values.
    for curr_time in range(start_frame, end_frame+1):
        pprint('===> Export at time: #{}'.format(curr_time))
        cmds.currentTime(curr_time)

        for node in blendshape_node_name:
            pprint('---> blendshape: {}'.format(node))
            save_filename = "{}/{}.keyframe.{}.frame_{}.json".format(save_dir, scene_name, node, curr_time)
            blendshape_keys_list = get_blendshape_keys_list(node)
            weight_values = cmds.getAttr(node+'.weight')[0]
            # pprint(len(blendshape_keys_list))
            # pprint(len(weight_values[0]))
            # pprint(type(weight_values))
            # pprint(weight_values)
            kv_dict = dict(zip(blendshape_keys_list, weight_values))
            fp = open(save_filename, 'w')
            json.dump(kv_dict, fp, indent=2)
            fp.close()


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/yuanli_bs_tang2'
    # blendshape_node_name = r'AI_TD_01_Head01_blendShape'
    blendshape_node_name = get_all_blendshape_nodes(False)

    export_keyframe_blendshape_weight_values(blendshape_node_name, save_dir, start_frame=1, end_frame=27)