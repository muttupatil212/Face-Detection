import cv2
import sys
import logging as log
import datetime as dt
from time import sleep


#Creating Haar Cascade For Face
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

#Creating Haar Cascade For Only Nose
cascPath_1 = "haarcascade_mcs_nose.xml"
noseCascade = cv2.CascadeClassifier(cascPath_1)


#Creating Haar Cascade For  Only Eyes
cascPath_2 = "eye.xml"
eyesCascade = cv2.CascadeClassifier(cascPath_2)

#Creating Haar Cascade For all features
cascPath_3 = "haarcascade_mcs_mouth.xml"
mouthCascade = cv2.CascadeClassifier(cascPath_3)

log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detecting Faces....    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_gray=gray[y:y+h, x:x+w]
        roi_color= frame[y:y+h, x:x+w]
    nose=noseCascade.detectMultiScale(roi_gray)  
    eyes=eyesCascade.detectMultiScale(roi_gray)     
    lips=mouthCascade.detectMultiScale(roi_gray)   
    
    #For all features
    for (ex,ey,ew,eh) in lips:
           cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)     
   #For only eyes
   #for (ex,ey,ew,eh) in eyes:
          #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)
    #For only nose
    #for (ex,ey,ew,eh) in nose:
    #      cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
    
   

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
