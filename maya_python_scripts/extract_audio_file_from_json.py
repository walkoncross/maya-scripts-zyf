# coding=utf-8
# """
# Export .obj files for all blendshape weights in Maya.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import os
import os.path as osp
import json
import base64
import tempfile

from scipy.io import wavfile
import numpy as np


def extract_audio_file_from_json(json_file, save_dir):
    with open(json_file, 'r') as fp:
        attr_frames_list = json.load(fp)
        fp.close()

    base_name = osp.basename(json_file)

    audio_data_list = list()

    frame_cnt = 0
    for attr_frame in attr_frames_list:
        # frame_cnt = attr_frame['frame_num']
        frame_cnt += 1

        b64enc_audio = attr_frame["frame"]["animation"]["agent"]["audio"]
        audio = base64.b64decode(b64enc_audio)

        fp = tempfile.TemporaryFile()
        fp.write(audio)
        fp.seek(0)
        sample_rate, audio_data = wavfile.read(fp)
        fp.close()

        audio_data_list.append(audio_data)
        # print('sample_rate=',sample_rate)
        # print('audio_data.shape', audio_data.shape)
        # print(type(audio))
        # exit()

    # audio_data
    concated_audio_data = np.vstack(audio_data_list)
    print('===> sample_rate=',sample_rate)
    print('===> concated_audio_data.shape', concated_audio_data.shape)
    print('===> sample_rate=',sample_rate)

    audio_fname = osp.join(save_dir, base_name+'.wav')
    wavfile.write(audio_fname, sample_rate, concated_audio_data)
    
    print('===> {} frames in total'.format(frame_cnt))
    print('===> extracted audio saved into: ', audio_fname)
    return audio_fname

if __name__ == '__main__':
    keyframe_json_filename = r'/Users/zhaoyafei/Downloads/video2bs_with_bones/jinghuashuo8_bs_head_version1_20201127.json'
    save_dir = r'/Users/zhaoyafei/Downloads/video2bs_with_bones/'

    audio_fname = extract_audio_file_from_json(keyframe_json_filename, save_dir)
