#-*-coding:UTF-8
'''
Created on 2018-10-8 5:11:36 pm
author: Gary-W
'''
import os

class ImgData:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img_id = os.path.split(self.img_path)[-1][:-4]
        
class PointData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.id = 0
        self.img_id = "0"
        self.type = "unknow"
        
    def __repr__(self):
        log = "**Point*Img:'%s' type:'%s' id:%d x:%d y:%d#" % (str(self.img_id), self.type, self.id, self.x, self.y)
        return log


if __name__=="__main__":
    pass
