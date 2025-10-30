import cv2

import mediapipe as mp 



mp_hands = mp.solutions.hands 



hands = mp_hands.Hands()



mp_draw = mp.solutions.drawing_utils



cap = cv2.VideoCapture(0)



while True: 

    ret, frame = cap.read()



    if not ret:

        print("Imagem indisponivel")

        break

    

    frame = cv2.flip(frame, 1)



    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



    results = hands.process(rgb_frame)



    gesto_detectado = ""



    if results.multi_hand_landmarks: 

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark



            print(landmarks)

            indicador_levantado = landmarks[8].y < landmarks[6].y

            medio_abaixado = landmarks[12].y > landmarks[10].y

            anelar_abaixado = landmarks[16].y > landmarks[14].y

            mindinho_abaixado = landmarks[20].y > landmarks[18].y



            if indicador_levantado and medio_abaixado and anelar_abaixado and mindinho_abaixado:

                gesto_detectado = "INDICADOR LEVANTADO!"

            elif indicador_levantado and anelar_abaixado and mindinho_abaixado:

                gesto_detectado = "SINAL DA PAZ!"



    cv2.putText(

        frame,

        gesto_detectado,

        (10, 70),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        (0, 0, 255),

        2

    )



    cv2.imshow("Webcam", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



cap.release()

cv2.destroyAllWindows()