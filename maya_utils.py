# coding=utf-8
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
"""
The maya_utils file.

Authors: Wang Jianxiang (wangjianxiang01@baidu.com)
"""
import os
import json

import glob
import tqdm
import cask
import numpy as np
import maya.cmds as cmds
import maya.mel as mel

FACE_BS_PREFIX = "AI_TD_01_Head01_blendShape_ncl1_1"
TEETH_BS_PREFIX = "AI_TD_01_Teeth01_blendShape"

ALL_BS_KEYS = ["brows_dn_blink_1", "brows_dn_blink_2", "brows_dn_in", "brows_dn_in_1",
               "brows_dn_in_2", "brows_dn_in_3", "brows_dn_in_4", "brows_dn_in_eye_sqz",
               "brows_dn_out", "brows_dn_out_1", "brows_dn_out_2", "brows_dn_out_3",
               "brows_dn_out_4", "brows_sqz", "brows_sqz_1", "brows_sqz_2", "brows_sqz_3",
               "brows_sqz_4", "brows_sqz_eye_sqz", "brows_sqz_up", "brows_sqz_up_1",
               "brows_sqz_up_2", "brows_sqz_up_3", "brows_sqz_up_4", "brows_up", "brows_up_1",
               "brows_up_2", "brows_up_3", "brows_up_4", "brows_up_blink", "brows_up_blink_1",
               "brows_up_blink_2", "browssqz_blink", "browssqz_blink_1", "browssqz_blink_2",
               "browssqzup_blink", "browssqzup_blink_1", "browssqzup_blink_2", "cheek_raise",
               "cheek_raise_1", "cheek_raise_2", "cheek_raise_3", "cheek_raise_4", "cheek_raise_5",
               "cheek_raise_6", "cheek_raise_blink", "cheek_raise_blink_1", "cheek_raise_blink_2",
               "chin_dn", "chin_raise", "chin_raise_1", "chin_raise_2", "chin_raise_3",
               "chin_raise_4", "chin_raise_5", "chin_raise_6", "chin_tension", "corner_dn",
               "corner_dn_1", "corner_dn_2", "corner_sqz", "corner_sqz_1", "corner_sqz_2",
               "corner_up", "corner_up_1", "corner_up_10", "corner_up_2", "corner_up_3",
               "corner_up_4", "corner_up_5", "corner_up_6", "corner_up_7", "corner_up_8",
               "corner_up_9", "dimple", "dimple_1", "dimple_2", "dimple_3", "dimple_4", "disgust",
               "disgust_1", "disgust_2", "disgust_3", "disgust_4", "disgust_5", "disgust_6",
               "disgust_7", "disgust_8", "disgust_close", "disgust_close_1", "disgust_close_2",
               "eye_blink", "eye_blink_1", "eye_blink_2", "eye_blink_3", "eye_blink_4",
               "eye_blink_b", "eye_blink_b_1", "eye_blink_b_2", "eye_look_dn", "eye_look_dn_1",
               "eye_look_dn_2", "eye_look_dn_3", "eye_look_dn_4", "eye_look_dn_b",
               "eye_look_dn_b_1", "eye_look_dn_b_2", "eye_look_l", "eye_look_l_1", "eye_look_l_2",
               "eye_look_l_3", "eye_look_l_4", "eye_look_l__50", "eye_look_r", "eye_look_r_1",
               "eye_look_r_2", "eye_look_r_3", "eye_look_r_4", "eye_look_r__50", "eye_look_up",
               "eye_look_up_1", "eye_look_up_2", "eye_look_up_3", "eye_look_up_4", "eye_squint",
               "eye_squint_1", "eye_squint_2", "eye_squint_3", "eye_squint_4", "eye_squint_5",
               "eye_squint_6", "eye_sqz", "eye_sqz_1", "eye_sqz_2", "eye_sqz_3", "eye_sqz_4",
               "eye_sqz_5", "eye_sqz_6", "eye_sqz_blink", "eye_sqz_blink_1", "eye_sqz_blink_2",
               "frown", "frown_1", "frown_2", "frown_3", "frown_4", "funnel", "funnel_1",
               "funnel_2", "funnel_3", "funnel_4", "funnel_5", "funnel_6", "funnel_close",
               "funnel_close_1", "funnel_close_2", "funnel_wide", "funnel_wide_1", "funnel_wide_2",
               "funnel_wide_3", "funnel_wide_4", "head_ctrl_turn_l__15", "head_skin_slide",
               "jaw_back", "jaw_clench", "jaw_fwd", "jaw_l", "jaw_open", "jaw_open_1",
               "jaw_open_10", "jaw_open_2", "jaw_open_3", "jaw_open_4", "jaw_open_5", "jaw_open_6",
               "jaw_open_7", "jaw_open_8", "jaw_open_9", "jaw_r", "jaw_up", "lip_in", "lip_in_1",
               "lip_in_2", "lip_in_3", "lip_in_4", "lip_in_5", "lip_in_6", "lip_lock_back",
               "lip_lock_back_1", "lip_lock_back_2", "lip_lock_fwd", "lip_lock_fwd_1",
               "lip_lock_fwd_2", "lip_lock_l", "lip_lock_l_1", "lip_lock_l_2",
               "lip_lock_l_lip_lock_open", "lip_lock_open", "lip_lock_open_1", "lip_lock_open_2",
               "lip_lock_open_lip_lock_r", "lip_lock_r", "lip_lock_r_1", "lip_lock_r_2",
               "lwr_lid_dn", "lwr_lid_dn_1", "lwr_lid_dn_2", "lwr_lid_up", "lwr_lid_up_1",
               "lwr_lid_up_2", "lwr_lip_bk", "lwr_lip_dn", "lwr_lip_dn_1", "lwr_lip_dn_2",
               "lwr_lip_dn_3", "lwr_lip_dn_4", "lwr_lip_fwd", "lwr_lip_l", "lwr_lip_l_1",
               "lwr_lip_l_2", "lwr_lip_l_3", "lwr_lip_l_4", "lwr_lip_r", "lwr_lip_r_1",
               "lwr_lip_r_2", "lwr_lip_r_3", "lwr_lip_r_4", "lwr_lip_up", "lwr_lip_vol", "mouth_dn",
               "mouth_fwd", "mouth_l", "mouth_r", "mouth_up", "neck_1_ctrl_turn_l__15",
               "neck_2_ctrl_turn_l__15", "neck_3_ctrl_turn_l__15", "neck_blow", "neck_muscle",
               "neck_slide", "neck_tension", "neck_tension_1", "neck_tension_2", "nl_deep",
               "nl_deep_1", "nl_deep_2", "nl_deep_3", "nl_deep_4", "nl_deep_5", "nl_deep_6",
               "nl_deep_7", "nl_deep_8", "nl_deep_l", "nl_deep_r", "nose_close", "nose_dn",
               "nose_open", "o", "o_1", "o_2", "o_3", "o_4", "o_5", "o_6", "o_wide", "o_wide_1",
               "o_wide_2", "o_wide_3", "o_wide_4", "press", "press_1", "press_2", "press_3",
               "press_4", "press_5", "press_6", "pucker", "pucker_1", "pucker_2", "pucker_3",
               "pucker_4", "pucker_5", "pucker_6", "puff", "puff_1", "puff_2", "puff_dn",
               "puff_dn_1", "puff_dn_2", "puff_up", "puff_up_1", "puff_up_2", "smile", "smile_1",
               "smile_10", "smile_2", "smile_3", "smile_4", "smile_5", "smile_6", "smile_7",
               "smile_8", "smile_9", "smile_close", "smile_close_1", "smile_close_2", "smile_drop",
               "smile_drop_1", "smile_drop_2", "sneer", "sneer_1", "sneer_2", "sneer_3", "sneer_4",
               "sneer_5", "sneer_6", "sneer_7", "sneer_8", "sneer_close", "sneer_close_1",
               "sneer_close_2", "sticky_lips", "sticky_lips_1", "sticky_lips_10", "sticky_lips_2",
               "sticky_lips_3", "sticky_lips_4", "sticky_lips_5", "sticky_lips_6", "sticky_lips_7",
               "sticky_lips_8", "sticky_lips_9", "stretch", "stretch_1", "stretch_2", "stretch_3",
               "stretch_4", "stretch_close", "stretch_close_1", "stretch_close_2", "suck", "suck_1",
               "suck_2", "swallow_1", "swallow_2", "swallow_3", "swallow_4", "swallow_5", "tension",
               "tension_1", "tension_2", "tension_3", "tension_4", "tension_5", "tension_6",
               "tight", "tight_1", "tight_2", "upr_lid_dn", "upr_lid_dn_1", "upr_lid_dn_2",
               "upr_lid_up", "upr_lid_up_1", "upr_lid_up_2", "upr_lip_bk", "upr_lip_dn",
               "upr_lip_dn_1", "upr_lip_dn_2", "upr_lip_dn_3", "upr_lip_dn_4", "upr_lip_dn_5",
               "upr_lip_dn_6", "upr_lip_fwd", "upr_lip_vol", "wide", "wide_1", "wide_2"]

# Group bs keys.
BS_GROUP_NAME_TO_KEYS = {
    "brows_dn_blink_1_2_group": ["brows_dn_blink_1", "brows_dn_blink_2"],
    "brows_dn_in_1_3_group": ["brows_dn_in_1", "brows_dn_in_3"],
    "brows_dn_in_2_4_group": ["brows_dn_in_2", "brows_dn_in_4"],
    "brows_dn_out_1_3_group": ["brows_dn_out_1", "brows_dn_out_3"],
    "brows_dn_out_2_4_group": ["brows_dn_out_2", "brows_dn_out_4"],
    "brows_sqz_1_3_group": ["brows_sqz_1", "brows_sqz_3"],
    "brows_sqz_2_4_group": ["brows_sqz_2", "brows_sqz_4"],
    "brows_sqz_up_1_3_group": ["brows_sqz_up_1", "brows_sqz_up_3"],
    "brows_sqz_up_2_4_group": ["brows_sqz_up_2", "brows_sqz_up_4"],
    "brows_up_1_3_group": ["brows_up_1", "brows_up_3"],
    "brows_up_2_4_group": ["brows_up_2", "brows_up_4"],
    "brows_up_blink_1_2_group": ["brows_up_blink_1", "brows_up_blink_2"],
    "browssqz_blink_1_2_group": ["browssqz_blink_1", "browssqz_blink_2"],
    "browssqzup_blink_1_2_group": ["browssqzup_blink_1", "browssqzup_blink_2"],
    "cheek_raise_1_4_group": ["cheek_raise_1", "cheek_raise_4"],
    "cheek_raise_2_5_group": ["cheek_raise_2", "cheek_raise_5"],
    "cheek_raise_3_6_group": ["cheek_raise_3", "cheek_raise_6"],
    "cheek_raise_blink_1_2_group": ["cheek_raise_blink_1", "cheek_raise_blink_2"],
    "chin_raise_1_4_group": ["chin_raise_1", "chin_raise_4"],
    "chin_raise_2_5_group": ["chin_raise_2", "chin_raise_5"],
    "chin_raise_3_6_group": ["chin_raise_3", "chin_raise_6"],
    "corner_dn_1_2_group": ["corner_dn_1", "corner_dn_2"],
    "corner_sqz_1_2_group": ["corner_sqz_1", "corner_sqz_2"],
    "corner_up_1_6_group": ["corner_up_1", "corner_up_6"],
    "corner_up_2_7_group": ["corner_up_2", "corner_up_7"],
    "corner_up_3_8_group": ["corner_up_3", "corner_up_8"],
    "corner_up_4_9_group": ["corner_up_4", "corner_up_9"],
    "corner_up_5_10_group": ["corner_up_5", "corner_up_10"],
    "dimple_1_3_group": ["dimple_1", "dimple_3"],
    "dimple_2_4_group": ["dimple_2", "dimple_4"],
    "disgust_1_5_group": ["disgust_1", "disgust_5"],
    "disgust_2_6_group": ["disgust_2", "disgust_6"],
    "disgust_3_7_group": ["disgust_3", "disgust_7"],
    "disgust_4_8_group": ["disgust_4", "disgust_8"],
    "disgust_close_1_2_group": ["disgust_close_1", "disgust_close_2"],
    "eye_blink_1_3_group": ["eye_blink_1", "eye_blink_3"],
    "eye_blink_2_4_group": ["eye_blink_2", "eye_blink_4"],
    "eye_blink_b_1_2_group": ["eye_blink_b_1", "eye_blink_b_2"],
    "eye_look_dn_1_3_group": ["eye_look_dn_1", "eye_look_dn_3"],
    "eye_look_dn_2_4_group": ["eye_look_dn_2", "eye_look_dn_4"],
    "eye_look_dn_b_1_2_group": ["eye_look_dn_b_1", "eye_look_dn_b_2"],
    "eye_look_l_1_3_group": ["eye_look_l_1", "eye_look_l_3"],
    "eye_look_l_2_4_group": ["eye_look_l_2", "eye_look_l_4"],
    "eye_look_r_1_3_group": ["eye_look_r_1", "eye_look_r_3"],
    "eye_look_r_2_4_group": ["eye_look_r_2", "eye_look_r_4"],
    "eye_look_up_1_3_group": ["eye_look_up_1", "eye_look_up_3"],
    "eye_look_up_2_4_group": ["eye_look_up_2", "eye_look_up_4"],
    "eye_squint_1_4_group": ["eye_squint_1", "eye_squint_4"],
    "eye_squint_2_5_group": ["eye_squint_2", "eye_squint_5"],
    "eye_squint_3_6_group": ["eye_squint_3", "eye_squint_6"],
    "eye_sqz_1_4_group": ["eye_sqz_1", "eye_sqz_4"],
    "eye_sqz_2_5_group": ["eye_sqz_2", "eye_sqz_5"],
    "eye_sqz_3_6_group": ["eye_sqz_3", "eye_sqz_6"],
    "eye_sqz_blink_1_2_group": ["eye_sqz_blink_1", "eye_sqz_blink_2"],
    "frown_1_3_group": ["frown_1", "frown_3"],
    "frown_2_4_group": ["frown_2", "frown_4"],
    "funnel_1_4_group": ["funnel_1", "funnel_4"],
    "funnel_2_5_group": ["funnel_2", "funnel_5"],
    "funnel_3_6_group": ["funnel_3", "funnel_6"],
    "funnel_close_1_2_group": ["funnel_close_1", "funnel_close_2"],
    "funnel_wide_1_3_group": ["funnel_wide_1", "funnel_wide_3"],
    "funnel_wide_2_4_group": ["funnel_wide_2", "funnel_wide_4"],
    "jaw_open_1_6_group": ["jaw_open_1", "jaw_open_6"],
    "jaw_open_2_7_group": ["jaw_open_2", "jaw_open_7"],
    "jaw_open_3_8_group": ["jaw_open_3", "jaw_open_8"],
    "jaw_open_4_9_group": ["jaw_open_4", "jaw_open_9"],
    "jaw_open_5_10_group": ["jaw_open_5", "jaw_open_10"],
    "lip_in_1_4_group": ["lip_in_1", "lip_in_4"],
    "lip_in_2_5_group": ["lip_in_2", "lip_in_5"],
    "lip_in_3_6_group": ["lip_in_3", "lip_in_6"],
    "lip_lock_back_1_2_group": ["lip_lock_back_1", "lip_lock_back_2"],
    "lip_lock_fwd_1_2_group": ["lip_lock_fwd_1", "lip_lock_fwd_2"],
    "lip_lock_l_1_2_group": ["lip_lock_l_1", "lip_lock_l_2"],
    "lip_lock_open_1_2_group": ["lip_lock_open_1", "lip_lock_open_2"],
    "lip_lock_r_1_2_group": ["lip_lock_r_1", "lip_lock_r_2"],
    "lwr_lid_dn_1_2_group": ["lwr_lid_dn_1", "lwr_lid_dn_2"],
    "lwr_lid_up_1_2_group": ["lwr_lid_up_1", "lwr_lid_up_2"],
    "lwr_lip_dn_1_3_group": ["lwr_lip_dn_1", "lwr_lip_dn_3"],
    "lwr_lip_dn_2_4_group": ["lwr_lip_dn_2", "lwr_lip_dn_4"],
    "lwr_lip_l_1_3_group": ["lwr_lip_l_1", "lwr_lip_l_3"],
    "lwr_lip_l_2_4_group": ["lwr_lip_l_2", "lwr_lip_l_4"],
    "lwr_lip_r_1_3_group": ["lwr_lip_r_1", "lwr_lip_r_3"],
    "lwr_lip_r_2_4_group": ["lwr_lip_r_2", "lwr_lip_r_4"],
    "neck_tension_1_2_group": ["neck_tension_1", "neck_tension_2"],
    "nl_deep_1_5_group": ["nl_deep_1", "nl_deep_5"],
    "nl_deep_2_6_group": ["nl_deep_2", "nl_deep_6"],
    "nl_deep_3_7_group": ["nl_deep_3", "nl_deep_7"],
    "nl_deep_4_8_group": ["nl_deep_4", "nl_deep_8"],
    "o_1_4_group": ["o_1", "o_4"],
    "o_2_5_group": ["o_2", "o_5"],
    "o_3_6_group": ["o_3", "o_6"],
    "o_wide_1_3_group": ["o_wide_1", "o_wide_3"],
    "o_wide_2_4_group": ["o_wide_2", "o_wide_4"],
    "press_1_4_group": ["press_1", "press_4"],
    "press_2_5_group": ["press_2", "press_5"],
    "press_3_6_group": ["press_3", "press_6"],
    "pucker_1_4_group": ["pucker_1", "pucker_4"],
    "pucker_2_5_group": ["pucker_2", "pucker_5"],
    "pucker_3_6_group": ["pucker_3", "pucker_6"],
    "puff_1_2_group": ["puff_1", "puff_2"],
    "puff_dn_1_2_group": ["puff_dn_1", "puff_dn_2"],
    "puff_up_1_2_group": ["puff_up_1", "puff_up_2"],
    "smile_1_6_group": ["smile_1", "smile_6"],
    "smile_2_7_group": ["smile_2", "smile_7"],
    "smile_3_8_group": ["smile_3", "smile_8"],
    "smile_4_9_group": ["smile_4", "smile_9"],
    "smile_5_10_group": ["smile_5", "smile_10"],
    "smile_close_1_2_group": ["smile_close_1", "smile_close_2"],
    "smile_drop_1_2_group": ["smile_drop_1", "smile_drop_2"],
    "sneer_1_5_group": ["sneer_1", "sneer_5"],
    "sneer_2_6_group": ["sneer_2", "sneer_6"],
    "sneer_3_7_group": ["sneer_3", "sneer_7"],
    "sneer_4_8_group": ["sneer_4", "sneer_8"],
    "sneer_close_1_2_group": ["sneer_close_1", "sneer_close_2"],
    "sticky_lips_1_6_group": ["sticky_lips_1", "sticky_lips_6"],
    "sticky_lips_2_7_group": ["sticky_lips_2", "sticky_lips_7"],
    "sticky_lips_3_8_group": ["sticky_lips_3", "sticky_lips_8"],
    "sticky_lips_4_9_group": ["sticky_lips_4", "sticky_lips_9"],
    "sticky_lips_5_10_group": ["sticky_lips_5", "sticky_lips_10"],
    "stretch_1_3_group": ["stretch_1", "stretch_3"],
    "stretch_2_4_group": ["stretch_2", "stretch_4"],
    "stretch_close_1_2_group": ["stretch_close_1", "stretch_close_2"],
    "suck_1_2_group": ["suck_1", "suck_2"],
    "swallow_1_3_group": ["swallow_1", "swallow_3"],
    "swallow_2_4_group": ["swallow_2", "swallow_4"],
    "tension_1_4_group": ["tension_1", "tension_4"],
    "tension_2_5_group": ["tension_2", "tension_5"],
    "tension_3_6_group": ["tension_3", "tension_6"],
    "tight_1_2_group": ["tight_1", "tight_2"],
    "upr_lid_dn_1_2_group": ["upr_lid_dn_1", "upr_lid_dn_2"],
    "upr_lid_up_1_2_group": ["upr_lid_up_1", "upr_lid_up_2"],
    "upr_lip_dn_1_4_group": ["upr_lip_dn_1", "upr_lip_dn_4"],
    "upr_lip_dn_2_5_group": ["upr_lip_dn_2", "upr_lip_dn_5"],
    "upr_lip_dn_3_6_group": ["upr_lip_dn_3", "upr_lip_dn_6"],
    "wide_1_2_group": ["wide_1", "wide_2"]
}


def export_abc_file_from_bs_file(bs_file, to_abc_file):
    """
    Export abc file from the input bs file.
    Args:
        bs_file: the input bs file.
        to_abc_file: the output abc file.

    Returns: None.

    """
    with open(bs_file) as fin:
        data = json.load(fin)
        key_value = "value"
        if "animations" in data:
            data = data["animations"][0]
            key_value = "values"
        for i, clip in enumerate(data["animClip"]):
            time_ = clip["time"]
            h, m, s, c = map(float, time_.split(":"))
            time_ = h * 60. * 60. + m * 60. + s + c / float(100)
            print("%s: %.2f" % (os.path.basename(bs_file), time_))

            cmds.currentTime(i)
            for k, v in clip[key_value].items():
                if k in ALL_BS_KEYS:
                    cmds.setAttr("{}.{}".format(FACE_BS_PREFIX, k), v)
                    cmds.setKeyframe("{}.{}".format(FACE_BS_PREFIX, k))
                    if k == "jaw_open_1":
                        cmds.setAttr("{}.{}".format(TEETH_BS_PREFIX, k), v)
                        cmds.setKeyframe("{}.{}".format(TEETH_BS_PREFIX, k))

        # Export.
        n = len(data["animClip"])
        cmd = "AbcExport -j \"-frameRange 0 %d -step 1 -dataFormat ogawa -root AI_TD_01_Head01 -file %s\"" % (
            n - 1, to_abc_file)
        print(cmd)
        mel.eval(cmd)


def demo_for_exporting_abc_file_from_bs_file():
    """
    Demo for exporting abc file from bs file
    """
    export_abc_file_from_bs_file("D:/bs_files/001_0040_00A_001.cut.json",
                                 "D:/abc_files/001_0040_00A_001.cut.abc")


def export_obj_files_from_bs(to_dir):
    """
    Export bs to obj files.
    Args:
        to_dir: the output dir.

    Returns: None.

    """
    # 0. Neutral pose.
    curr_time = 0
    for k in ALL_BS_KEYS:
        v = 0.
        cmds.setAttr("{}.{}".format(FACE_BS_PREFIX, k), v)
        cmds.setKeyframe("{}.{}".format(FACE_BS_PREFIX, k))
    cmd = "polyTriangulate -ch 1 AI_TD_01_Head01;"
    mel.eval(cmd)
    cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                  -typ "OBJexport" -pr -es " {}/{}.obj";""".format(to_dir, "neutral")
    mel.eval(cmd)

    # 1. For every bs.
    for curr_k in ALL_BS_KEYS:
        print(curr_k)
        curr_time += 1
        cmds.currentTime(curr_time)
        for k in ALL_BS_KEYS:
            v = 1.0 if curr_k == k else 0.
            cmds.setAttr("{}.{}".format(FACE_BS_PREFIX, k), v)
            cmds.setKeyframe("{}.{}".format(FACE_BS_PREFIX, k))

        cmd = "polyTriangulate -ch 1 AI_TD_01_Head01;"
        mel.eval(cmd)
        cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                      -typ "OBJexport" -pr -es " {}/{}.obj";""".format(to_dir, curr_k)
        mel.eval(cmd)

    # 2. For group bs.
    for g_k, ks in BS_GROUP_NAME_TO_KEYS.items():
        print(g_k)
        cmds.currentTime(curr_time)
        for k in ALL_BS_KEYS:
            v = 1.0 if k in ks else 0.
            cmds.setAttr("{}.{}".format(FACE_BS_PREFIX, k), v)
            cmds.setKeyframe("{}.{}".format(FACE_BS_PREFIX, k))

        cmd = "polyTriangulate -ch 1 AI_TD_01_Head01;"
        mel.eval(cmd)
        cmd = """file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" 
                        -typ "OBJexport" -pr -es " {}/{}.obj";""".format(to_dir, g_k)
        mel.eval(cmd)
        curr_time += 1


def demo_for_exporting_obj_files_from_bs():
    """
    Demo for exporting_bs_to_obj_files

    """
    export_obj_files_from_bs("bs_objs")


def export_mesh_from_abc_file(abc_file, to_mesh_file):
    """
    Export mesh form abc file.
    Args:
        abc_file: the input abc file.
        to_mesh_file: the output mesh file.

    Returns: None.

    """
    archive = cask.Archive(abc_file)

    def dfs(obj, path, ans):
        if str(obj.type()) == "PolyMesh":
            ans.append("/".join(path))
            return
        for child in obj.children.values():
            dfs(child, path + [child.name], ans)

    ans = []
    dfs(archive.top, [], ans)
    poly_mesh_path = ans[0]

    mesh = archive.top.children[poly_mesh_path]
    print("poly_mesh_path", poly_mesh_path)
    print("number of samples:", len(mesh.samples))

    mesh_numpy = []
    for sample in tqdm.tqdm(mesh.samples):
        curr_mesh = []
        for position in sample.getPositions():
            curr_mesh.append([position.x, position.y, position.z])
        mesh_numpy.append(curr_mesh)
    mesh_numpy = np.array(mesh_numpy)

    np.save(to_mesh_file, mesh_numpy)


def demo_for_exporting_mesh_from_abc_file():
    """
    Demo.
    """
    dataset_dir = "/root/blanc/original_force/alembic_cache_data_baidu/"
    to_dir = "/root/blanc/original_force/mesh_data"
    convert_log_file = "/root/blanc/original_force/alembic_cache_data_baidu/mesh_convert.log"
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    with open(convert_log_file, "w") as fout:
        for abc_file in glob.glob("{}/*.abc".format(dataset_dir)):
            try:
                filename = os.path.basename(abc_file)  # "001_0040_0BH_001.cut.abc"
                filename = filename.split(".", 1)[0] + "_mesh" + "." \
                           + filename.split(".", 1)[1].replace("abc", "npy")
                to_mesh_file = "{}/{}".format(to_dir, filename)
                print(abc_file, "-->", to_mesh_file)
                if os.path.exists(to_mesh_file):
                    continue
                export_mesh_from_abc_file(abc_file, to_mesh_file)
            except Exception as e:
                print(e)
                fout.write("{}: failed\n".format(abc_file))

