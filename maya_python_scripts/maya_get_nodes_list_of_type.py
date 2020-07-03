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


def get_nodes_list_of_type(node_type, show_type=True):
    """
    Get name list of all shape nodes. 
    (Shapes in Maya are selectable DAG objects that display in 3D views. 
    Meshes, NURBS surfaces and curves, and locators are just some examples of shapes.)

    Args:
        node_type: str
            node type, for example: mesh, transform, texture, geometryShape, blendShape.
        show_type: boolean
            Whether to show the node type of each shape node.

    Returns: 
        list of str
            Name list of all shape nodes.
            If show_type==True, every second item in the list is the node type of its previous item.

    """

    nodes_list = cmds.ls(type=node_type, showType=show_type)

    if not show_type:
        nodes_list.sort()

    return nodes_list


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
                       'geometryShape', 'mesh',
                       'nurbsCurve', 'nurbsSurface',
                       'blendShape', 'joint',
                       'lattice', 'jiggle', 'deltaMush',
                       'tweak',
                       'skinCluster', 'jointCluster',
                       'animCurve',
                       'locator', 'lookAt',
                       'constraint',
                       'parentConstraint', 'pointConstraint',
                       #    'scaleConstraint', 'orientConstraint',
                       #    'aimConstraint', 'dynamicConstraint',
                       #    'geometryConstraint', 'symmetryConstraint',
                       #    'tangentConstraint', 'normalConstraint',
                       #    'rigidConstraint', 'hairConstraint',
                       'material', 'texture',
                       #    'lambert', 'phong',
                       'camera', 'light',
                       #    'pointLight', 'spotLight',
                       #    'volumeLight', 'areaLight',
                       #    'ambientLight', 'directionalLight',
                       #    'plane',
                       #    'objectSet', 'partition',
                       #    'container'
                       ]

    for node_type in node_types_list:
        pprint('\n===> save nodes of type {}'.format(node_type))
        nodes_list_filename = osp.join(
            save_dir, '{}.nodes_list_of_type.{}_nodes.txt'.format(scene_name, node_type))

        nodes_list = get_nodes_list_of_type(node_type, show_type)

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
