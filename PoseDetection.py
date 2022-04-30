import cv2
import mediapipe as mp

class PoseDetector():
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def findPts(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(rgb)

        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

        pts = []
        displm = [0, 17, 18, 31, 32]
        for lm in displm:
            if(lm < len(self.lmList)):
                pts.append([self.lmList[lm][1], self.lmList[lm][2]])

        return pts
