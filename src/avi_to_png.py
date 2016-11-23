'''
put the unzipped avi's in the folder <home>/avi
the script will create a png folder to put the png's

'''

import os
import imageio

home = os.getcwd()

if not (os.path.isdir(home+"/png")):
    os.mkdir(home+'/png')

if not (os.path.isdir(home+"/avi")):
    print "No avi folder"
    exit()

files = [f for f in os.listdir(home+"/avi")]
ct = 1 #This will add a number id indicating the avi for each frame      

for f in files:
    print f
    fname_in = home + '/avi/'+f
    vid = imageio.get_reader(fname_in, 'ffmpeg')
    for i,im in enumerate(vid):
        image = vid.get_data(i)
        print i
        fname = home+'/png/image'+str(ct)+'_'+str(i)+'.png'
        imageio.imwrite(fname, image)
    ct = ct + 1

# Save the avi files in a csv
import pandas as pd
outlist = pd.DataFrame(files)
TrueIndex= pd.DataFrame(range(1,len(files)+1)) #because I started ct at 1 instead of 0
outlist = pd.concat([TrueIndex,outlist],axis=1)
outlist.columns = ['TrueIndex','avi_file']
outlist.to_csv("avi_list.csv")
