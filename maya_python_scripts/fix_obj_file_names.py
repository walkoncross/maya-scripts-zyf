import os.path as osp
import glob
import shutil


obj_files = glob.glob("*.obj")

prefix_len = len('lmz_head_mesh_blendshapes')

for obj_fn in obj_files:
    print('---> process ' + obj_fn)
    with open(obj_fn, 'r') as fp_in:
        lines = fp_in.readlines()
        splits = lines[2].split(' ') #mtllib lmz_head_mesh_blendshapes00_neutral.mtl\n

        #splits[1] = 'lmz_head_mesh_blendshapes00_neutral.mtl\n'
        splits[1] = splits[1][prefix_len:]
        lines[2] = ' '.join(splits)

        base_fn = osp.splitext(splits[1])[0]

        new_obj_fn = base_fn + '.obj'

        with open(new_obj_fn, 'w') as fp_out:
            fp_out.writelines(lines)
        
        new_mtl_fn = base_fn + '.mtl'

        shutil.copy('00_neutral (1).mtl', new_mtl_fn)


        