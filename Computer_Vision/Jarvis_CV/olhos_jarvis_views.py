import time
import cv2
import mediapipe as mp
import cvzone
import pyautogui
from models.hand_detector import HandDetector, FPS
import math
import numpy as np


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


class GestureController:
    def __init__(self, zoom_step=0.1):
        self.zoom_step = zoom_step
        self.hand_status = "Aberto"  # Inicializa o status da mão

    def handle_gesture(self, hand):
        fingers = hand["fingers"]
        if fingers == [0, 0, 0, 0, 0]:  # Mão fechada
            self.zoom_out()
            self.hand_status = "Fechado"
        elif fingers == [1, 1, 1, 1, 1]:  # Mão aberta
            self.zoom_in()
            self.hand_status = "Aberto"

    def zoom_in(self):
        pyautogui.scroll(int(100 * self.zoom_step))  # Aumentar zoom

    def zoom_out(self):
        pyautogui.scroll(int(-100 * self.zoom_step))  # Diminuir zoom

    def modes(self):
        if self.hand_status == "Aberto":
            return "zoom"


class VideoProcessor:
    def __init__(
        self,
        video_source,
        hand_detector,
        fps_calculator,
        visualizer,
        gesture_controller,
    ):
        self.video_source = video_source
        self.hand_detector = hand_detector
        self.fps_calculator = fps_calculator
        self.visualizer = visualizer
        self.gesture_controller = gesture_controller

    def visualizarMenu(self, img):
        cv2.putText(
            img,
            f"Status: {self.gesture_controller.hand_status}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

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
                self.gesture_controller.handle_gesture(hand1)
                # Exibir o status da mão na imagem
                self.visualizarMenu(img)

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


def main_openCV_Jarvis():
    # Initialize the webcam to capture video
    # The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
    cap = cv2.VideoCapture(0)

    # Initialize the HandDetector class with the given parameters
    detector = HandDetector(
        staticMode=False,
        maxHands=2,
        modelComplexity=1,
        detectionCon=0.5,
        minTrackCon=0.5,
    )

    # Continuously get frames from the webcam
    while True:
        # Capture each frame from the webcam
        # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
        success, img = cap.read()

        # Find hands in the current frame
        # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
        # The 'flipType' parameter flips the image, making it easier for some detections
        hands, img = detector.findHands(img, draw=True, flipType=True)

        # Check if any hands are detected
        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1[
                "bbox"
            ]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1["center"]  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            # Count the number of fingers up for the first hand
            fingers1 = detector.fingersUp(hand1)
            print(
                f"H1 = {fingers1.count(1)}", end=" "
            )  # Print the count of fingers that are up

            # Calculate distance between specific landmarks on the first hand and draw it on the image
            length, info, img = detector.findDistance(
                lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255), scale=10
            )

            # Check if a second hand is detected
            if len(hands) == 2:
                # Information for the second hand
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                bbox2 = hand2["bbox"]
                center2 = hand2["center"]
                handType2 = hand2["type"]

                # Count the number of fingers up for the second hand
                fingers2 = detector.fingersUp(hand2)
                print(f"H2 = {fingers2.count(1)}", end=" ")

                # Calculate distance between the index fingers of both hands and draw it on the image
                length, info, img = detector.findDistance(
                    lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0), scale=10
                )

            print(" ")  # New line for better readability of the printed output

        # Display the image in a window
        cv2.imshow("Image", img)

        # Keep the window open and update it for each frame; wait for 1 millisecond between frames
        cv2.waitKey(1)


if __name__ == "__main__":
    # video_source = VideoSource(0)
    # hand_detector = HandDetector()
    # fps_calculator = FPS()
    # visualizer = Visualizer()
    # processor = VideoProcessor(video_source, hand_detector, fps_calculator, visualizer)
    # processor.run()

    main_openCV_Jarvis()
