#-*-coding:UTF-8
'''
Created on 2018-10-8--5:11:36 pm
author: Gary-W
'''
import cv2

class CvMarker:
    @staticmethod
    def draw_cross_marker(src_img,x,y,_id):
        _id = str(_id)
        l = 2
        cv2.line(src_img, (x,y),(x+l,y), (100,200,100),1)
        cv2.line(src_img, (x,y),(x-l,y), (100,200,100),1)
        cv2.line(src_img, (x,y),(x,y+l), (100,200,100),1)
        cv2.line(src_img, (x,y),(x,y-l), (100,200,100),1)
        id_lines = _id.split("\n")
        for i in range(len(id_lines)):
            cv2.putText(src_img, "%s"%id_lines[i], (x+5,y+10*i), cv2.FONT_HERSHEY_PLAIN, 0.8,(100,200,100),thickness=1)
    
    @staticmethod
    def draw_label(src_img,x,y, strlabel):
        l = 2
        cv2.line(src_img, (x,y),(x+l,y), (100,200,100),1)
        cv2.line(src_img, (x,y),(x-l,y), (100,200,100),1)
        cv2.line(src_img, (x,y),(x,y+l), (100,200,100),1)
        cv2.line(src_img, (x,y),(x,y-l), (100,200,100),1)
        cv2.putText(src_img, strlabel, (x+5,y), cv2.FONT_HERSHEY_PLAIN, 1.0,(100,200,100),thickness=1)
            
    @staticmethod
    def print_marker(src_img,x,y,pldx,pldy):
        cv2.putText(src_img, "rX: %d" % pldx, (x+20,y-6), cv2.FONT_HERSHEY_PLAIN, 0.8,(200,200,100),thickness=1)
        cv2.putText(src_img, "rY: %d" % pldy, (x+20,y+6), cv2.FONT_HERSHEY_PLAIN, 0.8,(200,200,100),thickness=1)
    
    @staticmethod
    def draw_cross(src_img, img_col,img_row):
        h,w,_ = src_img.shape
        cv2.line(src_img, (0, img_row),(w, img_row),(100,100,200),1)
        cv2.line(src_img, (img_col, 0),(img_col, h),(100,100,200),1)


