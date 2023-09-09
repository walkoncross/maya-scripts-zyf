# coding=utf-8
# """

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import json

bs_prefix  = ['Brow', 'Cheek', 'Ear', 'Eye', 'Lip', 'Mouth', 'Nose', 'Throat']

def check_combined_bs(bs_name):
    """
    Is combined bs.

    Args: 
        bs_name: str

    Returns: 
        bool
    """

    splits = bs_name.split('_')

    combined_bs = False
    driver_bs_list = None

    if len(splits) > 1:
        for prefix in bs_prefix:
            if prefix in splits[1]:
                combined_bs = True
                driver_bs_list = splits
                break

    return combined_bs, driver_bs_list


def bs_has_inbetween(bs_name):
    """
    Is combined bs.

    Args: 
        bs_name: str

    Returns: 
        bool
    """

    has_inbetween = '4D' in bs_name
    return has_inbetween


if __name__ == '__main__':
    input_fn = r'/Users/zhaoyafei/work/maya_exports/LiuMengZhang_rig_0830.blendshape.head_lod0_mesh_blendShape.txt'

    combined_bs_list = []
    combined_bs_dict = {}
    regular_bs_list = []
    inbetween_bs_list = []

    with open(input_fn, 'r') as fid:
        lines = fid.readlines()

        for line in lines:
            bs_name = line.strip()

            combined_bs, driver_bs_list = check_combined_bs(bs_name)

            if combined_bs:
                combined_bs_list.append(bs_name)
                combined_bs_dict[bs_name] = driver_bs_list
            elif bs_has_inbetween(bs_name):
                inbetween_bs_list.append(bs_name)
            else:
                regular_bs_list.append(bs_name)

    root, ext = osp.splitext(input_fn)

    bs_fn = root + '.regular_bs_list.json'
    with open(bs_fn, 'w') as fid:
        json.dump(regular_bs_list, fid, indent=2)
    
    bs_fn = root + '.combined_bs_list.json'
    with open(bs_fn, 'w') as fid:
        json.dump(combined_bs_list, fid, indent=2)
    
    bs_fn = root + '.combined_bs_dict.json'
    with open(bs_fn, 'w') as fid:
        json.dump(combined_bs_dict, fid, indent=2)
    
    bs_fn = root + '.inbetween_bs_list.json'
    with open(bs_fn, 'w') as fid:
        json.dump(inbetween_bs_list, fid, indent=2)