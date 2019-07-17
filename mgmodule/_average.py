import cv2
import numpy as np
import os

def average_image(filename, normalize = True):

	"""
	Post-processing tool. Finds and saves an average image of entire video.
	
	parameters:
	enhance (float): Takes values between '0' and '1'. Where '0' is no enhancement and '1' scales the pixel 
		values such that the brightest pixel gets the value 255. 
	Usage:
	from _motionaverage import motionaverage
	motionaverage('filename.avi', enhance = 0.5)
	"""

	of = os.path.splitext(filename)[0]
	video = cv2.VideoCapture(filename)
	ret, frame = video.read()
	length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	average = frame.astype(np.float)/length
	ii = 0
	while(video.isOpened()):
		ret, frame = video.read()
		if ret==True:
			frame = np.array(frame)
			frame = frame.astype(np.float)
			average += frame/length
		else:
			print('Rendering average image 100%%')
			break
		ii+=1
		print('Rendering average image %s%%' %(int(ii/(length-1)*100)), end='\r')

	if normalize:
		average = average/np.max(average)*255
		average = average.astype(np.uint8)
		average_hsv = cv2.cvtColor(average, cv2.COLOR_BGR2HSV)
		average_hsv[:,:,2] = cv2.equalizeHist(average_hsv[:,:,2])
		average = cv2.cvtColor(average_hsv, cv2.COLOR_HSV2BGR)
		
	cv2.imwrite(of+'_average.png',average.astype(np.uint8))
