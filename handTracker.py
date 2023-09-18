import cv2
import mediapipe as mp
import time
import slider as s 

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands()

webcam=cv2.VideoCapture(0)

root = 'main'
cv2.namedWindow(root)

sliders = [s.make_slid(0,255,29, 'r', root)]

while True:
    sucess, img = cap.read()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)

    #use BGR not RGB
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,hand_landmarks, connections = mp_hands.HAND_CONNECTIONS)
        

    cv2.imshow(root, img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()


