#-*-coding:UTF-8
'''
Created on 2018-8-14
@author: mipapapa

create label points on BEV dataset
given bev info:(car center x, car center y, ppmmx, ppmmy)
if veh_loc_file is provided, this tool will also compute the coords of label points

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

class BevPointsMarker(PointsMarker):
    def __init__(self, imgs_dir, bev_config, veh_loc_file=None):
        PointsMarker.__init__(self, imgs_dir)
        self.bev_config = bev_config
        self.load_loc_data(veh_loc_file)
        
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
                
                print("Page:%d - %d  P = (%d, %d)" % (self.cur_img_idx, new_point.id, x, y))
                if self.loc_data:
                    cur_time = int(new_point.img_id)
                    try:
                        print(cur_time)
                        bev_pose = self.loc_data[cur_time]
                        cosa = cos(bev_pose.Yawr)
                        sina = sin(bev_pose.Yawr)
                        new_point.world_x = new_point.veh_y * cosa + new_point.veh_x * sina + bev_pose.Xm
                        new_point.world_y = new_point.veh_x * cosa - new_point.veh_y * sina + bev_pose.Ym
                        print("  time:%09d X:%2.4f Y:%2.4f" % (cur_time, new_point.world_x, new_point.world_y))
                    except:
                        print("can not fine match pose data of time:%09d" % (cur_time))
                        
                self.cur_points.append(new_point)
                
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(self.cur_point_id)+":"+self.type_str+"\n (%2.1f,%2.1f)" % (new_point.veh_x, new_point.veh_y))

                self.cur_point_id += 1
                self.cmd_win.clear(1)
                msg = "%s\n%d %s P=(%d, %d)\nVeh: X: %2.2f Y: %2.2f\n" \
                    % (new_point.img_id, 
                       new_point.id, new_point.type, x, y,
                       new_point.veh_x, new_point.veh_y)
                    
                if new_point.world_x and new_point.world_y:
                    msg += "Wld: X: %2.2f Y: %2.2f" % (new_point.world_x, new_point.world_y)

                self.cmd_win.update_tab(msg)
                self.cmd_win.update_displayer()
                
                    
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
    
    def mainloop(self):
        while (1):
            CvMarker.draw_cross(self.cur_img, self.bev_config["vc_img_x"], self.bev_config["vc_img_y"])
            self.window[:self.view_heigth, :self.view_width,:] = self.cur_img[:]
            self.window[:self.plam.h, self.view_width:self.view_width+self.plam.w,:] = self.plam.bg[:]
            self.window[self.plam.h+10:self.plam.h+10+self.cmd_win.h, self.view_width+20:self.view_width+20+self.cmd_win.w,:] = self.cmd_win.bg[:]
                
            cv2.imshow(self.win_title, self.window)
            key = cv2.waitKey(10) & 0xFF
            if 0 == self.keyboard_respond(key):
                break
    
def main():
    pass
    imgs_dir = r"D:\bev_512_WH\landmarks\20180717_203642_2\bev"
    veh_loc_file = r"D:\bev_512_WH\landmarks\20180717_203642_2\can_ekf.txt"
    bev_config = {"vc_img_x":256, "vc_img_y":320, "ppmmx":20, "ppmmy":20}
    pm = BevPointsMarker(imgs_dir, bev_config, veh_loc_file)
    pm.mainloop()
    
if __name__=="__main__":
    pass
    main()

