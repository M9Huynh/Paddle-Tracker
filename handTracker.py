import cv2
import mediapipe as mp
import sys
from collections import deque
# import slider as s 

class PaddleTracker(object):
    def __init__(self, window_name = "main") -> None:
        self.window_name = window_name 
        self.delay = 20
        self.coords = deque(maxlen=self.delay)
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands()
        cv2.namedWindow(self.window_name)

    def midpoint(self, x_pos, y_pos):
        c_x_pos = sum(x_pos)/len(x_pos)
        c_y_pos = sum(y_pos)/len(y_pos)
        center = [c_x_pos,c_y_pos]    
        return center

    def track(self):
        while True:
            img = self.cap.read()[1]

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img)

            #use BGR not RGB
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            image_height, image_width, _ = img.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hand_pos = hand_landmarks.landmark
                    x_pos = [hand_pos[0].x, hand_pos[5].x, hand_pos[17].x]
                    y_pos = [hand_pos[0].y,hand_pos[5].y,hand_pos[17].y]                
                        
                    c = self.midpoint(x_pos, y_pos)
                    cx = int(c[0]*image_width)
                    cy = int(c[1]*image_height)

                    self.coords.appendleft([cx,cy])
                    cv2.circle(img,(cx,cy),1,(255, 0, 0),3)
                    
                    for i in range(1, len(self.coords)):
                        if self.coords[i-1] == None or self.coords[i] == None:
                            continue
                        cv2.line(img, self.coords[i-1], self.coords[i],(0,0,255), 3)

            cv2.imshow(self.window_name, img)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        sys.exit(1)

if __name__ == '__main__':
    tracker = PaddleTracker(window_name= "tracker") 
    tracker.track()
