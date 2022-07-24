#!/usr/bin/env python
import freenect
import cv2 as cv
import numpy as np
from PIL import Image
import tk
from pydub import AudioSegment
import pygame

cv.namedWindow('Depth')
cv.namedWindow('Video')
cv.namedWindow('Water')
print('Press ESC in window to stop')


def pretty_depth(depth):
    """Converts depth into a 'nicer' format for display

    This is abstracted to allow for experimentation with normalization

    Args:
        depth: A numpy array with 2 bytes per pixel

    Returns:
        A numpy array that has been processed whos datatype is unspecified
    """
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

def get_depth():
    return 


def get_video():
    return np.array(freenect.sync_get_video()[0])

def count_frames_manual(video):
	# initialize the total number of frames read
	total = 0
	# loop over the frames of the video
	while True:
		# grab the current frame
		(grabbed, frame) = video.read()
	 
		# check to see if we have reached the end of the
		# video
		if not grabbed:
			break
		# increment the total number of frames read
		total += 1
	# return the total number of frames in the video file
	return total

def check_depth():
    blue = cv.VideoCapture('water_gifs/water_b.mp4')
    blue_red = cv.VideoCapture('water_gifs/water_b_to_r.mp4')
    red_blue = cv.VideoCapture('water_gifs/water_b_to_r_rev.mp4')
    red = cv.VideoCapture('water_gifs/water_r.mp4')
    modes = [blue, blue_red, red_blue, red]
    FRAMECOUNT = 150
    mode = 0
    '''frames = []
    while cap.isOpened():
        _ret, frame = cap.read()        
        if frame is None:
            break
        frames.append(frame)
    cap.release()'''
    idx = 0
    #normal = AudioSegment.from_file("steamrave_sound/normal.wav", format="wav")
    #distorted = AudioSegment.from_file("steamrave_sound/distorted.wav", format="wav")
    pygame.mixer.init()
    normal = pygame.mixer.Sound('steamrave_sound/basesound.wav')
    distorted = pygame.mixer.Sound('steamrave_sound/distortion.wav')
    pygame.mixer.set_num_channels(2)
    n_channel = pygame.mixer.Channel(0)
    d_channel = pygame.mixer.Channel(1)
    n_channel.play(normal, -1)
    d_channel.play(distorted, -1)
    d_channel.pause()
    cs = "b"
    transition = False
    while 1:
        cap = modes[mode]
        ret, frame = cap.read()
        if ret:
            cv.imshow('frame', frame)
        else:
            if mode == 0:
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            elif mode == 3:
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            elif mode == 1:
                mode = 3
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            elif mode == 2:
                mode = 0
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        depth = pretty_depth(freenect.sync_get_depth()[0])
        cv.imshow('Depth', depth)
        threshold = 240
        vals = depth[depth < threshold]
        
        if (vals.shape[0])/(depth.shape[0]*depth.shape[1]) > 0.35 and mode == 0:
            mode = 1
            cap = modes[mode]
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            transition = True
            avg_depth = np.average(vals)
            d_channel.set_volume(0.3 + 1.5*(240 - avg_depth)/240)
            d_channel.unpause()
            print("activated", avg_depth)
            idx += 1
        elif (vals.shape[0])/(depth.shape[0]*depth.shape[1]) > 0.35 and mode == 2:
            mode = 1
            curframe = cap.get(cv.CAP_PROP_POS_FRAMES)
            cap = modes[mode]
            cap.set(cv.CAP_PROP_POS_FRAMES, 150 - curframe)
            transition = True
            avg_depth = np.average(vals)
            d_channel.set_volume(0.3 + 1.5*(240 - avg_depth)/240)
            d_channel.unpause()
            print("activated", avg_depth)
            idx += 1
        elif (vals.shape[0])/(depth.shape[0]*depth.shape[1]) < 0.35 and mode == 3:
            d_channel.pause()
            mode = 2
            cap = modes[mode]
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            cv.imshow('frame', frame)
            transition = False    
        elif (vals.shape[0])/(depth.shape[0]*depth.shape[1]) < 0.35 and mode == 1:   
            d_channel.pause()
            mode = 2
            curframe = cap.get(cv.CAP_PROP_POS_FRAMES)
            cap = modes[mode]
            cap.set(cv.CAP_PROP_POS_FRAMES, 150 - curframe)
            ret, frame = cap.read()
            cv.imshow('frame', frame)
            transition = False           
        if cv.waitKey(10) == 27:
            break

check_depth()






