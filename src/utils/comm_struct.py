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

class BevPointData(PointData):
    def __init__(self):
        PointData.__init__(self)
        self.veh_x = 0
        self.veh_y = 0
        
        self.world_x = None
        self.world_y = None
    
    def __repr__(self):
        if self.world_x or self.world_y:
            log = "**Point*Img:'%s' type:'%s' id:%d x:%d y:%d veh_x:%2.4f veh_y:%2.4f world_x:%2.4f world_y:%2.4f#" \
                    % (str(self.img_id), self.type, self.id, self.x, self.y, 
                       self.veh_x, self.veh_y, self.world_x, self.world_y)
        else:
            log = "**Point*Img:'%s' type:'%s' id:%d x:%d y:%d veh_x:%2.4f veh_y:%2.4f#" \
                    % (str(self.img_id), self.type, self.id, self.x, self.y, self.veh_x, self.veh_y)
            
        return log

class PoseData:
    def __init__(self):
        self.Xm = 0
        self.Ym = 0
        self.Yawr = 0
        self.time =  0
        
    def __repr__(self):
        log = "**Loc*time:%09d Xm:%f Ym:%f Yawr:%f#" % (self.time, self.Xm, self.Ym, self.Yawr)
        return log    

if __name__=="__main__":
    pass

