# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import argparse

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(dir_path + '/../../python/openpose/Release');
    os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
    import pyopenpose as op
    
    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"
    params["hand"] = True

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    
    datum = op.Datum()
    #video = cv2.VideoCapture("../../../../Bobath_Tutorial/Bobath-c.mp4")
    video = cv2.VideoCapture(0)
    while(video.isOpened()):
        ret,frame=video.read()
        #if ret == True:
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        cv2.namedWindow("Posture_detection_video",0)
        cv2.imshow("Posture_detection_video", datum.cvOutputData)
        cv2.waitKey(1)
    
        
except :
    print('oops, something wrong')
    sys.exit(-1)
