# video

## Instructions for loading and running prednet evaluation on their model and their data.

Conceptual foundation of the model: [The PredNet Paper](https://arxiv.org/pdf/1605.08104v4.pdf)

The repository of PredNet source code: [https://github.com/coxlab/prednet.git](https://github.com/coxlab/prednet.git).

Some packages you might need to install before running the demo: Keras, Theano, imageio, hickle, six

## Analysis

### accident-demo

Run this notebook to test whether an avi has an accident. The first cell will ask for a frame
rate and an avi. The frame rate should be either 2 or 5 (Hz).

### hist_mse

This script takes csv's with the frame MSE's and creates histograms, both overall (across clip)
and by frame.

### kitti_evaluate-shanghai-all-plots and kitti_evaluate-shanghai-parts

These run the pretrained prednet model on input hkl files. They are modifications of the
original prednet code kitti-evaluate. -shanghai- all-plots creates plots for all the input 
clips. -shanghai-parts runs the model through batches of hkl files.

### mse_hist_start

This takes the accident videos and finds the MSE's for the first 3 frames of the accidents.

### mse_sort

This takes the 50hz results for the Shanghai data and creates hkl files for the 50 clips with
either the top or lowest MSE's. 



