# coding=utf-8
# """
# Export attributes list of a node in Maya.

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


def get_attributes_list(controller_node_name, attribute_name_pattern=None):
    """
    Get attributes list of a node.

    Args:
        controller_node_name: str 
            Node Name in Maya.
        attribute_name_pattern: str
            List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

    Returns: 
        list of str
            Attribute name list of the input node.

    """

    # Maya Mel cmd
    # cmd = 'listAttr -k -m -st "weight" ' + controller_node_name
    # attributes_list = mel.eval(cmd)

    # Maya python cmd
    if attribute_name_pattern is None:
        attributes_list = cmds.listAttr(controller_node_name, multi=True, keyable=True)
    else:
        attributes_list = cmds.listAttr(
            controller_node_name, st=attribute_name_pattern, multi=True, keyable=True)

    attributes_list.sort()

    return attributes_list


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


def export_controller_to_bs_mapping(
        controller_node_name, 
        blendshape_node_name, 
        save_dir='./'):
    """
    Get and save attributes list of a node.

    Args:
        controller_node_name: str
            controller Node Name in Maya.
        blendshape_node_name: str
            blendshape Node Name in Maya.
        save_dir: str
            Directory to save attributes list.

    Returns: 
        None.
    """

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    attribute_name_pattern = 'CTRL*'
    controller_to_bs_mapping_dict = {}

    scene_name = get_current_scene_name()
    mapping_filename = osp.join(
        save_dir, '{}.{}.controller_to_bs_mapping_dict.json'.format(scene_name, blendshape_node_name))

    attributes_list = get_attributes_list(controller_node_name, attribute_name_pattern)
    attributes_dict = {}

    blendshape_keys_list = get_blendshape_keys_list(blendshape_node_name, sort_keys=False)

    for idx, attribute in enumerate(attributes_list):
        cmds.setAttr( controller_node_name + '.' + attribute, 0)
        attribute_value = cmds.getAttr( controller_node_name + '.' + attribute )
        attributes_dict[attribute] =  attribute_value
        pprint('---> {}: {} {}'.format(idx+1, attribute, attribute_value))

    pprint('\n===> {} attributes in total'.format(len(attributes_list)))

    for idx, attribute in enumerate(attributes_list):
        controller_vals = [1.0, -1.0, 0.5, -0.5]
        mapping_dict_list = []
        val_range = cmds.attributeQuery(attribute, node=controller_node_name, range=True)

        controller_to_bs_mapping_dict[attribute] = {}
        controller_to_bs_mapping_dict[attribute]['range'] = val_range
        pos_driven_bs = set()
        neg_driven_bs = set()

        for val in controller_vals:
            if val < val_range[0] or val > val_range[1]:
                continue

            cmds.setAttr(controller_node_name + '.' + attribute, val)

            bs_weights_list = cmds.getAttr(blendshape_node_name + '.weight')[0] # getAttr returns: [tuple(weights),]
            driven_bs_dict = {}

            for idx, blendshape in enumerate(blendshape_keys_list):
                if bs_weights_list[idx] > 0 or bs_weights_list[idx] < 0:
                    driven_bs_dict[blendshape] = bs_weights_list[idx]
                
                    if bs_weights_list[idx] * val < 0:
                        neg_driven_bs.add(blendshape)
                    else:
                        pos_driven_bs.add(blendshape)

            tmp_dict = {
                'controller_value': val,
                'driven_blendshapes': driven_bs_dict
            }
            mapping_dict_list.append(tmp_dict)

            cmds.setAttr(controller_node_name + '.' + attribute, 0)

        controller_to_bs_mapping_dict[attribute]['pos_driven_bs_list'] = list(pos_driven_bs)
        controller_to_bs_mapping_dict[attribute]['neg_driven_bs_list'] = list(neg_driven_bs)
        controller_to_bs_mapping_dict[attribute]['mapping'] = mapping_dict_list

    pprint('\n===> save attributes values dict into file: ')
    pprint(mapping_filename)
    fp = open(mapping_filename, 'w')
    json.dump(controller_to_bs_mapping_dict, fp, indent=2, sort_keys=True)
    fp.close()


if __name__ == '__main__':
    controller_node_name = r'Root_M'
    blendshape_node_name = r'head_lod0_mesh_blendShape'

    save_dir = r'D:/zhaoyafei/maya_exports'

    export_controller_to_bs_mapping(controller_node_name, blendshape_node_name, save_dir)