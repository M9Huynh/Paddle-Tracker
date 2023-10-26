import cv2
import mediapipe as mp
import slider as s 
from collections import deque

def midpoint(x_pos, y_pos):

    c_x_pos = sum(x_pos)/len(x_pos)
    c_y_pos = sum(y_pos)/len(y_pos)

    center = [c_x_pos,c_y_pos]    

    return center

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands()

webcam=cv2.VideoCapture(0)

root = 'main'
cv2.namedWindow(root)

sliders = [s.make_slid(0,255,29, 'r', root)]

coords = deque(maxlen=20)

while True:
    sucess, img = cap.read()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)

    #use BGR not RGB
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    image_height, image_width, _ = img.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,hand_landmarks, connections = mp_hands.HAND_CONNECTIONS)
            hand_pos = hand_landmarks.landmark
            x_pos = [hand_pos[0].x, hand_pos[5].x, hand_pos[17].x]
            y_pos = [hand_pos[0].y,hand_pos[5].y,hand_pos[17].y]                
                
            c = midpoint(x_pos, y_pos)
            cx = int(c[0]*image_width)
            cy = int(c[1]*image_height)
            coords.appendleft([cx,cy])
            cv2.circle(img,(cx,cy),1,(255, 0, 0),3)
            for i in range(1, len(coords)):
                if coords[i-1] == None or coords[i] == None:
                    continue
                cv2.line(img, coords[i-1], coords[i],(0,0,255), 1)

    cv2.imshow(root, img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()

# if __name__ == '__main__':
