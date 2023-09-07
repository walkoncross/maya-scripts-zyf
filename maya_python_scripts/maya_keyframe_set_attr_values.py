# coding=utf-8
# """
# Set keyframe attribute values (blendshape weights and bones/joints rotations) in Maya.

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
                blendshape_node_name, sort_keys=True)

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

                    for attr in restore_info_dict["connections_from"]:
                        cmds.disconnectAttr(attr, key_name)

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
        if "connections_to" in restore_info_dict:
            for attr in restore_info_dict["connections_to"]:
                cmds.connectAttr(key_name, attr)
        if "connections_from" in restore_info_dict:
            for attr in restore_info_dict["connections_from"]:
                cmds.connectAttr(attr, key_name)

        # restore attr keyable info and lock info
        cmds.setAttr(
            key_name, keyable=restore_info_dict["keyable"], lock=restore_info_dict["lock"])


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


def set_keyframe_values(node_name, frame_number, attribute_values_dict):
    """
    Set keyframe at frame #frame_number.

    Args:
        node_name: str
            Name of ;
        frame_number: int
            Frame number (>0)
        attribute_values_dict: dict
            Values for blendshape weights, a dict

    Returns: 
        None.
    """

    cmds.currentTime(frame_number)
    pprint('===> currentTime {}'.format(frame_number))

    for k, v in attribute_values_dict.iteritems():
        key_name = "{}.{}".format(node_name, k)
        # pprint('---> setAttr {} {}'.format(key_name, v))
        try:
            cmds.setAttr(key_name, v)
        except:
            pprint('skip locked key: ' + key_name)

    cmds.setKeyframe(node_name)


if __name__ == '__main__':
    blendshape_node_name = r'AI_TD_01_Head01_blendShape'

    keyframe_json_filename = r'/Users/zhaoyafei/work/maya-scripts-zyf/data/add_smile_1_bs_head_version1_20201126.json'
    save_dir = r'/Users/zhaoyafei/work/maya-scripts-zyf/data'

    with open(keyframe_json_filename, 'r') as fp:
        attr_frames_list = json.load(fp)
        fp.close()

    frame_num = len(attr_frames_list)
    pprint('===> {} frames in total'.format(frame_num))

    # 0. make all blendshape keys/attributes settable
    blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=True)

    need_restore, restore_info = make_blendshape_keys_settable(
        blendshape_node_name, save_dir, blendshape_keys_list)

    if need_restore < 0:
        exit()

    frame_cnt = 0
    for attr_frame in attr_frames_list:
        # frame_cnt = attr_frame['frame_num']
        frame_cnt += 1

        bs_dict = attr_frame["frame"]["animation"]["agent"]["values"]
        set_keyframe_values(blendshape_node_name, frame_cnt, bs_dict)

        bones_dict = attr_frame["frame"]["animation"]["agent"]["bones"]

        for bone_name, attr_dict in bones_dict.iteritems():
            bone_name = bone_name.capitalize()
            set_keyframe_values(bone_name, frame_cnt, attr_dict)

    if need_restore==1:
        restore_settable_modification(restore_info)
