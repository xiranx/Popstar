import cv2
import numpy as np
import os
import time


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

def Renew_map(map,poplist):
    for row,column in poplist:
        map[row,column]=0
    #数每一行有几个零  然后平移几个
    for i in range(10):
        for j in range(1,10):
            if map[i,j]==0:
                map[i,1:j+1]=map[i,0:j]
                map[i,0]=0
    for i in range(1,10):
        if map[i][9]==0:
            map[1:i+1,:]=map[0:i,:]
            map[0,:]=0
    return map

def Play(map):
    global current_score
    global clicklist
    global score
    candidate = Check_ClickableStar(map)
    if len(candidate)==0:
        left_stars = 0
        for i in range(10):
            for j in range(10):
                if map[i,j]>0:
                    left_stars = left_stars+1
        bonus = 2000-left_stars*left_stars*20
        if bonus>0:
            current_score = current_score+bonus
        return True
    else:
        poplist = candidate[np.random.choice(len(candidate))]
        coor = poplist[np.random.choice(len(poplist))]
        row,column = coor
        clicklist.append((column,9-row))
        once_score = len(poplist)*len(poplist)*5
        score.append(once_score)
        current_score = current_score + once_score
        Renew_map(map,poplist)
        return Play(map)

def Check_ClickableStar(map):
    candidate = []
    frame = map.copy()
    for i in range(10):
        for j in range(10):
            if frame[i][j] != 0:
                ori_map = np.zeros((10,10),dtype=bool)
                ori_map[i,j]=True
                poplist = Pop((i,j),[(i,j)],map,ori_map)
                if len(poplist) > 1:
                    candidate.append(poplist)
                    for row,column in poplist:
                        frame[row,column]=0
    return candidate

def pull_screen():
    os.system('adb shell screencap -p /sdcard/popstar.png')
    os.system('adb pull /sdcard/popstar.png /Users/xxr/Desktop/xrr_screenshot')


best_clicklist = []
score = []
best_score = 0
pull_screen()
for i in range(500):
    map = initial_map()
    clicklist = []
    current_score = 0
    Play(map)
    if best_score<current_score:
        best_clicklist = clicklist
        best_score = current_score

print('final score',best_score)

for i,j in best_clicklist:
    row = 700+i*109
    column = 50+j*109
    os.system('adb shell input tap %i %i' % (column,row))
    time.sleep(1.0)



