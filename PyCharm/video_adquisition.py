# Dependencies
# streamlink package must be installed.

# Libraries

#import cv2  # opencv-python package must be installed.
import subprocess
import time
import os

# Input: video url
import cv2

video_url = "https://www.youtube.com/watch?v=F109TZt3nRc&feature=emb_logo" # Youtube

# Create output folder if necessary
output_dir = './tmp/';
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Clean existing file
subprocess.call(['del', '.\\tmp\\tmp.mp4'], shell=True) # shell=True needed in Windows to find operating commands

# Captured video stream.
subprocess.call(["streamlink", video_url, "best", "-o", "./tmp/tmp.mp4"])
#subprocess.Popen(["streamlink", video_url, "best", "-o", "./tmp/tmp.mp4"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(5)

# Open captured video
cap = cv2.VideoCapture("./tmp/tmp.mp4")
counter = 0
while cap.isOpened():
    # Read frame from video
    ret, frame = cap.read()
    # Show one frame out of 100 from video
    if 0 == counter % 100 and ret:
        if frame is not None:
            # Display the resulting frame
            cv2.imshow('frame', frame)
        else:
            print("No images")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    counter += 1
    time.sleep(0.025)

# Release memory
cv2.destroyAllWindows()
#
# vPafy = pafy.new('https://www.youtube.com/watch?v=bPw1KicdUzY')
#
# best = vPafy.getbest(preftype="webm")
#
# cap = cv2.VideoCapture(best.url)
# while (True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#cap.release()
#cv2.destroyAllWindows()
# from vidgear.gears import CamGear
# import cv2
#
# stream = CamGear(source='https://www.youtube.com/watch?v=bPw1KicdUzY',y_tube=True).start()
#
# while True:
#     frame=stream.read()
#     if frame is None:
#         break
#
#     cv2.imshow("Output frame",frame)
#     key = cv2.waitKey(1) & 0xFF
#
#     if key == ord('q'):
#         break
#
#
#
#
#
# cv2.destroyAllWindows()
#
# stream.stop()

