import cv2

import mediapipe as mp

from deepface import DeepFace

import time



cap = cv2.VideoCapture(0)

frame_count = 0 

while True:

    ret, frame = cap.read()



    if not ret:

        break



    frame = cv2.flip(frame, 1)

    frame_count += 1



    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



    current_time = time.time()



    cv2.imshow("Emoçoes", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



cap.release()

cv2.destroyAllWindows()