import cv2
import numpy as np


def initial_map():

    map = np.zeros((10,10))
    img = cv2.imread('/Users/xxr/Desktop/WechatIMG7.jpeg')

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
        lower = np.array(lower,dtype="uint8")
        upper = np.array(upper,dtype="uint8")
        mask = cv2.inRange(hsv,lower,upper)
        for i in range(10):
            for j in range(10):
                if np.mean(mask[280+i*43:300+i*43,20+j*43:24+j*43])>50:
                    map[i,j]= color
        color=color+1
    return map




def Pop(coor,poplist):
    coor_row,coor_column = coor
    shortlist = Neighbour(coor)
    for item in poplist:
        if item in shortlist:
            shortlist.remove(item)
    for row,column in shortlist:
        if map[row][column] == map[coor_row][coor_column]:
            poplist.append((row,column))
            Pop((row,column),poplist)
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
        map[row][column]=0
        if row>1:
            map[1:row+1,column] = map[0:row,column]
            map[0,column]=0
        elif row ==1:
            map[1,column]=map[0,column]
            map[0,column]=0
    '''
    for i in range(1,10):
        for j in range(10):
            if map[i][j]==0:
                if i==1:
                    map[i][j]=map[i-1][j]
                    map[0][j]=0
                else:
                    map[1:i+1,j]=map[0:i,j]
                    map[0][j]=0
    '''
    for j in range(8,0,-1):
            if map[9][j]==0:
                for i in range(j,9):
                    map[:,i]=map[:,i+1]
                    map[:,i+1]=0
    return map

def Play(map):
    global current_score
    global clicklist
    candidate = []
    for i in range(10):
        for j in range(10):
            if map[i][j] !=0:
                neighbour = Neighbour((i,j))
                for row,column in neighbour:
                    if map[row][column]==map[i][j]:
                        candidate.append((i,j))
                        break
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
        index = np.random.randint(0,len(candidate))
        coor = candidate[index]
        clicklist.append(coor)
        poplist = Pop(coor,[coor])
        score = len(poplist)*len(poplist)*5
        current_score = current_score + score
        Renew_map(map,poplist)
        return Play(map)




best_clicklist = []
best_score = 0
for i in range(500):
    map = initial_map()
    clicklist = []
    current_score = 0
        #print('----------------')
    Play(map)
    #print('current_score',current_score)
    if best_score<current_score:
        best_clicklist = clicklist
        best_score = current_score
    #print('best_score',best_score)
    #print('best+clicklist',clicklist)
print(best_clicklist)
print(best_score)

