import cv2
import numpy as np
import sqlite3
face_casecade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture('http://192.168.11.17:8080/video?x.mjpg')
def insertOrUpdate(Id,Name,age,sex):
    conn=sqlite3.connect('database1.db')
    cmd="SELECT * FROM criminaldata WHERE id="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE criminaldata SET name="+str(Name)+" ,age= "+str(age)+" ,sex= "+str(sex)+" WHERE id="+str(Id)
    else:
        cmd="INSERT INTO criminaldata Values("+str(Id)+","+str(Name)+","+str(age)+","+str(sex)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()
id=input('enter uniqe id:')
name=input('enter name: ')
age=input('enter age : ')
sex=input('sex :')
insertOrUpdate(id,name,age,sex)
cap=cv2.VideoCapture('http://192.168.11.17:8080/video?x.mjpg')
count=0
while(count<50):
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces=face_casecade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        #FaceImage=gray[y-int(h/2):y + int(h*1.5),x-int(x/2):x+int(w*1.5)]

        #cv2.putText(gray,"FACE DETECTED",(x+(w/2),y-5),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255))
        frame=gray[y:y+h,x:x+w]
        cv2.imwrite("datasets/User."+str(id)+"."+str(count)+".jpg",frame)
        cv2.waitKey(300)
        cv2.imshow("CAPTURED PHOTO",frame)
        count=count+1
    cv2.imshow('Face recognition system capture faces',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print('face capture for subject is completed')
cap.release()
cv2.destroyAllWindows()
