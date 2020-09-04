# coding=utf-8
# """
# Export .fbx files for skeleton animation in Maya.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import json
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint


def get_current_scene_name():
    """Get current scene name.

    Args: 
        None.

    Returns: 
        str
            Scene name.
    """

    scene_name = cmds.file(query=True, sceneName=True, shortName=True)
    scene_name = osp.splitext(scene_name)[0]

    return scene_name


def get_keyframe_count_for_node(node_name, trans_attr=True, rotate_attr=False, all_attr=False):
    """Get animation keyframe count.

    Args: 
        node_name: str
            Node name (keyframed) to count animation keyframes.
        trans_attr: bool
            Check traslate attributes (tx, ty, tz)
        rotate_attr: bool
            Check rotate attributes (rx, ry, rz)
        all_attr: bool
            Check all attributes.

    Returns: 
        num_frames: int
            Number of animation keyframes
    """
    num_frames = 0
    attr_list = []

    if all_attr:
        attr_list = cmds.listAttr(node_name, keyable=True)
    else:
        if trans_attr:
            attr_list += ['tx', 'ty', 'tz']

        if rotate_attr:
            attr_list += ['rx', 'ry', 'rz']

    for attr in attr_list:
        node_attr = node_name + '.' + attr
        frames = cmds.keyframe(node_attr, q=True, keyframeCount=True)
        num_frames = max(frames, num_frames)

    # anim_curves = cmds.keyframe(node_name, q=True, name=True)
    # for curve in anim_curves:
    #     frames = cmds.keyframe(curve, q=True, keyframeCount=True)
    #     num_frames = max(frames, num_frames)

    return num_frames


def export_animation_into_fbx(
    root_node_name,
    save_dir='./',
    start_time=0,
    end_time=240
):
    """Export animation of a node into .fbx file.

    Args:
        root_node_name: str
            Name of root joint.
        save_dir: str
            Directory to save .fbx files.
        start_time: int
            Start frame of animation
        end_time: int
            End frame of animation

    Returns: 
        None.
    """
    pprint("===> root_node_name: {}".format(root_node_name))
    pprint("===> save_dir: {}".format(save_dir))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    output_filename = osp.join(
        save_dir, '{}.animation.{}.fbx'.format(scene_name, root_node_name.replace(':', '-')))
    pprint("===> output file: {}".format(output_filename))

    # num_frames = cmds.keyframe(root_node_name, q=True, keyframeCount=True) / 6
    # num_frames = get_keyframe_count(root_node_name)
    # pprint('===> {} keyframes in total'.format(num_frames))

    pprint('===> start_time'.format(start_time))
    pprint('===> end_time'.format(end_time))

    cmds.currentTime(0)
    cmds.select(root_node_name, replace=True)

    # mel.eval('FBXExportAnimationOnly -v true;')
    # mel.eval('FBXExportBakeComplexAnimation -v true;')
    # mel.eval('FBXExportBakeComplexStart -v 0;')
    # mel.eval('FBXExportBakeComplexEnd -v {};'.format(num_frames))
    # mel.eval('FBXExportBakeComplexStep -v 1;')
    # mel.eval('FBXExport -f "{}" -s;'.format(output_filename))

    # cmd_str = """
    #     FBXExportAnimationOnly -v true;
    #     FBXExportBakeComplexAnimation -v true;
    #     FBXExportBakeComplexStart -v 0;
    #     FBXExportBakeComplexEnd -v {};
    #     FBXExportBakeComplexStep -v 1;
    #     FBXExport -f "{}" -s;
    # """.format(num_frames, output_filename)

    # pprint('===> run command: ')
    # pprint(cmd_str)
    # mel.eval(cmd_str)

    cmd_str = 'FBXExportAnimationOnly -v true;'
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexAnimation - v true;'
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexStart - v {};'.format(start_time)
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexEnd -v {};'.format(end_time)
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexStep - v 1;'
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExport -f "{}" -s;'.format(output_filename)
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/work/maya-scripts-zyf/maya_exports'

    keyframe_node_name = r'mixamorig:Hips'
    # export_node_name = r'AI_TD_01_grp'
    export_node_name = keyframe_node_name
    start_time = 0
    # end_time = 240

    keyframe_count = get_keyframe_count_for_node(keyframe_node_name, trans_attr=True, rotate_attr=False)
    end_time = keyframe_count - 1

    export_animation_into_fbx(export_node_name, save_dir, start_time, end_time)
