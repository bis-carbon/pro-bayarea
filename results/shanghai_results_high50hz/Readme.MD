## kitti_results_high50hz

These are results from pretrained prednet model with the 50 Shanghai clips (50 Hz, 10 frames, .2 sec) with the highest MSE's.

The plots (in the folder prediction plots) are numbered in order, with plot_0 having the highest MSE.

To generate these plots, the clips were first sorted by MSE and the .hkl files created with mse_sort.

sources_test_50hz_high50.hkl, X_test_50hz_high50.hkl

Then the predicted and actual files were run through kitti-evaluate-evaluate-shanghai-all-plots.ipynb to create the plots.


