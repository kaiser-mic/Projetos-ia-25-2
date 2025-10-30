import cv2
import mediapipe as mp 
import webbrowser

mp_hands = mp.solutions.hands 
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

LINK_URL = "https://youtu.be/mFIqdcxSVvM?si=qBOjRKMgT_V97ibh"
link_aberto = False

cap = cv2.VideoCapture(0)

print("Iniciando webcam... Pressione 'q' para sair.")
print(f"Mostre o 'Sinal da Paz' para abrir: {LINK_URL}")

while True: 
    ret, frame = cap.read()

    if not ret:
        print("Imagem indisponivel")
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesto_detectado = ""
    gesto_paz_detectado_agora = False 

    if results.multi_hand_landmarks: 
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            indicador_levantado = landmarks[8].y < landmarks[6].y
            medio_abaixado = landmarks[12].y > landmarks[10].y
            anelar_abaixado = landmarks[16].y > landmarks[14].y
            mindinho_abaixado = landmarks[20].y > landmarks[18].y

            if indicador_levantado and medio_abaixado and anelar_abaixado and mindinho_abaixado:
                gesto_detectado = "INDICADOR LEVANTADO!"

            medio_levantado = landmarks[12].y < landmarks[10].y 
            
            if indicador_levantado and medio_levantado and anelar_abaixado and mindinho_abaixado:
                gesto_detectado = "SINAL DA PAZ!"
                gesto_paz_detectado_agora = True 
                    
    if gesto_paz_detectado_agora and not link_aberto:
        print("Gesto detectado! Abrindo link...")
        webbrowser.open(LINK_URL, new=2)
        link_aberto = True
        gesto_detectado = "Abrindo o Link!"
    
    if not gesto_paz_detectado_agora:
        link_aberto = False

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

print("Fechando...")
cap.release()
cv2.destroyAllWindows()