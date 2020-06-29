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


def get_node_types():
    """
    Get list of all registered node types. 

    Args: 
        None.

    Returns: 
        list of str
            Name list of all registered node types.

    """

    node_types_list = cmds.ls(nodeTypes=True)
    node_types_list.sort()

    return node_types_list


def get_all_nodes_list(show_type=True):
    """
    Get name list of all available nodes in current scene/projects. 

    Args:
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all available nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    nodes_list = cmds.ls(showType=show_type)

    if not show_type:
        nodes_list.sort()

    return nodes_list


def get_all_mesh_nodes(show_type=True):
    """
    Get name list of all mesh nodes.

    Args:
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all meshes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    # mesh_nodes_list = cmds.lsType("mesh")
    mesh_nodes_list = cmds.ls(type="mesh", showType=show_type)

    if not show_type:
        mesh_nodes_list.sort()

    return mesh_nodes_list


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

    if not show_type:
        joint_nodes_list.sort()

    return joint_nodes_list


def get_all_shape_nodes(show_type=True):
    """
    Get name list of all shape nodes. 
    (Shapes in Maya are selectable DAG objects that display in 3D views. 
    Meshes, NURBS surfaces and curves, and locators are just some examples of shapes.)

    Args:
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all shape nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    shape_nodes_list = cmds.ls(shapes=True, showType=show_type)

    if not show_type:
        shape_nodes_list.sort()

    return shape_nodes_list


def get_all_transform_nodes(show_type=True):
    """
    Get name list of all transform nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each transform node.

    Returns: 
        list of str
            Name list of all transform nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    transform_nodes_list = cmds.ls(transforms=True, showType=show_type)

    if not show_type:
        transform_nodes_list.sort()

    return transform_nodes_list


def get_all_geometry_nodes(show_type=True):
    """
    Get name list of all geometry nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each geometry node.

    Returns: 
        list of str
            Name list of all geometry nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    geometry_nodes_list = cmds.ls(geometry=True, showType=show_type)

    if not show_type:
        geometry_nodes_list.sort()

    return geometry_nodes_list


def get_all_camera_nodes(show_type=True):
    """
    Get name list of all camera nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each camera node.

    Returns: 
        list of str
            Name list of all camera nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    camera_nodes_list = cmds.ls(cameras=True, showType=show_type)

    if not show_type:
        camera_nodes_list.sort()

    return camera_nodes_list


def get_all_light_nodes(show_type=True):
    """
    Get name list of all light nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each light node.

    Returns: 
        list of str
            Name list of all light nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    light_nodes_list = cmds.ls(lights=True, showType=show_type)

    if not show_type:
        light_nodes_list.sort()

    return light_nodes_list


def get_all_material_nodes(show_type=True):
    """
    Get name list of all material nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each material node.

    Returns: 
        list of str
            Name list of all material nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    material_nodes_list = cmds.ls(materials=True, showType=show_type)

    if not show_type:
        material_nodes_list.sort()

    return material_nodes_list


def get_all_texture_nodes(show_type=True):
    """
    Get name list of all texture nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each texture node.

    Returns: 
        list of str
            Name list of all texture nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    texture_nodes_list = cmds.ls(textures=True, showType=show_type)

    if not show_type:
        texture_nodes_list.sort()

    return texture_nodes_list


def get_all_container_nodes(show_type=True):
    """
    Get name list of all container nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each container node.

    Returns: 
        list of str
            Name list of all container nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    container_nodes_list = cmds.ls(containers=True, showType=show_type)

    if not show_type:
        container_nodes_list.sort()

    return container_nodes_list


def get_all_plane_nodes(show_type=True):
    """
    Get name list of all plane nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each plane node.

    Returns: 
        list of str
            Name list of all plane nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    plane_nodes_list = cmds.ls(planes=True, showType=show_type)

    if not show_type:
        plane_nodes_list.sort()

    return plane_nodes_list


def get_all_partition_nodes(show_type=True):
    """
    Get name list of all partition nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each partition node.

    Returns: 
        list of str
            Name list of all partition nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    partition_nodes_list = cmds.ls(partitions=True, showType=show_type)

    if not show_type:
        partition_nodes_list.sort()

    return partition_nodes_list


def get_all_set_nodes(show_type=True):
    """
    Get name list of all set nodes. 

    Args:
        show_type: boolean
            Whether to show the node type of each set node.

    Returns: 
        list of str
            Name list of all set nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    set_nodes_list = cmds.ls(sets=True, showType=show_type)

    if not show_type:
        set_nodes_list.sort()

    return set_nodes_list


def export_nodes_list(save_dir='./', show_type=True):
    """
    Export differnet type of nodes.

    Args:
        save_dir: str
            Directory to save .obj files for all target shapes of a blendshape node.
        show_type: boolean
            Whether to show the node type of each shape node.
            If show_type==True, every second line in the saved file shows the node type.

    Returns: 
        None.
    """

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()

    node_types_filename = osp.join(
        save_dir, '{}.node_types.txt'.format(scene_name))

    pprint('\n===> get all node types')

    node_types_list = get_node_types()

    pprint('---> all node types:')
    # pprint(node_types_list)
    pprint('\n===> {} node types in total'.format(len(node_types_list)))

    pprint('\n===> save node types into file: ')
    pprint(node_types_filename)
    fp = open(node_types_filename, 'w')
    if len(node_types_list) > 0:
        fp.write('\n'.join(node_types_list) + '\n')
    fp.close()

    pprint('\n===> get all nodes')
    nodes_list_filename = osp.join(
        save_dir, '{}.{}_nodes.txt'.format(scene_name, 'all'))

    nodes_list = get_all_nodes_list(show_type)

    # for idx, node in enumerate(nodes_list):
    #     pprint('---> {}: {}'.format(idx+1, node))
    # pprint(nodes_list)

    pprint('\n===> {} node keys in total'.format(len(nodes_list)))

    pprint('\n===> save all nodes list into file: ')
    pprint(nodes_list_filename)
    fp = open(nodes_list_filename, 'w')
    if len(nodes_list) > 0:
        fp.write('\n'.join(nodes_list) + '\n')
    fp.close()

    node_types_list = ['transform', 'shape',
                       'geometry', 'mesh',
                       'blendshape', 'joint',
                       'camera', 'light',
                       'material', 'texture',
                       'set', 'partition',
                       'plane',
                       'container'
                       ]

    for node_type in node_types_list:
        pprint('\n===> save nodes of type {}'.format(node_type))
        nodes_list_filename = osp.join(
            save_dir, '{}.nodes_list.{}_nodes.txt'.format(scene_name, node_type))

        get_func_name = "get_all_{}_nodes".format(node_type)
        nodes_list = eval(get_func_name)(show_type)

        # for idx, node in enumerate(nodes_list):
        #     pprint('---> {}: {}'.format(idx+1, node))
        # pprint(nodes_list)

        pprint('\n===> {} nodes in total'.format(len(nodes_list)))

        pprint('\n===> save list of nodes (type: {}) into file: '.format(node_type))
        pprint(nodes_list_filename)
        fp = open(nodes_list_filename, 'w')
        if len(nodes_list) > 0:
            fp.write('\n'.join(nodes_list) + '\n')
        fp.close()


if __name__ == '__main__':
    # blendshape_node_name = r'AI_TD_01_Head01_blendShape'
    # mesh_node_name = r'AI_TD_01_Head01Shape'

    save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/yuanli_bs_tang2'
    show_type = True

    export_nodes_list(save_dir, show_type)
