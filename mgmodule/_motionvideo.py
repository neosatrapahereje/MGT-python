import cv2
import os
import numpy as np
from scipy.signal import medfilt2d
from ._centroid import mg_centroid
from ._filter import motionfilter

def motionvideo(self, kernel_size = 5):
    ret, frame = self.video.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    of = os.path.splitext(self.filename)[0] 
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(of + '_motion.avi',fourcc, self.fps, (self.width,self.height))
    gramx = np.array([1,1])
    gramy = np.array([1,1])
    qom = np.array([]) #quantity of motion
    com = np.array([]) #centroid of motion
    ii = 0
    if self.color == False:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while(self.video.isOpened()):
        #May need to do this, not sure
        if self.blur == 'Average':
            prev_frame = cv2.blur(frame,(10,10))
        else:
            prev_frame = frame

        ret, frame = self.video.read()
        if ret==True:
            if self.blur == 'Average':
                frame = cv2.blur(frame,(10,10)) #The higher these numbers the more blur you get
                    
            if self.color == True:
                frame = frame
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = np.array(frame)
            frame = frame.astype(np.int32)

            if self.method == 'Diff':
                if self.color == True:
                    motion_frame_rgb = np.zeros([self.height,self.width,3])

                    for i in range(frame.shape[2]):
                        motion_frame = (np.abs(frame[:,:,i]-prev_frame[:,:,i])).astype(np.uint8)
                        motion_frame = motionfilter(motion_frame,self.filtertype,self.thresh,kernel_size)
                        motion_frame_rgb[:,:,i] = motion_frame

                    gramy = np.append(gramx,np.mean(motion_frame_rgb,axis=0))
                    gramx = np.append(gramy,np.mean(motion_frame_rgb,axis=1))
                   
                else:
                    motion_frame = (np.abs(frame-prev_frame)).astype(np.uint8)
                    motion_frame = motionfilter(motion_frame,self.filtertype,self.thresh,kernel_size)

                    gramy = np.append(gramx,np.mean(motion_frame,axis=0))
                    gramx = np.append(gramy,np.mean(motion_frame,axis=1)) 

            elif self.method == 'OpticalFlow':
                print('Optical Flow not implemented yet!')

            if self.color == False: 
                motion_frame = cv2.cvtColor(motion_frame, cv2.COLOR_GRAY2BGR)
                motion_frame_rgb = motion_frame
            out.write(motion_frame_rgb.astype(np.uint8))
            combite, qombite = mg_centroid(motion_frame_rgb.astype(np.uint8),self.width,self.height,self.color)
            if ii == 0:
                com = combite.reshape(1,2)
                qom = qombite
            else:
                com=np.append(com,combite.reshape(1,2),axis =0)
                qom=np.append(qom,qombite)
        else:
            break
        ii+=1
        print('Processing %s%%' %(int(ii/(self.length-1)*100)), end='\r')


def plot_motion_metrics(of,com,qom,width,height):
    plt.rc('text',usetex = True)
    plt.rc('font',family='serif')
    fig = plt.figure(figsize = (12,6))
    ax = fig.add_subplot(1,2,1) 
    ax.scatter(com[:,0]/width,com[:,1]/height,s=2)
    ax.set_xlim((0,1))
    ax.set_ylim((0,1))
    ax.set_xlabel('Pixels normalized')
    ax.set_ylabel('Pixels normalized')
    ax.set_title('Centroid of motion')
    ax = fig.add_subplot(1,2,2)
    ax.set_xlabel('Time[frames]')
    ax.set_ylabel('Pixels normalized')
    ax.set_title('Quantity of motion')
    ax.bar(np.arange(len(qom)-1),qom[1:,0]/(width*height))
    #ax.plot(qom[1:-1])
    plt.savefig('%s__motion_com_qom.eps'%of,format='eps')
