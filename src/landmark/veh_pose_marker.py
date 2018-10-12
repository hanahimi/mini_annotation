#-*-coding:UTF-8
'''
Created on 2018-10-9--3:43:41 pm
author: Gary-W

1 given coinstant landmark of dataset and bev setting
2 mark 2 points on an bev image(I)
3 auto compute the pose(xm, ym, yawr) of vehicale of img I
4 this pose can treat as ground true of location

# Key board event:
A: load last image
D: load next image
R: remove current annotation
F: save current annotation
1~9: select loading step

# mouse event:
1 click mouse-1 on left image: add new point annotation
2 click mouse-1 on right plam: entry point type(str)
    [X]: clear all charactors
    [<-]: clear last charactor
    [Enter]: save current annotation
    [others]: add new charactor
'''
import cv2
from utils.comm_struct import BevPointData, PoseData
from utils.cv_marker import CvMarker
from utils.log_parser import get_log_table
from landmark.points_marker import PointsMarker
from math import cos, sin

class VehPoseMarker(PointsMarker):
    def __init__(self, imgs_dir, bev_config, landmark_file):
        PointsMarker.__init__(self, imgs_dir)
        self.bev_config = bev_config
        self.load_landmark_data(landmark_file)
    
    def load_loc_data(self, veh_loc_file):
        self.loc_data = None
        try:
            loc_data_log = get_log_table(veh_loc_file)
            self.loc_data = {}
            for i in range(len(loc_data_log)):
                new_pose = PoseData()
                new_pose.time = loc_data_log[i].table["time"]
                new_pose.Xm = loc_data_log[i].table["Xm"]
                new_pose.Ym = loc_data_log[i].table["Ym"]
                new_pose.Yawr = loc_data_log[i].table["Yawr"]
                self.loc_data[new_pose.time] = new_pose
            print("read pose data, save veh coordinate and world coordinate")

        except:
            self.loc_data = None
            print("no valid pose data, only save veh coordinate")
if __name__=="__main__":
    pass

