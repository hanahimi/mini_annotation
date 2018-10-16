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
M: merge all annotation text file and coumpute vehicle pose of labeled time
   create "gt_pose_marked.txt" file
I: display computed veh loc in matplot

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
import numpy as np
import numpy.linalg as LA
from utils.dataio import get_walkfilelist
import os

class VehPoseMarker(PointsMarker):
    def __init__(self, imgs_dir, bev_config, landmark_file):
        PointsMarker.__init__(self, imgs_dir)
        self.bev_config = bev_config
        self.load_landmark_data(landmark_file)
    
    def load_landmark_data(self, landmark_file):
        self.landmark_data = None
        try:
            lmd_data_log = get_log_table(landmark_file)
            self.landmark_data = {}
            for i in range(len(lmd_data_log)):
                new_point = BevPointData()
                new_point.load_table(lmd_data_log[i].table)
                landmark_id = new_point.type+"_"+str(new_point.id)
                self.landmark_data[landmark_id] = new_point
        except:
            print("no valid landmark data")
    
    def mouse_add_point(self,event, x, y, flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if x < self.view_width and y < self.view_heigth:
                self.lock_flag = True
                new_point = BevPointData()
                new_point.x, new_point.y, new_point.id = x, y, self.cur_point_id
                new_point.img_id = self.dataset[self.cur_img_idx].img_id
                new_point.type = self.type_str
                new_point.veh_x = 1.0 * (self.bev_config["vc_img_y"] - new_point.y) * (self.bev_config["ppmmy"]*0.001)
                new_point.veh_y = 1.0 * (new_point.x - self.bev_config["vc_img_x"]) * (self.bev_config["ppmmx"]*0.001)
                
                new_landmark_id = new_point.type+"_"+str(new_point.id)

                
                if new_landmark_id in self.landmark_data:
                    match_landmark = self.landmark_data[new_landmark_id]
                    new_point.world_x = match_landmark.world_x
                    new_point.world_y = match_landmark.world_y
                    self.cur_points.append(new_point)
                    print("Page:%d - %d  lm:%s)" % (self.cur_img_idx, new_point.id, new_landmark_id))
                
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(self.cur_point_id)+":"+self.type_str+"\n (%2.1f,%2.1f)" % (new_point.veh_x, new_point.veh_y))
                self.cur_point_id += 1
                
            # detect plam area
            if (self.view_width < x < self.view_width+self.plam.w) and (0 < y < self.win_H):
                strKey =  self.plam.getKey(x, y)
                if strKey != 0:
                    if strKey == "Enter":
                        self.try_save_cur_labeling()
                    else:
                        self.plam.key_log.append(strKey)
                        self.plam.update_displayer()
                        self.type_str = "".join(self.plam.key_log)
                else:
                    # plam set clear
                    if len(self.plam.key_log) == 0:
                        self.type_str = "X"
                    else:
                        self.type_str = "".join(self.plam.key_log)
    
    def try_load_cur_labeling(self):
        try:
            tmplabels = get_log_table(self.cur_label_file)
            for la_data in tmplabels:
                x, y = la_data.table["x"], la_data.table["y"]
                tmp_point_id = la_data.table["id"]
                tmp_type_str = la_data.table["type"]
                tmp_veh_x, tmp_veh_y = la_data.table["veh_x"], la_data.table["veh_y"]
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(tmp_point_id)+":"+tmp_type_str+"\n (%2.1f,%2.1f)" % (tmp_veh_x, tmp_veh_y))
                self.cur_point_id = tmp_point_id + 1
        except:
            pass
    
    def  __compute_marked_pose(self, imgs_dir):
        label_lst, _ = get_walkfilelist(imgs_dir, ".txt")
        
        veh_pose_lst = []
        for i in range(len(label_lst)):
            try:
                label_data = get_log_table(label_lst[i])
                load_points = []
                for k in range(len(label_data)):
                    if "Point" == label_data[k].name:
                        new_point = BevPointData()
                        new_point.load_table(label_data[k].table)
                        load_points.append(new_point)
                
                if len(load_points) >= 2:
                    # compute veh pose in world with two landmark
                    vx0, vy0 = load_points[0].veh_x, load_points[0].veh_y
                    wx0, wy0 = load_points[0].world_x, load_points[0].world_y
                    vx1, vy1 = load_points[1].veh_x, load_points[1].veh_y
                    wx1, wy1 = load_points[1].world_x, load_points[1].world_y
                    
                    h = np.array([[vy0, vx0, 1.0, 0.0],
                                  [vx0,-vy0, 0.0, 1.0],
                                  [vy1, vx1, 1.0, 0.0],
                                  [vx1,-vy1, 0.0, 1.0]])
                    H = np.matrix(h)
                    Hinv = LA.inv(H)
                    WP = np.matrix([wx0,wy0,wx1,wy1]).T
                    WV = Hinv * WP
                    n = np.sqrt(WV[0,0]**2 + WV[1,0]**2)
                    WV[0,0] /= n
                    WV[1,0] /= n

                    veh_pose = PoseData()
                    veh_pose.time = int(load_points[0].img_id)
                    veh_pose.Xm = WV[2,0]
                    veh_pose.Ym = WV[3,0]
                    veh_pose.Yawr = np.arccos(WV[0,0])
                    if WV[1,0] < 0: 
                        veh_pose.Yawr *= -1
                    veh_pose_lst.append(veh_pose)
            except:
                pass
            
        if veh_pose_lst:
            print("%d pose load" % len(veh_pose_lst))
            gt_pose_file = os.path.join(os.path.split(imgs_dir)[0],"gt_pose_marked.txt")
            with open(gt_pose_file,"w") as f:
                for pose in veh_pose_lst:
                    f.write(str(pose)+"\n")
    
    def display_poses(self, imgs_dir):
        try:
            from matplotlib import pyplot as plt
            pose_file = os.path.join(os.path.split(imgs_dir)[0],"gt_pose_marked.txt")
            poses = get_log_table(pose_file)
            plt.figure()
            X,Y,dX,dY = [],[],[],[]
            for i in range(len(poses)):
                pose_data = poses[i].table
                X.append(pose_data["Xm"])
                Y.append(pose_data["Ym"])
                dX.append(np.sin(pose_data["Yawr"]))
                dY.append(np.cos(pose_data["Yawr"]))
            plt.plot(X, Y, ".")
            plt.show()
        
        except:
            pass
    
    def keyboard_respond(self, key):
        res = PointsMarker.keyboard_respond(self, key)
        
        if key==ord('m') or key==ord('M'):
            print("Compute Landmarks pose")
            self.__compute_marked_pose(self.imgs_dir)
        
        if key==ord('i') or key==ord('I'):
            print("Display Pose")
            self.display_poses(self.imgs_dir)

        return res
            
def main():
    pass
    imgs_dir = r"D:\VPS_GT\bev_512_WH\test_raw_data\20180717_231042\bev"
    landmark_file = r"D:\VPS_GT\bev_512_WH\landmarks\20180717_203642_2\landmarks.txt"
    bev_config = {"vc_img_x":256, "vc_img_y":320, "ppmmx":20, "ppmmy":20}
    pm = VehPoseMarker(imgs_dir, bev_config, landmark_file)
    pm.mainloop()
    
if __name__=="__main__":
    pass
    main()



