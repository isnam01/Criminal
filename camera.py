import cv2
import numpy as np
#from PIL import Image
#import pickle
import sqlite3
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainningData1.yml')
casecadePath='classifier/haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(casecadePath)
def getProfile(id):
    conn=sqlite3.connect('hellodata.db')
    cmd="SELECT * FROM hello WHERE ID= "+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
font=cv2.FONT_HERSHEY_SIMPLEX
#def find_id(id):

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        #self.video=cv2.VideoCapture('video.mp4')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.3,5)

        for(x,y,w,h) in faces:
            id,conf=recognizer.predict(gray[y:y+h,x:x+w])
            #p=find_id(id)
            acc=int(100-conf)
            if(acc<50):
                pass
            else:
                cv2.rectangle(image, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.rectangle(image, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
                profile=getProfile(id)
                if(profile!=None):
                    cv2.putText(image,str('Name: '+profile[1]+'  {0:.2f}%'.format(round(100-conf),2)),(x,y-75),font,0.5,(255,255,255),2)
                    cv2.putText(image,str('Age: '+str(profile[2])),(x,y-60),font,0.5,(255,255,255),1)
                    cv2.putText(image,str('Sex: '+str(profile[3])),(x,y-45),font,0.5,(255,255,255),1)
                    if(str(profile[4])!='NULL'):
                        cv2.putText(image,str(profile[4]),(x,y),font,1,(0,0,255),3)
                    else:
                        pass

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # we are 
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
