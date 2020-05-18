"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""

import utils
import numpy as np
import json
import time


def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    hh=np.histogram(img,bins=25)
    h1=hh[0]
    h2=hh[1]
    pair=list(np.zeros(len(h1)))

    i=0
    for val in range(0,len(h1)):
        pair[i]=h1[val],h2[val]
        i=i+1
    
    pair=(np.sort(pair,axis=0))
    lengg=len(pair)
    siz1= list(range(0, 255))
    [max1,max2]=[np.max(hh[1]),np.max(hh[0])]
    [len1,len2]=[len(hh[0]),len(hh[1])]

    def slope(a,b,c,d):
        global s1,s2,inter1,mx,my
        if a-c==0:
            s1='inf'
        else:
            s1=(float(b-d)/float(a-c))
        inter1=0
        if s1==0:
            s2='inf'
        elif s1=='inf':
            s2=0
        else:
            s2= -1 / s1
        inter1=0
        mx=float(float(a+c)/2)
        my=float(float(b+d)/2)
        inter2=(float(b+d)/2)-(s2*(float(a+c)/2))
        # inter2=my-(s2*my)
        return s1,s2,mx,my,inter1,inter2

    def makezone(a,b,c,d):
        global zone1,zone2,data,checky,checkx
        data=slope(a,b,c,d)
        zone1=[]
        zone2=[]
        cc=[]
        if s2!=1 and s2!=0:
            for aa in range(0,len1):
                checky=((data[1]*h2[aa])+data[5])
                cc.append(checky)
                if h1[aa]<=checky:
                    point=[h2[aa],h1[aa]]
                    zone1.append(point)
                else:
                    point=[h2[aa],h1[aa]]
                    zone2.append(point)
        elif s2==1:
            checkx=(a+c)/2
            for aa in range(0,len1):
                if h2[aa]<=checkx:
                    point=[h2[aa],h1[aa]]
                    zone1.append(point)
                else:
                    point=[h2[aa],h1[aa]]
                    zone2.append(point)
        elif s2==0:
            checky=(b+d)/2
            for aa in range(0,len1):
                if h1[aa]<=checky:
                    point=[h2[aa],h1[aa]]
                    zone1.append(point)
                else:
                    point=[h2[aa],h1[aa]]
                    zone2.append(point)
        return zone1,zone2
        
    def centre(zone):
        xacc=0
        yacc=0
        l=len(zone)
        for val in zone:
            xacc=xacc+(val[0])
            yacc=yacc+(val[1])
        xav=xacc/l
        yav=yacc/l
        return xav,yav

    def d(a,b,c,d):
        diss=( (a - c)**2 + (b - d)**2 )**0.5
        return diss

    def dist(z1,z2,c1,c2):
        sumz1=0
        sumz2=0
        lenz1=len(z1)
        lenz2=len(z2)
        [cx1,cy1]=c1
        [cx2,cy2]=c2
        for g in range(0,lenz1):
            [xa,ya]=z1[g]
            distancez1=d(xa,ya,cx1,cy1)
            sumz1=sumz1+distancez1

        for gg in range(0,lenz2):
            [xb,yb]=z2[gg]
            distancez2=d(xb,yb,cx2,cy2)
            sumz2=sumz2+distancez2
        return sumz1,sumz2

    fz1=[]
    fz2=[]
    fc1=[]
    fc2=[]
    fs1=[]
    fs2=[]
    for aaa in range(23,10,-1):
        for bbb in range(23,10,-1):

            [b0,a0]=pair[aaa]
            [b1,a1]=pair[bbb]

            ############################# iteration 1
            # divide into zone
            [zone1,zone2]=makezone(a0,b0,a1,b1)
            # print(zone1)
            # print(zone2)

            # find the centres
            [cx0,cy0]=centre(zone1)
            [cx1,cy1]=centre(zone2)
            # print(cx0,cy0,cx1,cy1)

            num1=str(int(cx0))+str(int(cy0))+str(int(cx1))+str(int(cy1))
            num1=int(num1)

            ########################### iteration 2
            a0=cx0
            b0=cy0
            a1=cx1
            b1=cy1
            # zone1=[]
            # zone2=[]
            makezone(a0,b0,a1,b1)
            [cx00,cy00]=centre(zone1)
            [cx11,cy11]=centre(zone2)
            num2=str(int(cx00))+str(int(cy00))+str(int(cx11))+str(int(cy11))
            num2=int(num2)

            [cx0,cy0]=[cx00,cy00]
            [cx1,cy1]=[cx11,cy11]
            i=0
            while num2!=num1:
                num1=str(int(cx0))+str(int(cy0))+str(int(cx1))+str(int(cy1))
                num1=int(num1)   
                a0=cx0
                b0=cy0
                a1=cx1
                b1=cy1
                zone1=[]
                zone2=[]
                makezone(a0,b0,a1,b1)
                [cx00,cy00]=centre(zone1)
                [cx11,cy11]=centre(zone2)
                num2=str(int(cx00))+str(int(cy00))+str(int(cx11))+str(int(cy11))
                num2=int(num2)
                [cx0,cy0]=[cx00,cy00]
                [cx1,cy1]=[cx11,cy11]

            c1=[int(cx0),int(cy0)]
            c2=[int(cx1),int(cy1)]
            [sumz1,sumz2]=dist(zone1,zone2,c1,c2)
            fc1.append(c1)
            fc2.append(c2)
            fz1.append(zone1)
            fz2.append(zone2)
            fs1.append(sumz1)
            fs2.append(sumz2)
    best=fs1.index(min(fs1))
    c1=fc1[best]
    c2=fc2[best]
    c1=c1[0]
    c2=c2[0]
    centrs=[c1,c2]
    th=(c1+c2)/2
    bsc1=fs1[best]
    bsc2=fs2[best]
    sumdistance=[bsc1,bsc2]
    sz=np.shape(img)
    label=np.zeros(sz)
    for aa in range(0,sz[0]):
        for bb in range(0,sz[1]):
            if img[aa,bb]<th:
                label[aa,bb]=0
            else:
                label[aa,bb]=1

    return centrs,label,sumdistance


def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.
    
    sz=np.shape(labels)
    imgg=np.zeros(sz)
    for aa in range(0,sz[0]):
        for bb in range(0,sz[1]):
            
            if labels[aa,bb]==0:
                imgg[aa,bb]=centers[1]
            else:
                imgg[aa,bb]=centers[0]

    imgg=np.uint8(imgg)
    # imgg=np.ndarray(imgg)
    return imgg
    # print(imgg)
    # plt.imshow(imgg)
    # plt.pause(10)
    # return imgg

     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
