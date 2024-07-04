import time
import cv2
import mediapipe as mp
import cvzone
import pyautogui
import math

"""
Hand Tracking Module
By: Computer Vision Zone

todo
https://www.youtube.com/watch?v=ieXQTtQgyo0&t=2709s
"""

import math

import cv2
import mediapipe as mp


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(
        self,
        staticMode=False,
        maxHands=2,
        modelComplexity=1,
        detectionCon=0.5,
        minTrackCon=0.5,
    ):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param modelComplexity: Complexity of the hand landmark model: 0 or 1.
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.staticMode = staticMode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.staticMode,
            max_num_hands=self.maxHands,
            model_complexity=modelComplexity,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.minTrackCon,
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(
                self.results.multi_handedness, self.results.multi_hand_landmarks
            ):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS
                    )
                    cv2.rectangle(
                        img,
                        (bbox[0] - 20, bbox[1] - 20),
                        (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                        (255, 0, 255),
                        2,
                    )
                    cv2.putText(
                        img,
                        myHand["type"],
                        (bbox[0] - 30, bbox[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (255, 0, 255),
                        2,
                    )

        return allHands, img

    def fingersUp(self, myHand):
        fingers = []
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]  # Certifique-se que myLmList tem os landmarks

        print(myHandType, myLmList)

        if self.results.multi_hand_landmarks:
            # Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
        Find the distance between two landmarks input should be (x1,y1) (x2,y2)
        :param p1: Point1 (x1,y1)
        :param p2: Point2 (x2,y2)
        :param img: Image to draw output on. If no image input output img is None
        :return: Distance between the points
                Image with output drawn
                Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, info, img


class FPS:
    """
    FPS class for calculating and displaying the Frames Per Second in a video stream.

    Attributes:
        pTime (float): Previous time stamp.
        frameTimes (list): List to keep track of frame times.
        avgCount (int): Number of frames over which to average the FPS.
    """

    def __init__(self, avgCount=30):
        """
        Initialize FPS class.

        :param avgCount: Number of frames over which to average the FPS, default is 30.
        """
        self.pTime = time.time()  # Initialize previous time to current time
        self.frameTimes = []  # List to store the time taken for each frame
        self.avgCount = avgCount  # Number of frames to average over

    def update(
        self,
        img=None,
        pos=(20, 50),
        bgColor=(255, 0, 255),
        textColor=(255, 255, 255),
        scale=3,
        thickness=3,
    ):
        """
        Update the frame rate and optionally display it on the image.

        :param img: Image to display FPS on. If None, just returns the FPS value.
        :param pos: Position to display FPS on the image.
        :param bgColor: Background color of the FPS text.
        :param textColor: Text color of the FPS display.
        :param scale: Font scale of the FPS text.
        :param thickness: Thickness of the FPS text.
        :return: FPS value, and optionally the image with FPS drawn on it.
        """

        cTime = time.time()  # Get the current time
        frameTime = (
            cTime - self.pTime
        )  # Calculate the time difference between the current and previous frame
        self.frameTimes.append(frameTime)  # Append the time difference to the list
        self.pTime = cTime  # Update previous time

        # Remove the oldest frame time if the list grows beyond avgCount
        if len(self.frameTimes) > self.avgCount:
            self.frameTimes.pop(0)

        avgFrameTime = sum(self.frameTimes) / len(
            self.frameTimes
        )  # Calculate the average frame time
        fps = 1 / avgFrameTime  # Calculate FPS based on the average frame time

        # Draw FPS on image if img is provided
        if img is not None:
            cvzone.putTextRect(
                img,
                f"FPS: {int(fps)}",
                pos,
                scale=scale,
                thickness=thickness,
                colorT=textColor,
                colorR=bgColor,
                offset=10,
            )
        return fps, img


class Visualizer:
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils

    def draw_hand_results(self, img, hands):
        if hands:
            for hand in hands:
                self.mpDraw.draw_landmarks(
                    img, hand["landmarks"], mp.solutions.hands.HAND_CONNECTIONS
                )
                cv2.rectangle(
                    img,
                    (hand["bbox"][0] - 20, hand["bbox"][1] - 20),
                    (
                        hand["bbox"][0] + hand["bbox"][2] + 20,
                        hand["bbox"][1] + hand["bbox"][3] + 20,
                    ),
                    (255, 0, 255),
                    2,
                )
                cv2.putText(
                    img,
                    hand["type"],
                    (hand["bbox"][0] - 30, hand["bbox"][1] - 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (255, 0, 255),
                    2,
                )

    def draw_distance(self, img, distance_info, color=(255, 0, 255), scale=5):
        x1, y1, x2, y2, cx, cy = distance_info
        cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
        cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
        cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

    def draw_fps(
        self,
        img,
        fps,
        pos=(20, 50),
        bgColor=(255, 0, 255),
        textColor=(255, 255, 255),
        scale=3,
        thickness=3,
    ):
        cvzone.putTextRect(
            img,
            f"FPS: {int(fps)}",
            pos,
            scale=scale,
            thickness=thickness,
            colorT=textColor,
            colorR=bgColor,
            offset=10,
        )


class VideoSource:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()


class VideoProcessor:
    def __init__(self, video_source, hand_detector, fps_calculator, visualizer):
        self.video_source = video_source
        self.hand_detector = hand_detector
        self.fps_calculator = fps_calculator
        self.visualizer = visualizer

    def process_frame(self):
        try:
            success, img = self.video_source.read()
            if not success:
                return None
            hands, img = self.hand_detector.findHands(img, draw=False, flipType=True)
            fps, img = self.fps_calculator.update(img)
            self.visualizer.draw_hand_results(img, hands)
            if hands:
                hand1 = hands[0]
                lmList1 = hand1["landmarks"]
                distance_info = self.hand_detector.findDistance(
                    lmList1[8][0:2], lmList1[12][0:2], img=None
                )
                self.visualizer.draw_distance(img, distance_info[1])
                # self.visualizarMenu(img)
                if len(hands) == 2:
                    hand2 = hands[1]
                    lmList2 = hand2["landmarks"]
                    distance_info = self.hand_detector.findDistance(
                        lmList1[8][0:2], lmList2[8][0:2], img=None
                    )
                    self.visualizer.draw_distance(
                        img, distance_info[1], color=(255, 0, 0)
                    )
            self.visualizer.draw_fps(img, fps)
            return img
        except Exception as error:
            print("Error:", error)

    def run(self):
        while True:
            img = self.process_frame()
            if img is None:
                break
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.video_source.release()
        cv2.destroyAllWindows()


class GestureController:
    def __init__(self, zoom_step=0.1):
        self.zoom_step = zoom_step

    def handle_gesture(self, hand):
        fingers = hand["fingers"]
        if fingers == [0, 0, 0, 0, 0]:  # Mão fechada
            self.zoom_out()
        elif fingers == [1, 1, 1, 1, 1]:  # Mão aberta
            self.zoom_in()

    def zoom_in(self):
        pyautogui.scroll(int(100 * self.zoom_step))  # Aumentar zoom

    def zoom_out(self):
        pyautogui.scroll(int(-100 * self.zoom_step))  # Diminuir zoom


def main_openCV_Jarvis():
    video_source = VideoSource(0)
    hand_detector = HandDetector()
    fps_calculator = FPS()
    visualizer = Visualizer()
    gesture_controller = GestureController()
    processor = VideoProcessor(video_source, hand_detector, fps_calculator, visualizer)
    processor.run()


if __name__ == "__main__":
    main_openCV_Jarvis()
