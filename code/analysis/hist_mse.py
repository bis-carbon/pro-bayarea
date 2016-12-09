# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 11:37:48 2016

@author: ibshi
"""
import os
import numpy as np
import pandas as pd

#data_dir ='C:/Users/ibshi/Desktop/startup.ml/video_stuff/prednet-master/kitti_results_50hz/'
data_dir ='./shanghai_results_2hz/'
prefix = 'mse_frame2_P1_'
parts = 1
num_clips_per_avi = 1
num_pred_frames_per_clip = 9 # remember, no prediction for first frame 

for part in range(1,parts+1):
    curr_mse_frame = data_dir+prefix+str(part)+'.csv'
    mse_in = pd.read_csv(curr_mse_frame,header = None)
    print mse_in.shape
    if (part == 1):
        mse_frame = mse_in
    else:
        mse_frame = pd.concat([mse_frame,mse_in],axis=0)

mse_clip = np.apply_over_axes(np.mean, mse_frame, [1])

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

do_scale = 1
if (do_scale):
    xmax = np.max(np.max(mse_frame))
    ymax, tmp = mse_frame.shape

for frame in range(0,num_pred_frames_per_clip):
    frame_plot = plt.hist(mse_frame[:][frame])
    if (do_scale):
        head = 'MSEsc'
        plt.axis([0,xmax,0,ymax])
    else:
        head = 'MSE'
    plt.xlabel('MSE')
    curr_ylabel = 'Frequency out of '+str(int(2160*parts/20))+ ' clips'
    plt.ylabel(curr_ylabel)
    tit_str = 'For ' + 'frame'+ str(frame + 2) 
    plt.title(tit_str)
    pmean = np.mean(mse_frame[:][frame])
    psd = np.std(mse_frame[:][frame])
    cap_str = 'Mean = '+str(pmean)+', SD = '+str(psd)
    plt.figtext(0.0,0.0,cap_str)
    plt.show()
    figfile = head+str(frame + 2)+'.png'
    plt.savefig(figfile)
    plt.close()


overall = plt.hist(mse_clip)
if (do_scale):
    plt.axis([0,xmax,0,ymax])
    overall_file = 'MSEsc_overall.png'
else:
    overall_file = 'MSE_overall.png'
plt.xlabel('MSE')
curr_ylabel = 'Frequency out of '+str(int(2160*parts/20))+ ' clips'
plt.ylabel(curr_ylabel)
plt.title('Over all 9 frames')
pmean = np.mean(mse_clip)
psd = np.std(mse_clip)
cap_str = 'Mean = '+str(pmean)+', SD = '+str(psd)
plt.figtext(0.0,0.0,cap_str)
plt.show()
plt.savefig(overall_file)
plt.close()    
  