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


def load_keyframe_names(mapping_file):
    """
    Load keyframe frame-to-names mapping from mapping file.

    Args: 
        mapping_file: str
            Path to mapping file.

    Returns: 
        dict
            A dict with element (k=str(keyframe_number), v=keyframe_name).
    """
    fp = open(mapping_file)
    lines = fp.readlines()
    names_dict = OrderedDict()

    for line in lines[1:]:
        k, v = line.split()
        names_dict[str(int(k))] = v.strip()

    return names_dict


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


def export_keyframe_meshes_into_objs(mesh_node_name, save_dir='./',
                                     start_frame=1, end_frame=10,
                                     keyframe_names=None):
    """
    Export keyframe meshes into .obj files.

    Args:
        mesh_node_name: str or list of str
            Name of mesh/shape in Maya;
        save_dir: str
            Directory to save .obj files for all target shapes of a blendshape node.
        start_frame: int
            Frame Number of the start keyframe;
        end_frame: int
            Frame Number of the end keyframe;
        keyframe_names: None or a dict. (optional)
            If a dict, elements should be (k=str(keyframe_number), v=keyframe_name).

    Returns: 
        None.
    """
    pprint("===> mesh_node_name: {}".format(mesh_node_name))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()

    save_dir += '/{}_keyframe_mesh_objs'.format(scene_name)
    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    # Export keyframe meshes.
    for curr_time in range(start_frame, end_frame+1):
        pprint('===> Export mesh at time: #{}'.format(curr_time))
        cmds.currentTime(curr_time)

        if isinstance(mesh_node_name, list):
            cmd = "polyTriangulate -ch 1 " + ' '.join(mesh_node_name)
        else:
            cmd = "polyTriangulate -ch 1 " + mesh_node_name
        pprint('===> run MEL command: ')
        pprint(cmd)
        mel.eval(cmd)

        frame_name = ''
        if isinstance(keyframe_names, dict):
            frame_name = keyframe_names.get(str(curr_time), '')
        if not frame_name:
            frame_name = 'frame_{}'.format(curr_time)

        # obj_filename = osp.join(save_dir, curr_k+'.obj')
        # cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
        #               -typ "OBJexport" -pr -es " {}";""".format(obj_filename)
        cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                      -typ "OBJexport" -pr -es " {}/arkit_{}.obj";""".format(save_dir, frame_name)
        pprint('===> run MEL command: ')
        pprint(cmd)
        mel.eval(cmd)


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/maya_exports'
    # blendshape_node_name = r'Head01_blendShape'
    # mesh_node_name = get_blendshape_geometry_name(blendshape_node_name)
    # pprint("===> mesh_node_name: {}".format(mesh_node_name))
    mesh_node_name = r'Head01Shape'
    keyframe_names_file = r'/Users/zhaoyafei/work/maya-scripts-zyf/data/keyframe_names.txt'

    keyframe_names = load_keyframe_names(keyframe_names_file)

    export_keyframe_meshes_into_objs(mesh_node_name, save_dir,
                                     start_frame=1, end_frame=27,
                                     keyframe_names=keyframe_names)
