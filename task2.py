"""
Denoise Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to denoise image using median filter.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are suggested to use utils.zero_pad.
"""


import utils
import numpy as np
import json

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    # TODO: implement this function.

    s=np.shape(img)
    newimg=utils.zero_pad(img,s[0],s[1])
    s1=np.shape(newimg)
    fimage=np.zeros(s1)
    window=np.zeros((3,3))
    lis=[]
    for len in range(0,s1[0]-3):
        for lenn in range(0,s1[1]-3):
            for k in range(0,3):
                for l in range(0,3):
                    window[k,l]=newimg[len+k,lenn+l]
            liss=list(window.ravel())
            liss=sorted(liss)
            median=liss[4]
            fimage[len+1,lenn+1]=median
    ffimage=np.zeros(s)
    for a in range(0,512):
        for b in range(0,512):
            ffimage[a,b]=fimage[a+512,b+512]
    ffimage=np.uint8(ffimage)
    return ffimage


def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    # TODO: implement this function.
    s=np.shape(img1)
    sum=0
    for a in range(0,s[0]):
        for b in range(0,s[1]):
            dif=(((img1[a,b])-img2[a,b]))**2
            # print(dif)
            sum=sum+dif
    error=sum/(s[0]*s[1])
    return error


if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')


