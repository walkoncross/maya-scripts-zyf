# coding=utf-8
# """
# Export all expression in a scene/project in Maya.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import maya.cmds as cmds
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


def get_expression_list():
    """
    Get name list of expressions.

    Args: 
        None.

    Returns: 
        list of str
            Name list of all expressions.
    """

    expression_list = cmds.ls(type='expression')
    pprint(expression_list)

    return expression_list


def export_expression(expression_name, save_dir='./'):
    """
    Export the content (string) of a expression to save_dir.

    Args:
        expression_name: str
            Expression name;
        save_dir: str
            Save directory;

    Returns: 
        None.
    """
    pprint('===> export expression: ' + expression_name)
    save_filename = osp.join(save_dir, expression_name+'.txt')
    expression = cmds.getAttr(expression_name+'.expression')
    # pprint(expression)

    pprint('---> save expression into file {}'.format(save_filename))
    fp = open(save_filename, 'w')
    fp.write(expression)
    fp.close()


def export_all_expressions(save_dir):
    """
    Export the content (string) of all expression to save_dir, one .txt file for each expression.

    Args:
        save_dir: str
            Directory to save expression content file.

    Returns: 
        list of str
            Name list of all expressions.

    """
    
    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    scene_name = get_current_scene_name()
    save_dir = osp.join(save_dir, scene_name+'_expressions')
    os.mkdir(save_dir)

    expression_list = get_expression_list()

    for exp_name in expression_list:
        export_expression(exp_name, save_dir)


if __name__ == '__main__':
    save_dir = '/Users/zhaoyafei/work/maya-scripts-zyf/exported_expressions'
    export_all_expressions(save_dir)
