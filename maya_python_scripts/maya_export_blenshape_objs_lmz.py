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


def make_blendshape_keys_settable(blendshape_node_name, save_dir, blendshape_keys_list=None, forced=False):
    """
    Make keyable/settable a list of blendshape keys (name of target-shapes/morphing-targets)
    by unlocking/makeing settable/breaking connections.

    Args:
        blendshape_node_name: str
            Name of blend shape deformer (blendShape Node) in Maya.
        save_dir: str
            Where to save the restore info file
        blendshape_keys_list: list of str
            List of blendshape keys (weight names).
        forced: bool
            If True, will not ask user to check.

    Returns: tuple of (int, str)
        str: file path to restore info of all the modifications to make blendshape settable.
    """

    need_restore = -1
    info_str = ""

    if forced:
        input_words = 'y'
    else:
        pprint("""\n===> Are you sure to make blendshape attributes settable? 
                    This will try to make attributes settable by making them keyable, unlocking them, 
                    breaking their connection. Although this script will try to save the modification info,
                    and use these info to restore all the attribute state back, 
                    there still is risk not able to restore everything.
                    Please make a copy of your Maya Project (.ma,.mb), and operates in the project copy. 
                    If you are aware of what you are doing, input 'yes' or 'y' to continue;
                    Otherwise, this script will exit.""")
        input_words = raw_input('yes or no:')
        input_words = input_words.lower()

    if not(input_words == 'yes' or input_words == 'y'):
        need_restore = -1
        info_str = "make_blendshape_keys_settable() is canceled"
    else:
        scene_name = get_current_scene_name()
        need_restore = True

        settable_restore_info_list = []

        if blendshape_keys_list is None:
            blendshape_keys_list = get_blendshape_keys_list(
                blendshape_node_name)

        for k in blendshape_keys_list:
            key_name = "{}.{}".format(blendshape_node_name, k)
            restore_info_dict = {'key_name': key_name}

            if not cmds.getAttr(key_name, settable=True):
                pprint('---> Attribute {} is not settable'.format(key_name))
                pprint('     Try to make it keyable and unlocked')

                keyable = cmds.getAttr(key_name, keyable=True)
                lock = cmds.getAttr(key_name, lock=True)

                restore_info_dict["keyable"] = keyable
                restore_info_dict["lock"] = lock

                # set attr keyable and unlock attr
                cmds.setAttr(key_name, keyable=True, lock=False)

                if not cmds.getAttr(key_name, settable=True):
                    pprint('---> Attribute {} is still not settable'.format(key_name))
                    pprint('     Try to break all the connections upon it.')
                    # break all connections:
                    # cmd = 'CBdeleteConnection ' + key_name
                    # mel.eval(cmd)
                    restore_info_dict["connections_from"] = cmds.listConnections(
                        key_name, d=False, s=True, p=True)
                    restore_info_dict["connections_to"] = cmds.listConnections(
                        key_name, d=True, s=False, p=True)

                    if isinstance(restore_info_dict["connections_from"], list) and len(restore_info_dict["connections_from"]) > 0:
                        for attr in restore_info_dict["connections_from"]:
                            cmds.disconnectAttr(attr, key_name)

                    if  isinstance(restore_info_dict["connections_to"], list) and len(restore_info_dict["connections_to"]) > 0:
                        for attr in restore_info_dict["connections_to"]:
                            cmds.disconnectAttr(key_name, attr)

                settable_restore_info_list.append(restore_info_dict)

        if len(settable_restore_info_list) > 0:
            restore_filename = osp.join(
                save_dir, '{}.blendshape.restore_info.txt'.format(scene_name))
            pprint('\n===> save blendshape restore info into file: ')
            pprint(restore_filename)
            fp = open(restore_filename, 'w')
            fp.write(json.dumps(settable_restore_info_list, indent=2) + '\n')
            fp.close()

            need_restore = 1
            info_str = restore_filename

        else:
            need_restore = 0
            info_str = "Nothing to restore"

    return (need_restore, info_str)


def restore_settable_modification(restore_info):
    """
    Restore all the modifications to make keyable/settable a list of 
    blendshape keys (name of target-shapes/morphing-targets)
    by unlocking/makeing settable/breaking connections.

    Args:
        restore_info: list of dict or str
            list of dict: Restore info of all the modifications to make blendshape settable.
            str: path to the restore info file

    Returns: 
        None.
    """
    if isinstance(restore_info, list):
        settable_restore_info_list = restore_info
    elif isinstance(restore_info, str) and osp.isfile(restore_info):
        with open(restore_info, 'r') as fp:
            settable_restore_info_list = json.load(fp)
            fp.close()
    else:
        pprint("===> restore_settable_modification(): valid input ")
        return

    for restore_info_dict in settable_restore_info_list[::-1]:
        key_name = restore_info_dict['key_name']
        if "connections_to" in restore_info_dict and isinstance(restore_info_dict["connections_to"], list) and len(restore_info_dict["connections_to"]) > 0:
            for attr in restore_info_dict["connections_to"]:
                cmds.connectAttr(key_name, attr)
        if "connections_from" in restore_info_dict and  isinstance(restore_info_dict["connections_from"], list) and len(restore_info_dict["connections_from"]) > 0:
            for attr in restore_info_dict["connections_from"]:
                cmds.connectAttr(attr, key_name)

        # restore attr keyable info and lock info
        cmds.setAttr(
            key_name, keyable=restore_info_dict["keyable"], lock=restore_info_dict["lock"])


def export_blendshape_target_shapes(blendshape_node_name,
                                    mesh_node_name,
                                    save_dir='./',
                                    blendshape_keys_list=None,
                                    force_triangulate=False,
                                    skip_existing_files=True):
    """
    Export target shapes into .obj files for a blendshape node (name of target-shapes/morphing-targets).

    Args:
        blendshape_node_name: str
            Name of blend shape deformer (blendShape Node) in Maya.
        mesh_node_name: str or list of str
            Name of mesh/shape in Maya;
        save_dir: str
            Directory to save .obj files for all target shapes of a blendshape node.
        blendshape_keys_list: list of str or None
            List of blendshape keys  (names of target shapes) to export. If =None, export all target shapes.

    Returns: 
        None.
    """
    pprint("===> blendshape_node_name: {}".format(blendshape_node_name))
    pprint("===> mesh_node_name: {}".format(mesh_node_name))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    blendshape_keys_filename = osp.join(
        save_dir, '{}.blendshape.{}.txt'.format(scene_name, blendshape_node_name))

    if blendshape_keys_list is None:
        blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=True)

    for idx, blendshape in enumerate(blendshape_keys_list):
        pprint('---> {}: {}'.format(idx+1, blendshape))

    pprint('\n===> {} blendshape keys in total'.format(len(blendshape_keys_list)))

    pprint('\n===> save blendshape keys into file: ')
    pprint(blendshape_keys_filename)
    fp = open(blendshape_keys_filename, 'w')
    fp.write('\n'.join(blendshape_keys_list) + '\n')
    fp.close()

    # 0. make all blendshape keys/attributes settable
    need_restore, restore_info = make_blendshape_keys_settable(
        blendshape_node_name, save_dir, blendshape_keys_list, forced=False)

    if need_restore < 0:
        exit()

    # 1. Export the neutral pose.
    obj_filename = osp.join(save_dir, '00_neutral.obj')
    pprint('===> Export the neutral pose into {}.'.format(obj_filename))

    curr_time = 0
    cmds.currentTime(curr_time)

    if osp.isfile(obj_filename) and skip_existing_files:
        pprint('===> skip existing file: {}'.format(obj_filename))
    else:
        for k in blendshape_keys_list:
            v = 0.
            key_name = "{}.{}".format(blendshape_node_name, k)

            cmds.setAttr(key_name, v)
            cmds.setKeyframe(key_name)

        # Select Mesh before export
        cmds.select(mesh_node_name)

        if force_triangulate:
            pprint('===> Force to export triangulated mesh')
            if isinstance(mesh_node_name, list):
                cmd = "polyTriangulate -ch 1 " + ' '.join(mesh_node_name)
            else:
                cmd = "polyTriangulate -ch 1 " + mesh_node_name

            pprint('===> run MEL command: ')
            pprint(cmd)

            mel.eval(cmd)

        cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
                    -typ "OBJexport" -pr -es " {}";""".format(obj_filename)

        # cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
        #             -typ "OBJexport" -pr -es " {}/{}.obj";""".format(save_dir, "00_neutral")
        pprint('===> run MEL command: ')
        pprint(cmd)
        mel.eval(cmd)

    # 2. Export blendshape target shapes.
    # for curr_k in blendshape_keys_list[:5]:
    for curr_k in blendshape_keys_list:
        obj_filename = osp.join(save_dir, curr_k+'.obj')

        # if not curr_k.startswith('jaw'):
        #     continue
        pprint('===> Export the blendshape key: {}'.format(curr_k))

        curr_time += 1
        cmds.currentTime(curr_time)

        if osp.isfile(obj_filename) and skip_existing_files:
            pprint('===> skip existing file: {}'.format(obj_filename))
        else:
            for k in blendshape_keys_list:
                v = 1.0 if curr_k == k else 0.
                key_name = "{}.{}".format(blendshape_node_name, k)
                cmds.setAttr(key_name, v)
                cmds.setKeyframe(key_name)

            # Select Mesh before export
            cmds.select(mesh_node_name)

            if force_triangulate:
                pprint('===> Force to export triangulated mesh')
                if isinstance(mesh_node_name, list):
                    cmd = "polyTriangulate -ch 1 " + ' '.join(mesh_node_name)
                else:
                    cmd = "polyTriangulate -ch 1 " + mesh_node_name

                pprint('===> run MEL command: ')
                pprint(cmd)
                mel.eval(cmd)

            cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
                        -typ "OBJexport" -pr -es " {}";""".format(obj_filename)
            # cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
            #               -typ "OBJexport" -pr -es " {}/{}.obj";""".format(save_dir, curr_k)
            pprint('===> run MEL command: ')
            pprint(cmd)
            mel.eval(cmd)

    if need_restore==1:
        restore_settable_modification(restore_info)


if __name__ == '__main__':
    save_dir = r'D:/zhaoyafei/lmz_head_mesh_blendshapes'
    # save_dir = r'/Users/zhaoyafei/Downloads/bs_definition_3D_face/bs_objs_bs_vert_quad'

    blendshape_node_name = r'head_lod0_mesh_blendShape'
    pprint("===> blendshape_node_name: {}".format(blendshape_node_name))

    # mesh_node_name = r'Head01Shape'
    mesh_node_name = get_blendshape_geometry_name(blendshape_node_name)
    pprint("===> mesh_node_name: {}".format(mesh_node_name))

    force_triangulate = False
    skip_existing_files = True

    export_blendshape_target_shapes(
        blendshape_node_name, mesh_node_name, save_dir,
        force_triangulate=force_triangulate,
        skip_existing_files=skip_existing_files)
