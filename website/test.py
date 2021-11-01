from flask import Blueprint, render_template, Response
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
from website import mysql

test= Blueprint('test', __name__)
path= 'website/imagesAttendance'
images= [] #a list to store the image
classNames= [] # a list to store the name of person image to view on the webcam
myList=os.listdir(path)
#print(myList)

for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    #print(curImg)
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#print(classNames)

def findEncodings(images):
    encodeList= [] #define a new encoded image list which will return 128 dimension
    for img in images: #it will go in the list of the images [image1.jpg,image2.jpg]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert the images in the list into grayscale
        encode=face_recognition.face_encodings(img)[0] #it will encode the images in the list into 128 dimension
        encodeList.append(encode) #it will append the encoded images into the encodeList [[128 dimensions],[128 dimensions]]
    return encodeList #return the list into the findEncoding(images)

def markAttendance(name):
    with open('website/Attendance.csv','r+')as f:
        myDataList=f.readlines()
        #print(myDataList)
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'{name},{dtString}''\n')
        else:
            with open('website/ClockOut.csv', 'r+')as f:
                myDataList = f.readlines()
                # deleteList = []
                # print(myDataList)
                for line in myDataList:
                    if name in line:
                        myDataList.remove(line)
                        f.truncate(0)
                        for x in myDataList:
                            f.writelines(f'{x}')

def markclockOut(name):
    with open('website/ClockOut.csv','r+')as f:
        myDataList=f.readlines()
        #print(myDataList)
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            #if name != entry:
            nameList.append(entry[0])
        #print(name) chunyee
        #print(entry[0]) chunyee
       # if name==entry[0]:
          #  print("Same character")
       # print(nameList)
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'{name},{dtString}''\n')
        else:
            with open('website/Attendance.csv', 'r+')as f:
                myDataList = f.readlines()
                # deleteList = []
                # print(myDataList)

                for line in myDataList:
                    if name in line:
                        myDataList.remove(line)
                        f.truncate(0)
                        for x in myDataList:
                            f.writelines(f'{x}')

encodeListKnown=findEncodings(images) #images list storing the images, after return will get the encodeList variable list
#print(encodeListKnown)  #show all the encoded images with 128 dimensions
#print('Encoding Complete')



cap=cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) #resize the webcam image into 1/4
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) #set the color of the webcam image into grayscale

        facesCurFrame = face_recognition.face_locations(imgS) #search for the location of face in webcam (top,right,bottom,left)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame) #encoding the face into 128 dimension through the location stated
        #print("Face Location:",facesCurFrame) #will return the true or false (true means the face recognized, false means not recognized)
        #print("Encoded Face:",encodesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame): #will search in same time of the encoded face and the location face from the webcam
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace) #compare the both encoded faces (return True if matches, else False)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)# compare the distance of both encoded faces(the more lesser is more nearest the matches)
            print("matches:",matches) #it will return true and false
            print("Face Distance:",faceDis) #it will return the distance
            matchIndex = np.argmin(faceDis) #it will retrieve the value which is the most lesser
            #print(matchIndex[matchIndex])

            if matches[matchIndex]: #return the index such as 0 for first element in list if the distance the most accurate
                name = classNames[matchIndex].upper() #will uppercase the name based on the classNames list
                #print(name)
                #settings of the rectange in webcam
                y1, x2, y2, x1 = faceLoc #it will based on the face location which getting from the encodesCurFrame variable
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #multiple 4 because it resize into 1/4 during the image processing
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)#this is the rectangle showing the face location
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)#this is the rectangle under the face location to view the person name
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)#put text into the purple rectangle
                markAttendance(name)

        ret, buffer = cv2.imencode('.jpg', img) #show in the webpage with the jpg format
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
def gen_frames2():
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                #print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)#this is the rectangle showing the face location
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)#this is the rectangle under the face location to view the person name
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) #put text into the purple rectangle
                markclockOut(name)
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')




@test.route('/index')
def index():
    return render_template('index.html')

@test.route('/clockout')
def clockout():
    return render_template('clockout.html')

@test.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@test.route('/video_feed2')
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')
