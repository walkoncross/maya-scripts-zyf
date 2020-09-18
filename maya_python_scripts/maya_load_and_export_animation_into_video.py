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


def load_animation_from_fbx(fbx_path):
    """Load animation from .fbx file.

    Args: 
        fbx_path: str
            Path to .fbx file.

    Returns: 
        No returns.
    """
    base_name = osp.splitext(osp.basename(fbx_path))[0]
    name_space = base_name.replace(' ', '_')

    # cmd_str = 'FBXImport -f "{}" ;'.format(fbx_path) # Failed
    cmd_str = ('file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "{}" -options "fbx"  -pr  -importTimeRange "combine" "{}" ;'.format(name_space, fbx_path))
    pprint('===> run command: ')
    pprint(cmd_str)
    mel.eval(cmd_str)

    cmds.currentTime(0)


def export_animation_into_video(
    root_node_name,
    save_dir='./',
    save_filename='',
    start_time=0,
    end_time=240
):
    """Export animation of a node into video file.

    Args:
        root_node_name: str
            Name of root joint.
        save_dir: str
            Directory to save video files.
        save_filename: str
            Video filename. The full file path is : {save_dir}/{save_filename}
            If set None or a null string, filename will be automaticly set to:
                <scane_name>.animation.<root_node_name>.<ext>
            <ext>: depending on your OS system, e.g. .mov on MacOS.
        start_time: int
            Start frame of animation
        end_time: int
            End frame of animation

    Returns: 
        Full absolute path of saved file.
    """
    pprint("===> root_node_name: {}".format(root_node_name))
    pprint("===> save_dir: {}".format(save_dir))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    # save_dir = osp.abspath(save_dir)
    scene_name = get_current_scene_name()

    if not save_filename:
        save_filename = '{}.animation.{}'.format(scene_name, root_node_name.replace(':', '-'))
    
    output_filename = osp.join(save_dir, save_filename)
    pprint("===> output file: {}".format(output_filename))

    # num_frames = cmds.keyframe(root_node_name, q=True, keyframeCount=True) / 6
    # num_frames = get_keyframe_count(root_node_name)
    # pprint('===> {} keyframes in total'.format(num_frames))

    pprint('===> start_time: {}'.format(start_time))
    pprint('===> end_time: {}'.format(end_time))

    cmds.currentTime(0)

    """MEL
    string $isolated_panel = `paneLayout -q -pane1 viewPanes`;
    isolateSelect -state 0 $isolated_panel;
    isolateSelect -update $isolated_panel;

    select -r $driven_node;
    isolateSelect -state 1 $isolated_panel;

    playblast -filename $export_filename -offScreen -startTime $start_time -endTime $end_time  -format avfoundation  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 70;
    """
    # isolate selected object (make it the only active one) 
    isolated_panel = cmds.paneLayout("viewPanes", query=True, pane1=True)
    cmds.isolateSelect(isolated_panel, state=True)
    cmds.isolateSelect(isolated_panel, update=True)

    cmds.select(root_node_name, replace=True)
    cmds.isolateSelect(isolated_panel, loadSelected=True)

    cmd_str = 'playblast -filename "{}" -offScreen -startTime {} -endTime {} -format avfoundation  -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 100 -compression "H.264" -quality 70;'.format(output_filename, start_time, end_time)
    pprint('===> run command: ')
    pprint(cmd_str)

    # de-isolate
    cmds.isolateSelect(isolated_panel, state=False)
    
    output_filename = mel.eval(cmd_str)

    output_filename = osp.abspath(output_filename)
    pprint("===> full path of output file: {}".format(output_filename))

    return output_filename


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/work/maya-scripts-zyf/maya_exports'
    # input_fbx = r'‎/Volumes/seagate2Tz/backup/Downloads/3D_model_assets/adobe-mixamo-characters/xbot_dance_animations_noskin_30fps/Salsa Dance Variation Five.fbx'
    input_fbx = r'‎/Volumes/seagate2Tz/backup/Downloads/3D_model_assets/adobe-mixamo-characters/xbot_dance_animations_noskin_30fps/Samba Funky Pocoto Variation 1.fbx'

    # save_filename = r''
    base_name = osp.splitext(osp.basename(input_fbx))[0]
    save_filename = base_name.replace(' ', '_') + '.mp4'

    keyframe_node_name = r'mixamorig:Hips'
    export_node_name = r'AI_TD_01_grp'
    start_time = 0
    # end_time = 240

    load_animation_from_fbx(input_fbx)

    keyframe_count = get_keyframe_count_for_node(
        keyframe_node_name, 
        trans_attr=True, 
        rotate_attr=False
    )
    end_time = keyframe_count - 1

    video_path = export_animation_into_video(
        export_node_name, 
        save_dir, 
        save_filename, 
        start_time, 
        end_time
    )

    print('='*32)
    print('===> video saved into: ', video_path)
    print('='*32)
