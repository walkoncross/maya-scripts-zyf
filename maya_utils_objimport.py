# coding=utf-8
# """
# Export .obj files for all blendshape weights in Maya.

# Authors: Zhao Yafei (zhaoyafei@baidu.com)
# """
from __future__ import print_function
import os
import os.path as osp
import glob
import pprint

import maya.cmds as cmds
import maya.mel as mel


def check_existance(path):
    if not osp.exists(path):
        raise Exception('Path Not Found: ' + path)

    
def import_file(fn, group_name="myobj"):
    """Import an individual OBJ file
    
    Ref: http://download.autodesk.com/us/maya/2011help/CommandsPython/file.html
    """
    cmds.file(fn, i=True, ra=True, groupReference=True, groupName=group_name)


def make_blendshape(bs_name, neutral_mesh_name, transform_name_list):
    """"Make a blendshape using blendShape() from Maya CommandsPython .

    Ref: http://download.autodesk.com/us/maya/2011help/CommandsPython/blendShape.html
    Examples for blendShape():
    # Perform a blendShape using the currently-selected objects.
    # The lead (last-selected) object will be the base shape, and each
    # of the others become targets.
    #
    cmds.blendShape()

    #
    # Create a blendShape that starts with curve3 as the base, and blends
    # in curve1 and curve2 as targets.

    cmds.blendShape( 'curve1', 'curve2', 'curve3' )

    #
    # Apply 80% of the total blendShape deformation, by setting
    # the envelope parameter to 0.8
    cmds.blendShape( 'blendShape1', edit=True, en=0.8 )


    #
    # Set the weights for the first two target shapes to 0.6
    # and 0.1 respecxtively
    cmds.blendShape( 'blendShape1', edit=True, w=[(0, 0.6), (1, 0.1)] )

    #
    # Add a third target (target3) to the blendShape on curve3
    cmds.blendShape( 'blendShape1', edit=True, t=('curve3', 1, 'target3', 1.0) )

    #
    # Add an inbetween (smirk) on target3 for base shape curve3
    # The inbetween will take effect at a weight of 0.2
    cmds.blendShape( 'blendShape2', edit=True, ib=True, t=('curve3', 2, 'smirk', 0.2) )
    """
    

def import_obj_files(from_dir, neural_key, group_name='myobj'):
    """Import all obj files from a folder.

    Args:
        from_dir: the output dir;
        neural_key: key name for neutral mesh;
        group_name: group name for the imported meshes.

    Returns: None.

    """
    # 0. Neutral pose.
    obj_fn = osp.join(from_dir, neural_key + '.obj')
    check_existance(obj_fn)

    obj_list = glob.glob(from_dir + '/*.obj')
    pprint.pprint(obj_list)

    for obj_fn in obj_list: 
        check_existance(obj_fn)
        import_file(obj_fn, group_name)


if __name__=='__main__':
    from_dir = '/Users/zhaoyafei/Downloads/bs_definition_3D_face/Apple_ARKit_BS/OBJs'
    # neural_key = 'shape_0'
    
    neural_key = 'Neutral'
    group_name = 'arkit_bs_ref'
    import_obj_files(from_dir, neural_key, group_name)