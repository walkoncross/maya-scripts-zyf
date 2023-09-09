# coding=utf-8
# """
# Export .obj files for all blendshape weights in Maya.

# Authors: Zhao Yafei (zhaoyafei@baidu.com)
# """
import os
import os.path as osp
import maya.cmds as cmds
import maya.mel as mel


def get_bs_weights_name_list(blendshape_node_name):
    """
    Get name list of blendshape weights.
    Args:
        blendshape_node_name: name of blendshape (transform object) in Maya.

    Returns: name list of bs weights.

    """
    cmd = 'listAttr -m -st "weight" ' + blendshape_node_name
    bs_list = mel.eval(cmd)
    
    bs_list.sort()

    return bs_list


def export_obj_files_from_bs(mesh_node_name, blendshape_node_name, bs_keys, to_dir):
    """
    Export bs to obj files.
    Args:
        mesh_node_name: name of mesh/shape in Maya;
        blendshape_node_name: name of blendshape (transform object) in Maya;
        bs_keys: bs keys (weight names) to export;
        to_dir: the output dir.

    Returns: None.

    """
    # 0. Neutral pose.
    curr_time = 0
    for k in bs_keys:
        v = 0.
        cmds.setAttr("{}.{}".format(blendshape_node_name, k), v)
        cmds.setKeyframe("{}.{}".format(blendshape_node_name, k))
    
    cmd = "polyTriangulate -ch 1 " + mesh_node_name
    mel.eval(cmd)

    cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                  -typ "OBJexport" -pr -es " {}/{}.obj";""".format(to_dir, "00_neutral")
    mel.eval(cmd)

    # 1. For every bs.
    for curr_k in bs_keys:
        print(curr_k)
        curr_time += 1
        cmds.currentTime(curr_time)

        for k in bs_keys:
            v = 1.0 if curr_k == k else 0.
            cmds.setAttr("{}.{}".format(blendshape_node_name, k), v)
            cmds.setKeyframe("{}.{}".format(blendshape_node_name, k))

        cmd = "polyTriangulate -ch 1 " + mesh_node_name
        mel.eval(cmd)
    
        cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                      -typ "OBJexport" -pr -es " {}/{}.obj";""".format(to_dir, curr_k)
        mel.eval(cmd)


if __name__=='__main__':
    # mesh_node_name = 'FBXASC0510bsFBXASC040imdjsFBXASC041Shape'
    # blendshape_node_name = 'FBXASC0510bsFBXASC040imdjsFBXASC041_ncl1_2'
    # save_dir = '/Users/zhaoyafei/Downloads/bs'

    # mesh_node_name = 'FEIFBXASC232FBXASC132FBXASC184Shape'
    # blendshape_node_name = 'FEIFBXASC232FBXASC132FBXASC184'
    # save_dir = '/Users/zhaoyafei/Downloads/bs_xiaopu_20200221'

    # mesh_node_name = 'FEIFBXASC232FBXASC132FBXASC184FBXASC046FBXASC231FBXASC153FBXASC190FBXASC229FBXASC186FBXASC166FBXASC228FBXASC186FBXASC186FBXASC231FBXASC137FBXASC1695FBXASC046002Shape'
    # blendshape_node_name = 'FBXASC231FBXASC153FBXASC190FBXASC229FBXASC186FBXASC166FBXASC228FBXASC186FBXASC186FBXASC231FBXASC137FBXASC1695FBXASC046005_ncl1_1'
    # save_dir = '/Users/zhaoyafei/Downloads/bs_xiaopu_20200228'

    mesh_node_name = 'AI_TD_01_Head01Shape'
    blendshape_node_name = 'AI_TD_01_Head01_blendShape'
    save_dir = '/Users/zhaoyafei/Downloads/bs_definition_3D_face/yuanli_bs_tang'

    if not osp.exists(save_dir):
        os.mkdir(save_dir)

    bs_keys = get_bs_weights_name_list(blendshape_node_name)

    for idx, bs in enumerate(bs_keys):
        print idx+1, bs

    bs_keys_fn = save_dir + '/00_bs_keys.txt'
    fp = open(bs_keys_fn, 'w')
    fp.write('\n'.join(bs_keys) + '\n')
    fp.close()

    export_obj_files_from_bs(mesh_node_name, blendshape_node_name, bs_keys, save_dir)
