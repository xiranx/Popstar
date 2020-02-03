import cv2
import numpy as np

def initial_map():
    map = np.zeros((10,10))
    img = cv2.imread('/Users/xxr/Desktop/xrr_screenshot/popstar.png')

    #2-20，3-45，4-80，5-125，6-180，8-320，9-405
    #剩五个星星奖励1500   2000-x*x*20
    # get a frame and show
    boundaries = [
        ([100,43,46],[124,255,255]),#blue,1
        ([35,43,46],[77,255,255]),#green,2
        ([20,100,100],[30,255,255]),#yellow,3
        ([125,43,46],[155,255,255]),#purple,4
        ([156,43,46],[180,255,255]),#red,5
    ]

    (row,column,channel) = img.shape
    img = cv2.resize(img,(int(column*0.4),int(row*0.4)))
    frame = img
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    color = 1
    for (lower,upper) in boundaries:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv,lower,upper)
        for i in range(10):
            for j in range(10):
                if np.mean(mask[280+i*43:300+i*43,20+j*43:24+j*43])>50:
                    map[9-j,i]= color
        color=color+1
    return map

def Pop(coor,poplist,map,ori_map):
    coor_row,coor_column = coor
    shortlist = Neighbour(coor)
    for row,column in shortlist:
        if not ori_map[row,column] and map[row,column] == map[coor_row,coor_column]:
                poplist.append((row,column))
                ori_map[row,column]=True
                Pop((row,column),poplist,map,ori_map)
    return poplist

#(9,8)
def Neighbour(coor):
    row,column = coor
    shortlist = []
    if row>0:
        up = (row-1,column)
        shortlist.append(up)
    if row <9:
        down = (row+1,column)
        shortlist.append(down)
    if column>0:
        left = (row,column-1)
        shortlist.append(left)
    if column<9:
        right = (row,column+1)
        shortlist.append(right)
    return shortlist

map = initial_map()
print(map)
ori_map = np.zeros((10,10),dtype = bool)
ori_map[(4,3)]=True
poplist = Pop((4,3),[(4,3)],map,ori_map)
print(poplist)
