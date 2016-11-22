# video

## Instructions for loading and running prednet evaluation on their model and their data.

*Note: Run on Windows 10 with Virtualbox. Running on MacOS Sierra (version 10) hasn't worked yet.*

*Note: The prednet source code can be found at: https://github.com/coxlab/prednet.git.*

### Load docker

https://www.docker.com/products/overview

### Start Docker Quickstart Terminal

*At this point, if you start VirtualBox, you should see a default machine corresponding to docker.
Before running kitti_evaluate, I had to increase the virtual RAM to 2G (the default size is 1G)
To do this, you will need to stop the default machine and change the settings in VirtualBox, and then 
restart Docker Quickstart Terminal.*

### Within docker ($ prompt):

*This will pull the docker image*

$ docker pull keras/keras-notebook

*This will give you the image id for keras-notebook for the docker run command*

$ docker images

*This will give you the ip for the jupyter notebook*

$ docker-machine ip default

*This will start the docker container*

$ winpty docker run -p 8888:8888 -it \<image id\>

*The container should start a jupyter notebook, at \<docker-machine ip default\>:8888. Naviagate your browser to this ip address.*

*Bring up a terminal in jupyter notebook (upper right under 'New')*

##In the container terminal (# prompt):

*This will git clone the prednet source code*

\# git clone https://github.com/coxlab/prednet.git

\# cd prednet

*This will run a shell to download the prednet pre-trained model*

\# bash download_models.sh

*This will download the prednet training and test sets, in hickle format*

\# bash download_data.sh

*This will install the hickle package. Be sure to use pip2 to get it into the right environment*

\# pip2 install hickle

*At this point, you should be able to run kitti_evaluate_py, pasted into a notebook. After running kitti_evaluate, 
about 10 minutes,* 

\# cd kitti_results

*From here you can see a file called prediction_scores.txt* 

*This will go to a folder with figures giving examples of the predictions for video segments.

\# cd prediction_plots

*The inputs were 10 frames. By default there is no prediction for the first frame.*

##To retrieve the files, go to the docker quickstart terminal

*This will give you the container nickname*

$ docker ps

$ docker cp \<container nickname\>:/home/jovyan/work/prednet/kitti_results \<your folder\>



