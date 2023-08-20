import cv2


#resize background video function
def resize(frame, new_width=1280):
    
   #get height and width of image
   height,width,_ = frame.shape 
   ratio = height/width 
   new_height = int(ratio*new_width)
   
   return cv2.resize(frame,(new_width,new_height))


#overlay talking video function
def overlayVideo():
    
    #capture video
    capture = cv2.VideoCapture('talking.mp4')
    
    #frame list
    frames = []


    while True:
        ret, frame = capture.read()
        
        if (ret):
            
            #resize video
            height,width,_ = frame.shape #get height n width of image
            ratio = height/width 
            new_height = int(ratio*320)
            frame =  cv2.resize(frame,(320,new_height))
            
            #add border to video
            frame = cv2.copyMakeBorder(frame, 5, 5, 5, 5, cv2.BORDER_CONSTANT,value=[0,0,0])
            
            #append frame into frame list
            frames.append(frame)
            
        else:
            break

    capture.release()
    
    #return frame list
    return frames


#overlay first watermark function
def overlayWatermark1(frame):
    
    #read image
    watermark = cv2.imread('watermark1.png')
    
    #convert image to grayscale
    gray = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    
    #get size of image
    [nrow,ncol] = gray.shape
    
    #overlay image onto frame
    for r in range(nrow):
        for c in range(ncol):
            if(gray[r,c] != 0):
                frame[r,c] = watermark[r,c]


#overlay second watermark function
def overlayWatermark2(frame):
    
    #read image
    watermark = cv2.imread('watermark2.png')
    
    #convert image to grayscale
    gray = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    
    #get size of image
    [nrow,ncol] = gray.shape
    
    #overlay image onto frame
    for r in range(nrow):
        for c in range(ncol):
            if(gray[r,c] != 0):
                frame[r,c] = watermark[r,c]

#process video(blur face, overlay video and watermark) function
def process(capture,outputname, neighbourno):
    
    #initialize output video details
    outputpath = outputname + '.avi'
    codec = cv2.VideoWriter_fourcc('X','V','I','D')
    framerate = 30
    resolution = (1280,720)
    
    #set up video writer
    output = cv2.VideoWriter(outputpath,codec,framerate,resolution)
    
    #set up video capture
    if capture.isOpened():
        ret, frame = capture.read()
    
    else:
        ret = False
        
    #add overlay talking video to frame
    overlayframes = overlayVideo()
    counter = 0
    
    while ret:
        ret, frame = capture.read()
        
        if(ret):
            
            #resize frame
            frame = resize(frame)
            
            #convert video frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           
            #cascasde face detector
            face_cascade = cv2.CascadeClassifier('face_detector.xml')
           
            #detect face in gray video
            faces_rect = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=neighbourno)
           
            #blur faces in frame
            for (x,y,w,h) in faces_rect:
                frame[y:y+h,x:x+w] = cv2.GaussianBlur(frame[y:y+h,x:x+w],(25,25),cv2.BORDER_DEFAULT)
            
            
            #overlay talking video and loop talking video if length is shorter than backgrond video
            if(counter < 465): 
                frame[50:50+overlayframes[counter].shape[0], 50:50+overlayframes[counter].shape[1]] = overlayframes[counter]
                counter += 1
            else:
                counter = 0
                frame[50:50+overlayframes[counter].shape[0], 50:50+overlayframes[counter].shape[1]] = overlayframes[counter]
            
            #get current frame number and total video frames
            currentframe = capture.get(cv2.CAP_PROP_POS_FRAMES)
            totalframes = capture.get(cv2.CAP_PROP_FRAME_COUNT)
            
            #overlay watermark 1 for first half portion of the video
            if(currentframe <= int(totalframes/2)):
                overlayWatermark1(frame)
            
            #overlay watermark 2 for second half portion of the video
            else:
                overlayWatermark2(frame)
            
            #write and show output video
            output.write(frame)
            cv2.imshow('video',frame)
            
            #break while loop to end video
            if cv2.waitKey(20) & 0xFF==ord('d'):
                break
        
        else:
            break
    
    cv2.destroyAllWindows()
    output.release()
    capture.release()

#capture videos
capture1 = cv2.VideoCapture('street.mp4')
capture2 = cv2.VideoCapture('exercise.mp4')
capture3 = cv2.VideoCapture('office.mp4')

#process captured videos
process(capture1, 'output/output1',6)
process(capture2, 'output/output2',2)
process(capture3, 'output/output3',3)


