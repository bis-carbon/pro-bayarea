# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 11:37:48 2016

@author: ibshi
"""
import os
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.misc import imread, imresize
import hickle as hkl

# resize and crop image
def process_im(im, desired_sz):
    target_ds = float(desired_sz[0])/im.shape[0]
    im = imresize(im, (desired_sz[0], int(np.round(target_ds * im.shape[1]))))
    d = (im.shape[1] - desired_sz[1]) / 2
    im = im[:, d:d+desired_sz[1]]
    return im


#data_dir ='C:/Users/ibshi/Desktop/startup.ml/video_stuff/prednet-master/kitti_results_50hz/'
res_dir ='./shanghai_results_50hz/'
data_dir ='./shanghai_data_50hz/'
prefix = 'mse_frame2_P20_' 
#suffix = '_50hz_high50'
suffix = '_50hz_low50'
parts = 20
num_clips_per_avi = 20
num_pred_frames_per_clip = 9 # remember, no prediction for first frame 
num_frames_per_clip = 10
os.chdir('C:/Users/ibshi/Desktop/startup.ml/video_stuff/prednet-master/')
home = './'
#num_pull = 2 #number of clips to pull
num_pull = 50 #number of clips to pull
high_mse = 0 # a flag to pull high MSE's (the worst fits) or low MSE's (the best fits)
desired_im_sz = (128, 160)
split = 'test'
frames_per_ex =  10

for part in range(1,parts+1):
    curr_mse_frame = res_dir+prefix+str(part)+'.csv'
    mse_in = pd.read_csv(curr_mse_frame,header = None)
    print mse_in.shape
    if (part == 1):
        mse_frame = mse_in
    else:
        mse_frame = pd.concat([mse_frame,mse_in],axis=0)

mse_clip = pd.DataFrame(np.apply_over_axes(np.mean, mse_frame, [1]))
mse_clip.columns = ['MSE']
if (high_mse):
    mse_sort = mse_clip.sort_values(['MSE'],ascending=False)
else:
    mse_sort = mse_clip.sort_values(['MSE'],ascending=True)
    
avi_list = pd.read_csv('./avi_list.csv')
clip_list = pd.read_csv('./kitti_data_50hz/cliplist_50hz.csv', header = None)

im_list = []
source_list = []  

for k in range(0,num_pull):
    curr_index = mse_sort.iloc[k].name
    curr_MSE = mse_sort.iloc[k].MSE
    curr_source_ind = int(curr_index/num_clips_per_avi)
    curr_ex = curr_index % num_clips_per_avi
    new_source = avi_list.iloc[curr_source_ind]['avi_file']
    print curr_source_ind, curr_ex, curr_MSE
    for j in range(0,num_frames_per_clip):
        new_frame = './shanghai_png/image'+str(curr_source_ind+1)+'_'+str(frames_per_ex*(curr_ex)+j)+'.png'
        im_list = im_list + [new_frame]                                 
        source_list = source_list + [new_source]

X = np.zeros((len(im_list),) + desired_im_sz + (3,), np.uint8)
for i, im_file in enumerate(im_list):
    im = imread(im_file)
    X[i] = process_im(im, desired_im_sz)

hkl.dump(X, os.path.join(home, 'X_' + split + suffix+'.hkl'))
hkl.dump(source_list, os.path.join(home, 'sources_' + split + suffix + '.hkl'))

  