#-*-coding:UTF-8
'''
Created on 2018-8-14
@author: mipapapa

create label points on BEV dataset

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
from utils.comm_struct import BevPointData
from utils.cv_marker import CvMarker
from utils.log_parser import get_log_table
from landmark.points_marker import PointsMarker

class BevPointsMarker(PointsMarker):
    def __init__(self, imgs_dir, bev_config):
        PointsMarker.__init__(self, imgs_dir)
        self.bev_config = bev_config

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
                self.cur_points.append(new_point)
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(self.cur_point_id)+":"+self.type_str+"\n (%2.1f,%2.1f)" % (new_point.veh_x, new_point.veh_y))
                print("Page:%d - %d  P = (%d, %d)" % (self.cur_img_idx, new_point.id, x, y))
                self.cur_point_id += 1
                    
            # detect plam area
            if (self.view_width < x < self.view_width+self.plam.w) and (0 < y < self.win_H):
                strKey =  self.plam.getKey(x, y)
                if strKey != 0:
                    if strKey == "Enter":
                        self.try_save_cur_labeling()
                    else:
                        self.plam.key_log.append(strKey)
                        self.plam.updateDisplayer()
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
            cv2.imshow(self.win_title, self.window)
            key = cv2.waitKey(10) & 0xFF
            if 0 == self.keyboard_respond(key):
                break
    
def main():
    pass
    imgs_dir = r"D:\bev"
    bev_config = {"vc_img_x":256, "vc_img_y":312, "ppmmx":20, "ppmmy":20}
    pm = BevPointsMarker(imgs_dir, bev_config)
    pm.mainloop()
    
if __name__=="__main__":
    pass
    main()

