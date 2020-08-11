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
from collections import OrderedDict

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


def get_all_joint_nodes(show_type=True):
    """
    Get name list of all joint nodes.

    Args:
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all joint nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    # joint_nodes_list = cmds.lsType("joint")
    joint_nodes_list = cmds.ls(type="joint", showType=show_type)

    # if not show_type:
    #     joint_nodes_list.sort()

    return joint_nodes_list


def get_all_joint_nodes_under_root_joint(root_joint_node_name, show_type=True):
    """
    Get name list of all joint nodes.

    Args:
        root_joint_node_name: str
            Name of the root joint node.
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all joint nodes under the root_joint_node.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    # joint_nodes_list = cmds.lsType("joint")
    joint_nodes_list = cmds.ls(root_joint_node_name, dag=True, type="joint", showType=show_type)

    # if not show_type:
    #     joint_nodes_list.sort()

    return joint_nodes_list


def export_keyframe_joint_values(root_joint_node_name, save_dir='./',
                                     start_frame=1, end_frame=10):
    """
    Export keyframe meshes into .json files.

    Args:
        root_joint_node_name: str or list of str
            Name of blendshape node;
        save_dir: str
            Directory to save .json files for weight values of a blendshape node.

    Returns: 
        None.
    """
    pprint("===> root_joint_node_name: {}".format(root_joint_node_name))
    
    joint_nodes_list = []
    if root_joint_node_name=='all' or not root_joint_node_name:
        joint_nodes_list = get_all_joint_nodes(False)
        # joint_nodes_list.sort()
    else:
        joint_nodes_list = get_all_joint_nodes_under_root_joint(root_joint_node_name, False)
    
    pprint('===> {} joints in total'.format(len(joint_nodes_list)))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()

    # Export keyframe blendshape weight values.
    for curr_time in range(start_frame, end_frame+1):
        pprint('===> Export at time: #{}'.format(curr_time))
        cmds.currentTime(curr_time)

        save_filename = "{}/{}.keyframe.{}.frame_{}.json".format(save_dir, scene_name, 'joints', curr_time)
        
        joints_values_dict = OrderedDict()

        for joint_node in joint_nodes_list:
            pprint('---> joint_node: {}'.format(joint_node))

            position = cmds.joint(joint_node, q=True, position=True)
            scale = cmds.joint(joint_node, q=True, scale=True)
            orientation = cmds.joint(joint_node, q=True, orientation=True)
            angle_x, angle_y, angle_z = cmds.joint(joint_node, q=True, ax=True, ay=True, az=True)
            
            degreeOfFreedom = cmds.joint(joint_node, q=True, degreeOfFreedom=True)
            scaleCompensate = cmds.joint(joint_node, q=True, scaleCompensate=True)
            rotationOrder = cmds.joint(joint_node, q=True, rotationOrder=True)
            scaleOrientation = cmds.joint(joint_node, q=True, scaleOrientation=True)

            joints_values_dict[joint_node] = {
                "position": position,
                "scale": scale,
                "orientation": orientation,
                "angleX": angle_x,
                "angleY": angle_y,
                "angleZ": angle_z,
                "degreeOfFreedom": degreeOfFreedom,
                "scaleCompensate": scaleCompensate,
                "rotationOrder": rotationOrder,
                "scaleOrientation": scaleOrientation
            }

        fp = open(save_filename, 'w')
        json.dump(joints_values_dict, fp, indent=2)
        fp.close()


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/maya_exports'
    # root_joint_node_name = 'all'
    root_joint_node_name = 'Hips'

    export_keyframe_joint_values(root_joint_node_name, save_dir, start_frame=1, end_frame=5)
