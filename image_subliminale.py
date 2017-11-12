#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 11:23:12 2017

@author: Nicolas
"""
import cv2
import numpy as np

# Choose what to do :
# 1 : Get the frames that will be replaced
# 2 : Put the subliminal frames in the video
# 3 : ERROR and testing block
choice = 2

period_of_sub_frames_s = 30 # Periods between each subliminal image in seconds

###############################################################################
# General video settings
###############################################################################
# Import the video file
vidcap = cv2.VideoCapture('video.mp4')

# Video properties
CV_CAP_PROP_POS_MSEC = 0        # Current position of the video file in milliseconds or video capture timestamp.
CV_CAP_PROP_POS_FRAMES = 1      # 0-based index of the frame to be decoded/captured next.
CV_CAP_PROP_POS_AVI_RATIO = 2   # Relative position of the video file: 0 - start of the film, 1 - end of the film.
CV_CAP_PROP_FRAME_WIDTH = 3     # Width of the frames in the video stream.
CV_CAP_PROP_FRAME_HEIGHT = 4    # Height of the frames in the video stream.
CV_CAP_PROP_FPS = 5             # Frame rate.
CV_CAP_PROP_FOURCC = 6          # 4-character code of codec.
CV_CAP_PROP_FRAME_COUNT = 7     # Number of frames in the video file.
CV_CAP_PROP_FORMAT = 8          # Format of the Mat objects returned by retrieve() .
CV_CAP_PROP_MODE = 9            # Backend-specific value indicating the current capture mode.
CV_CAP_PROP_BRIGHTNESS = 10     # Brightness of the image (only for cameras).
CV_CAP_PROP_CONTRAST = 11       # Contrast of the image (only for cameras).
CV_CAP_PROP_SATURATION = 12     # Saturation of the image (only for cameras).
CV_CAP_PROP_HUE = 13            # Hue of the image (only for cameras).
CV_CAP_PROP_GAIN = 14           # Gain of the image (only for cameras).
CV_CAP_PROP_EXPOSURE = 15       # Exposure (only for cameras).
CV_CAP_PROP_CONVERT_RGB = 16    # Boolean flags indicating whether images should be converted to RGB.
CV_CAP_PROP_WHITE_BALANCE = 17  # Currently not supported
CV_CAP_PROP_RECTIFICATION = 18  # Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

width = int(vidcap.get(CV_CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(CV_CAP_PROP_FRAME_HEIGHT))
fps = int(round(vidcap.get(CV_CAP_PROP_FPS)))
nb_frame = round(vidcap.get(CV_CAP_PROP_FRAME_COUNT))
codec = vidcap.get(CV_CAP_PROP_FOURCC)
    
count = 0
temp = 0

if choice == 1:
###############################################################################
# 1 : Get the frames that will be replaced
###############################################################################
    while(vidcap.isOpened()):
        success,frame = vidcap.read()
        if success==True:
            if count%(period_of_sub_frames_s*fps) == 0:
                if count > 0:
                    cv2.imwrite("montage/frame%d.jpg" % count, frame)     # save frame as JPEG file
            if round(count/nb_frame) > temp:
                temp = round(count/nb_frame)
                print('%i %%' % temp)
            count = count+1
        else:
            break
    
    # Release everything if job is finished
    vidcap.release()
    #out.release()
    cv2.destroyAllWindows()



elif choice == 2:
###############################################################################
# 2 : Put the subliminal frames in the video
###############################################################################
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # Define the codec
    video_out = cv2.VideoWriter('video_sub.avi',fourcc, fps, (width,height), True) # Create VideoWriter object
    # I have not found yet a combination of codec and video format compatible with .mp4 video format
    
    print('%i %%' % temp)
    while(vidcap.isOpened()):
        success,frame = vidcap.read()
        if success==True:
            if count == 300: # Select the frame 300
                frame_sub = cv2.imread("montage/frame"+ str(count) +"_sub.jpg")
                video_out.write(frame_sub)     # write subliminal frames
            elif count%(period_of_sub_frames_s*fps) == 0: # Select the frames that will be replaced
                if count > 0:
                    frame_sub = cv2.imread("montage/frame"+ str(count) +"_sub.jpg")
                    video_out.write(frame_sub)     # write subliminal frame
            else:
                video_out.write(frame) # write normal frame
            if round(count/nb_frame*100) > temp:
                temp = round(count/nb_frame*100)
                print('%i %%' % temp)
            count = count+1
        else:
            break
    
    # Release everything if job is finished
    vidcap.release()
    video_out.release()
    #cv2.destroyAllWindows()

else:
###############################################################################
# Error
###############################################################################
    print('Choice ERROR and free noise video')
    writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))
    for frame in range(100):
        writer.write(np.random.randint(0, 255, (480,640,3)).astype('uint8'))
        writer.release()
    for i in range(int(nb_frame)):
        if i%(period_of_sub_frames_s*fps) == 0:
            if i > 0:
                print(i)