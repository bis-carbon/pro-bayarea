'''
Code for downloading and processing KITTI data (Geiger et al. 2013, http://www.cvlibs.net/datasets/kitti/)
modified by Steve Shimozaki on Nov 29, 2016
'''

import os
import requests
from bs4 import BeautifulSoup
import urllib
import numpy as np
from scipy.misc import imread, imresize
import hickle as hkl
#from kitti_settings_ss import *
import pandas as pd
import re

desired_im_sz = (128, 160)

# resize and crop image
def process_im(im, desired_sz):
    target_ds = float(desired_sz[0])/im.shape[0]
    im = imresize(im, (desired_sz[0], int(np.round(target_ds * im.shape[1]))))
    d = (im.shape[1] - desired_sz[1]) / 2
    im = im[:, d:d+desired_sz[1]]
    return im

split = 'test'
suffix = '_Sd'
im_list = []
source_list = []  # corresponds to recording that image came from
home = os.getcwd()
max_ex_per_file = 15
max_file = 108
max_ex_per_file = 2
max_file = 10
frames_per_ex =  10

avi_list = pd.read_csv(home + '/avi_list.csv')

for currfile in range(1,max_file+1):
    s_temp = avi_list[avi_list['TrueIndex']==currfile]['avi_file']
    s_file = s_temp[currfile-1]
    s_head = s_file.split(".")[0]
    s_index = currfile
    for ex in range(1,max_ex_per_file+1):
        for frame in range(0,frames_per_ex):
            # Format of image file names follows image1_11.png
            new_frame = home+'/shanghai_png/image'+str(s_index)+'_'+str(frames_per_ex*(ex-1)+frame)+'.png'
            im_list = im_list + [new_frame]                                 
            new_source = s_head + '_'+str(ex)+'.avi' 
            source_list = source_list + [new_source]

X = np.zeros((len(im_list),) + desired_im_sz + (3,), np.uint8)
for i, im_file in enumerate(im_list):
    im = imread(im_file)
    X[i] = process_im(im, desired_im_sz)

hkl.dump(X, os.path.join(home, 'X_' + split + suffix+ '.hkl'))
hkl.dump(source_list, os.path.join(home, 'sources_' + split + suffix + '.hkl'))
