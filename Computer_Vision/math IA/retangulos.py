import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st


class HandDrawingApp:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.col1, self.col2 = st.columns([3, 2])
        with self.col1:
            self.run = st.checkbox("Run", value=True)
            self.FRAME_WINDOW = st.image([])

        with self.col2:
            st.title("Answer")
            self.output_text_area = st.subheader("")

        genai.configure(api_key="AIzaSyCZhKI6vWIAK0GkzXajc-PUjTBEO5zjoeA")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        self.detector = HandDetector(
            staticMode=False,
            maxHands=1,
            modelComplexity=1,
            detectionCon=0.7,
            minTrackCon=0.5,
        )

        self.prev_pos = None
        self.canvas = None
        self.output_text = ""

    def get_hand_info(self, img):
        hands, img = self.detector.findHands(img, draw=False, flipType=True)
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            fingers = self.detector.fingersUp(hand)
            return fingers, lmList
        else:
            return None

    def draw(self, info):
        fingers, lmList = info
        current_pos = None
        if fingers == [0, 1, 0, 0, 0]:
            current_pos = lmList[8][0:2]
            if self.prev_pos is None:
                self.prev_pos = current_pos
            cv2.line(
                self.canvas, tuple(current_pos), tuple(self.prev_pos), (0, 255, 0), 10
            )
            self.prev_pos = current_pos
        elif fingers == [1, 0, 0, 0, 0]:
            self.canvas = np.zeros_like(self.img)

    def send_to_ai(self, fingers):
        try:
            if fingers == [1, 1, 1, 1, 0]:
                pil_image = Image.fromarray(self.canvas)
                response = self.model.generate_content(
                    [
                        "Identifique o que estou desenhando e o assunto matematico ou fisico (se existir) e tente resolver por estapas e me de a resposta em portugues",
                        pil_image,
                    ]
                )
                return response.text
        except Exception as error:
            print(error)
        return ""

    def run_app(self):
        while self.run:
            success, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 1)

            if self.canvas is None:
                self.canvas = np.zeros_like(self.img)

            info = self.get_hand_info(self.img)
            if info:
                fingers, lmList = info
                self.draw(info)
                self.output_text = self.send_to_ai(fingers)

            image_combined = cv2.addWeighted(self.img, 0.7, self.canvas, 0.3, 0)
            self.FRAME_WINDOW.image(image_combined, channels="BGR")

            if self.output_text:
                self.output_text_area.text(self.output_text)

            cv2.waitKey(1)

    def show_drawing(self):
        if self.canvas is not None:
            cv2.imshow("Desenho", self.canvas)
            cv2.waitKey(1)


if __name__ == "__main__":
    app = HandDrawingApp()
    app.run_app()
