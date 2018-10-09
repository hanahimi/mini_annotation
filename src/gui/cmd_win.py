#-*-coding:UTF-8
'''
Created on 2018-10-9--2:26:53 pm
author: Gary-W
'''
import cv2

def script_path():
    import inspect, os
    this_file = inspect.getfile(inspect.currentframe())
    return os.path.abspath(os.path.dirname(this_file))

class CmdWindow:
    def __init__(self, x_offset=0, y_offset=0):
        spath = script_path()
        self.bg = cv2.imread(spath+"/cmd_table.jpg")
        self.h = self.bg.shape[0]
        self.w = self.bg.shape[1]
        
        self.msg_log = {1:None, 2:None, 3:None}
        
        self.x_offset = x_offset
        self.y_offset = y_offset
        
        self.cur_tab = 1
    
    def update_tab(self, msg, tab_id=1):
        try:
            assert tab_id in [1,2,3]
            self.msg_log[tab_id] = msg
        except:
            print("invalid input")
    
    def switch_tab(self, tab_id):
        try:
            assert tab_id in [1,2,3]
            self.update_displayer()
        except:
            print("invalid input")
        
    def update_displayer(self):
        for i in [1,2,3]:
            if self.cur_tab == i and self.msg_log[i]:
                cmd_lines = self.msg_log[i].split("\n")
                if len(cmd_lines) > 4:
                    cmd_lines = cmd_lines[:4]
                for i in range(len(cmd_lines)):
                    cv2.putText(self.bg, "%s" % cmd_lines[i][:24], (15,50+20*i), cv2.FONT_HERSHEY_DUPLEX, 0.4,(96,209,160),thickness=1)
                break
    
    def clear(self,tab=None):
        if tab == 1 or tab == 2 or tab == 3:
            self.msg_log[tab] = None
        else:
            self.msg_log = {1:None, 2:None, 3:None}
        
        self.bg[34:120,10:260,:] = 0
    
    def getKey(self,x, y):
        x -= self.x_offset
        y -= self.y_offset
        if (11 < x < 90) and (9 < y < 28):
            return 1
        elif (97 < x < 175) and (9 < y < 28):
            return 2
        elif (182 < x < 27) and (9 < y < 28):
            return 3
        else:
            return 0
        
if __name__=="__main__":
    c = CmdWindow(0,0)
    c.update_tab("12345678901234568\nhihi\nwawa\nwawa\nwawa")
    c.update_displayer()
    cv2.imshow("win", c.bg)
    cv2.waitKey(0)
