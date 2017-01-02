# results

*Steve Shimozaki, 1/2/2017*

## Overall

There are two folders, shanghai and accident. Shanghai results are based upon the Shanghai crowd 
videos and serve as the non-accident control avi's. Accident results are based upon video clips 
found on youtube using the search term factory accident. 

All the videos so far have been analyzed as 10-frame video 'clips', as that was the original input 
to the prednet model (KITTI dataset). Also, all the avi's have been approximately 5 seconds, to match 
the original prednet input. So, with 10 frames per clip, if we were to change the frames per second, 
we would get a different number of clips for each 5-sec avi. For example, at 2 Hz, 5 seconds of one 
avi yields just one clip. At 25 Hz, a 5-second avi yields up to 12.5 clips.

The main result is the mean squared error (MSE) of the predicted and the actual frame, pixel-by-pixel,
and over the 3 color channels (RGB).

The basic structure of the analysis is either by frame ('frame') or by clip ('overall'). The first 
analyses is by frame; because we cannot predict the first frame, for each clip there are 10-1=9 
'frame' MSEs per clip, for frames 2-10. By clip or overall I have been taking the mean MSE over 
those 9 frames (for which we have MSE's) for each clip. I have been calling that the 'overall' MSE 
(because it is the the average MSE over all the frames of a clip).

In each folder there is a pdf with the distributions of the MSE's. The first one is the overall MSE. 
Then there is the distributions for each 'frame' MSE, for frames 2 to 10. Each individual plot also 
has the mean and SD for the distribution.

Each folder also has csv's with the frame MSE's. Those can be read by mse_hist.py to generate the 
plots in the pdfs. The MSE's were found by running 'kitti_evaluate-parts.ipynb' in a docker container.

## shanghai

The main results are in the folders shanghai_results_??hz, and give the results as described above 
for different frame rates (2, 5, 10, 25, and 50 hz).

The folders 'shanghai_results_high50hz' and 'shanghai_results_low50hz' are the results using 50hz, 
and looking at the clips with either the highest or lowest 50 MSE's. The pdf gives the MSE's for the
50 clips, ranked. The folder prediction plots give the images for the predicted, actual, and
MSE between predicted and actual for the 50 clips. 

To generate these plots, the clips were first sorted by MSE and the .hkl files created with 
'mse_sort.py'. The .hkl files are in the folder. Then the predicted and actual files were run through 
'kitti_evaluate-shanghai-all-plots.ipynb' to create the plots.

The folder shanghai_results_a gives the first test using a small subset of the shanghai video, 20
clips from 10 avi's (50 Hz, and 2 clips per avi). These were run on the original 'kitti_evaluate.py'
script from prednet.

## accident

These folders have the results from the accident videos, as described above. The accident videos
were 25 or 29.97 Hz; thus, the analyzed frame rates were (the closest to) 2, 5, 10, and 25 hz. 

The clips are also divided by whether the clips happened before, at the start of, during (but not
including the start of), and after the accident.  Note that some combinations do not exist; for 
example, for 2 hz there is only a 'start' category, as 2 hz with 10 frames takes up the entire 5 
second video clip. 

The 'before' clips act as controls for confounds related to the specific accident clips, for example,
the settings or context of those videos compared to the shanghai videos.

The 'overall_MSE.pdf' summarizes the MSE the 'overall' or 'clip' MSE. The 'MSE_frame.pdf' summarizes
a few key frame MSE's, namely those frames near the start of the accident (3 frames at and after the 
start), and a representative non-accident frame (frame 3, because that's where the MSE's drop off when 
looking how the frame MSE's decrease with frame, 2 to 10).


The results in 'overall_MSE.pdf' are very promising. First, there is a large difference in the MSE's 
both at the start and during the accident, compared to the Shanghai video, especially at 2 and 5 Hz. 
Also, note that before the accident the MSE's are about the same as the Shanghai videos. This last 
result suggests that it was the occurence of the accident that causes the increase of the MSEs (for 
the start and during the accident), as opposed to something about the subject (i. e., the setting or 
the context) of the videos themselves.

As far as choosing the best threshold MSE to distinguish non-accident from accident clips, by 
eyeballing, a threshold of about 0.008 for 2 Hz and about 0.005 for 5 Hz would be about the best.
A more quantitative analysis I used was choosing a threshold 3.5x the standard error from the 
mean MSE for the accident start clips. This gives thresholds of 0.00777565 for 2 hz and 0.004869763 
for 5 hz.

 


