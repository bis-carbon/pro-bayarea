'''
Code for downloading and processing accident avi files into .hkl files
modified by Steve Shimozaki on Dec 19, 2016
put accident-video-summary.csv in the home directory
put pngs (from avi_to_png.py) in <home>/png
'''

import os
import requests
from bs4 import BeautifulSoup
import urllib
import numpy as np
from scipy.misc import imread, imresize
import hickle as hkl
import pandas as pd
import re
import csv

home = os.getcwd()

desired_im_sz = (128, 160)

# resize and crop image
def process_im(im, desired_sz):
    target_ds = float(desired_sz[0])/im.shape[0]
    im = imresize(im, (desired_sz[0], int(np.round(target_ds * im.shape[1]))))
    d = (im.shape[1] - desired_sz[1]) / 2
    im = im[:, d:d+desired_sz[1]]
    return im

targ_hz = 2.0 
targ_ms_per_frame = 1000.0/targ_hz
framerate = str(int(targ_hz))+'hz'
frames_per_ex =  10
max_file = 40
split = 'test'
im_list_all = [[],[],[],[]]
source_list_all = [[],[],[],[]]
when_list =['before','start','during','after']

acc = pd.read_csv(home+'/accident-video-summary.csv')
acc['end timestamp'] = acc['end of accident'] - acc['start time'] 
acc['end timestamp'] = acc[['end timestamp','length']].min(axis=1)
acc['start timestamp'] = acc['start of accident'] - acc['start time']

clip_summary_columns = ['when_index','start_acc','end_acc','actual_hz','clip','frame','frame_file','source_file']

clip_summary_line = pd.DataFrame(data = [(-1,-1,-1,-1,-1,-1,'temp','temp')],columns = clip_summary_columns)
clip_summary = clip_summary_line

for currfile in range(1,max_file+1):
    
# some parameters for each currfile, prefixed by s_

    s_hz = acc['hz'].iloc[currfile - 1]
    s_length = acc['length'].iloc[currfile - 1]
    s_num_frames = int(round(s_hz * s_length))
    s_ms_start_timestamp = 1000*acc['start timestamp'].iloc[currfile - 1]
    s_ms_end_timestamp = 1000*acc['end timestamp'].iloc[currfile - 1]
    s_orig_ms_per_frame = 1000/s_hz
    skip = int(targ_ms_per_frame/s_orig_ms_per_frame)
    s_actual_hz = s_hz/skip
    s_actual_ms_per_frame = 1000/s_actual_hz
    s_start_acc_frame = int(s_ms_start_timestamp/s_orig_ms_per_frame)
    s_end_acc_frame = int(s_ms_end_timestamp/s_orig_ms_per_frame)
    s_file = acc['image avi'][currfile-1]
    s_head = s_file.split(".")[0]
    s_index = currfile
    s_total_clips = int(s_num_frames/(frames_per_ex*skip))
    
    for clip in range(0,s_total_clips):
        # is clip in before, start, during, or after?
        start_frame = int((clip)*skip*frames_per_ex)
        end_frame = start_frame + skip*(frames_per_ex - 1)
        temp_when = 'temp'
        print currfile,start_frame,end_frame
        if (end_frame < s_start_acc_frame):
            temp_when = 'before'
        if (start_frame - skip + 1 <= s_start_acc_frame  and end_frame >= s_start_acc_frame):
            temp_when = 'start'
        if (end_frame >= s_start_acc_frame and start_frame - skip + 1 <= s_end_acc_frame and temp_when != 'start'):
            temp_when = 'during'
        if (s_end_acc_frame < start_frame):
            temp_when = 'after'

        #go frame by frame for each clip
        for frame in range(start_frame,end_frame+skip,skip):

            clip_summary_line['start_acc'] = 0
            clip_summary_line['end_acc'] = 0
            clip_summary_line['actual_hz'] = s_actual_hz
            clip_summary_line['clip'] = clip
            clip_summary_line['frame'] = 1 + (frame - start_frame)/skip

            #figure out if start or end is here            
            if (frame - skip + 1 <= s_start_acc_frame  and frame >= s_start_acc_frame):
                clip_summary_line['start_acc'] = 1
            if (frame - skip + 1 <= s_end_acc_frame  and frame >= s_end_acc_frame):
                clip_summary_line['end_acc'] = 1

            curr_when_index = when_list.index(temp_when)
            clip_summary_line['when_index'] = curr_when_index

            # Format of image file names follows image1_11.png
            new_frame_file = home+'/png/image'+str(s_index)+'_'+str(frame)+'.png'
            im_list_all[curr_when_index] = im_list_all[curr_when_index] + [new_frame_file]                                 
            new_source = s_head + '_'+str(clip)+'.avi' 
            source_list_all[curr_when_index] = source_list_all[curr_when_index] + [new_source]
            clip_summary_line['frame_file'] = new_frame_file            
            clip_summary_line['source_file'] = new_source            
            clip_summary = pd.concat([clip_summary,clip_summary_line],axis=0)

#take out first line, which is a dummy line
clip_summary =clip_summary.iloc[1:]
            
max_clip = 100 # a limit to the batch file size to run on my container
step_im = max_clip * frames_per_ex

for j,when in enumerate(when_list):

    im_list = im_list_all[j]
    source_list = source_list_all[j]
    
    tot_clips = len(im_list)/frames_per_ex
    parts = int(tot_clips/max_clip) + 1
    
    clipfile = 'cliplist_acc_'+when+framerate+'.csv'
    clip_summary.loc[clip_summary['when_index']==j].to_csv(clipfile)

    X = np.zeros((len(im_list),) + desired_im_sz + (3,), np.uint8)
    for i, im_file in enumerate(im_list):
        im = imread(im_file)
        X[i] = process_im(im, desired_im_sz)

    tot_im = len(im_list)
    print when,'tot im',tot_im
    if (tot_im > 0):
        for part in range(1,parts+1):
            xbeg = int((part-1)*step_im)
            if (part == parts):
                xend = tot_im    
            else:
                xend = int(part*step_im) 
            print when,part,xbeg,xend
            hkl.dump(X[xbeg:xend], os.path.join(home, 'X_'+split+'_'+when+framerate+'P'+str(part)+'.hkl'))
            hkl.dump(source_list[xbeg:xend], os.path.join(home,'sources_'+split+'_'+when+framerate+'P'+str(part)+'.hkl'))

 