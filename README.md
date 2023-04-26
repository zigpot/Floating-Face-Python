# Floating-Face-Python

![](https://github.com/zigpot/Floating-Face-Python/blob/main/kocak.gif)

refer to this [link](https://zigpot.wordpress.com/2021/09/23/hello-and-making-floating-face-effect/)

### Requirements

Libraries can be installed by:

> pip3 install imutils opencv-python dlib

### How to use

prepare a file in the same directory named _video.mp4_.

run the program

> python3 new.py

a player window will open.

click any number from '1' to '8' on your keyboard everytime you want to capture a face. Each number indicates the direction the face will come from; '1' for top-left, '2' for top, '3' for top-right etc. you can skip the rest of the video by pressing ENTER which will proceed to processing right away. or quitting the program and cancelling by pressing 'q'.

The output video will be saved in the same directory as _output.mp4_.

### Todos

1. take arguments for input video, and optionally, output video name.
2. mitigate no faces case
3. mitigate multiple faces case
4. preserve audio
