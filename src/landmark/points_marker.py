#-*-coding:UTF-8
'''
Created on 2018-8-14
@author: mipapapa

create label points on image dataset

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
import numpy as np
import os
from gui.ctrl_plam import CtrlPlam
from utils.comm_struct import ImgData,PointData
from utils.cv_marker import CvMarker
from utils.dataio import get_walkfilelist
from utils.log_parser import get_log_table

class PointsMarker:
    def __init__(self, imgs_dir):
        self.win_title = "points_marker"
        self.root_dir = imgs_dir
        
        self.cur_img_idx = 0
        self.type_str = "X"
        self.init_images_dir(imgs_dir)
        self.build_window()
        
        self.step = 1
        
    def reset_status(self):
        self.lock_flag = False
        self.cur_img =cv2.imread(self.dataset[self.cur_img_idx].img_path)
        self.cur_label_file = self.dataset[self.cur_img_idx].img_path[:-4]+".txt"
        self.cur_point_id = 0
        self.cur_points = []
        self.try_load_cur_labeling()
        
    def init_images_dir(self, imgs_dir):
        # build image dataset (wrap an img file as ImgData)
        imgpath_lst, _ = get_walkfilelist(imgs_dir, ".jpg", ".png", ".bmp")
        self.dataset = [ImgData(img_path) for img_path in imgpath_lst]
        self.nData = len(self.dataset)

        self.reset_status()
        
        self.view_heigth = self.cur_img.shape[0]
        self.view_width = self.cur_img.shape[1]
        
    def build_window(self):
        cv2.namedWindow(self.win_title)
        cv2.setMouseCallback(self.win_title,self.mouse_add_point)

        self.mouse_cnt_status = 0
        self.plam = CtrlPlam(self.view_width, 0)
        
        self.window = np.zeros((max(self.view_heigth, self.plam.h),
                                self.view_width + self.plam.w, 3), np.uint8)
        
        self.win_H = self.window.shape[0]
        self.win_W = self.window.shape[1]
        
    def mouse_add_point(self,event, x, y, flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if x < self.view_width and y < self.view_heigth:
                self.lock_flag = True
                
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(self.cur_point_id)+":"+self.type_str)
                new_point = PointData()
                new_point.x, new_point.y, new_point.id = x, y, self.cur_point_id
                new_point.img_id = self.dataset[self.cur_img_idx].img_id
                new_point.type = self.type_str
                self.cur_points.append(new_point)
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

    def try_save_cur_labeling(self):
        self.cur_label_file = self.dataset[self.cur_img_idx].img_path[:-4]+".txt"
        with open(self.cur_label_file,"a") as f:
            for point in self.cur_points:
                f.write(str(point)+"\n")

        print("save %d new points" % (len(self.cur_points)))
    
    def try_remove_cur_labeling(self):
        try:
            os.remove(self.cur_label_file)
            self.reset_status()
        except:
            print("remove current labels err")
    
    def try_load_cur_labeling(self):
        try:
            tmplabels = get_log_table(self.cur_label_file)
            for la_data in tmplabels:
                x, y = la_data.table["x"], la_data.table["y"]
                tmp_point_id = la_data.table["id"]
                tmp_type_str = la_data.table["type"]
                CvMarker.draw_cross_marker(self.cur_img, x, y,str(tmp_point_id)+":"+tmp_type_str)
                self.cur_point_id = tmp_point_id + 1
        except:
            pass
        

    def keyboard_respond(self, key):
        if key==27:
            return 0
        
        if key==ord('a') or key==ord('A'):
            if self.cur_img_idx >= self.step: 
                self.cur_img_idx -= self.step
            self.reset_status()
            
        if key==ord('d') or key==ord('D'):
            if self.cur_img_idx < self.nData - self.step: 
                self.cur_img_idx += self.step
            self.reset_status()
        
        for i in range(1,10,1):
            if key==ord(str(i)):
                self.step = i
                print("reading step = %d" % (self.step))
        
        if key==ord('f') or key==ord('F'):
            self.try_save_cur_labeling()

        if key==ord('r') or key==ord('R'):
            self.try_remove_cur_labeling()
            
    def mainloop(self):
        while (1):
            self.window[:self.view_heigth, :self.view_width,:] = self.cur_img[:]
            self.window[:self.plam.h, self.view_width:self.view_width+self.plam.w,:] = self.plam.bg[:]
            cv2.imshow(self.win_title, self.window)
            key = cv2.waitKey(10) & 0xFF
            if 0 == self.keyboard_respond(key):
                break
    
def main():
    pass
    imgs_dir = r"D:\bev"
    pm = PointsMarker(imgs_dir)
    pm.mainloop()
    
if __name__=="__main__":
    pass
    main()

