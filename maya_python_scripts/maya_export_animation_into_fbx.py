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


def export_animation_into_fbx(
        root_node_name,
        save_dir='./'):
    """
    Export animation of a node into .fbx file.

    Args:
        root_node_name: str
            Name of blend shape deformer (blendShape Node) in Maya.
        save_dir: str
            Directory to save .obj files for all target shapes of a blendshape node.

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

    num_frames = cmds.keyframe(root_node_name, q=True, kc=True) / 6
    pprint('===> {} keyframes in total'.format(num_frames))

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

    # pprint('===> run command: ', cmd_str)
    # mel.eval(cmd_str)

    cmd_str = 'FBXExportAnimationOnly -v true;'
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexAnimation - v true;'
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexStart - v 0;'
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexEnd -v {};'.format(num_frames)
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExportBakeComplexStep - v 1;'
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)

    cmd_str = 'FBXExport -f "{}" -s;'.format(output_filename)
    pprint('===> run command: ', cmd_str)
    mel.eval(cmd_str)


if __name__ == '__main__':
    save_dir = r'/Users/zhaoyafei/work/maya-scripts-zyf/maya_exports'
    root_node_name = r'mixamorig:Hips'

    export_animation_into_fbx(root_node_name, save_dir)
