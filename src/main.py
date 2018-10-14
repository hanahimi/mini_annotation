#-*-coding:UTF-8
'''
Created on 2018年9月27日-下午10:28:37
author: Gary-W
'''
import os
from landmark.points_marker import PointsMarker
from landmark.bev_points_marker import BevPointsMarker
from landmark.veh_pose_marker import VehPoseMarker


def main():
    print("1: PointsMarker")
    print("2: BevPointsMarker")
    print("3: VehPoseMarker")

    n1 = raw_input("input tools id:")
    if n1 == "1":
        imgs_dir = raw_input("input images dir:")
        if os.path.exists(imgs_dir):
            pm = PointsMarker(imgs_dir)
            pm.mainloop()
    
    elif n1 == "2":
        imgs_dir = raw_input("input images dir:")
        if os.path.exists(imgs_dir):
            veh_loc_file = raw_input("input loc file(Enter if no file):")
            if not os.path.exists(veh_loc_file):
                veh_loc_file = None
            vc_img_x = int(raw_input("input car center X of bev:"))
            vc_img_y = int(raw_input("input car center Y of bev:"))
            ppmmx = int(raw_input("input ppmmx of bev:"))
            ppmmy = int(raw_input("input ppmmy of bev:"))
            bev_config = {"vc_img_x":vc_img_x, "vc_img_y":vc_img_y, "ppmmx":ppmmx, "ppmmy":ppmmy}
            pm = BevPointsMarker(imgs_dir, bev_config, veh_loc_file)
            pm.mainloop()
    
    elif n1 == "3":
        imgs_dir = raw_input("input images dir:")
        if os.path.exists(imgs_dir):
            landmark_file = raw_input("input landmark file:")
            if os.path.exists(landmark_file):
                vc_img_x = int(raw_input("input car center X of bev:"))
                vc_img_y = int(raw_input("input car center Y of bev:"))
                ppmmx = int(raw_input("input ppmmx of bev:"))
                ppmmy = int(raw_input("input ppmmy of bev:"))
                bev_config = {"vc_img_x":vc_img_x, "vc_img_y":vc_img_y, "ppmmx":ppmmx, "ppmmy":ppmmy}
                pm = VehPoseMarker(imgs_dir, bev_config, landmark_file)
                pm.mainloop()
            
            
if __name__=="__main__":
    pass
    main()

