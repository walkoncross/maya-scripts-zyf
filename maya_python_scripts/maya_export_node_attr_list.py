# coding=utf-8
# """
# Export attributes list of a node.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """

from __future__ import print_function
import os
import os.path as osp

import json
import maya.cmds



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


def export_node_attr_list(node_name, save_dir, only_user_defined=False):
    """
    Get attribute list of a node.

    Args: 
        node_name: str
            Node name.
        save_dir: str
            Path to save dir.
        only_user_defined: bool
            If True, only export user-defined attributes.

    Returns: 
        No returns.
    """    
    print("===> node_name: {}".format(node_name))
    print("===> save_dir: {}".format(save_dir))

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    if not osp.isdir(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()

    attr_list = cmds.listAttr(node_name, ud=only_user_defined)
    dump_str = json.dumps(attr_list, indent=2)

    print("===> User-defined attribute list of ", node_name)
    print(dump_str)

    fn = osp.join(
        save_dir, '{}.node_attr_list.{}.txt'.format(scene_name, node))

    # fn = osp.join(save_dir, node_name + '_attr_list.json')
    fp = open(fn, 'w')
    fp.write(dump_str + '\n')
    fp.close()


if __name__ == '__main__':
    nodes_list = ['head', 'L_shoulder', 'R_shoulder']
    save_dir = r'/Users/zhaoyafei/work/maya-scripts-zyf/maya_exports'
    only_user_defined = True

    for node in nodes_list:
        export_node_attr_list(node, save_dir,
                              only_user_defined=only_user_defined)
