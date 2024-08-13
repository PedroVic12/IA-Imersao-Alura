import cv2
import mediapipe as mp
import pyautogui
from PIL import ImageGrab
import requests
from abc import ABC, abstractmethod
import os
import numpy as np

# Single Responsibility Principle: Separating the responsibilities into different classes.
class OSsystemController:
    def __init__(self):
        pass
    
    def iniciar(self):
        _prompt = "Execute +xhost no terminal"
        print(_prompt)
        
        
class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hand(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return results

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def move_and_click(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        print(f"Clicked at ({x}, {y})")

class ScreenCapture:
    def capture_screen(self):
        screenshot = ImageGrab.grab()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

class ElementDetector:
    def __init__(self):
        self.api_endpoint = "https://api.gemini-pro-vision.com/analyze"  # Hypothetical API endpoint

    def detect_elements(self, image):
        _, img_encoded = cv2.imencode('.jpg', image)
        response = requests.post(self.api_endpoint, files={"image": img_encoded.tobytes()})
        return response.json()

class HandMouseControl:
    def __init__(self, detector: HandDetector, mouse_controller: MouseController, screen_capture: ScreenCapture, element_detector: ElementDetector):
        self.detector = detector
        self.mouse_controller = mouse_controller
        self.screen_capture = screen_capture
        self.element_detector = element_detector

    def process_frame(self):
        screen = self.screen_capture.capture_screen()
        hand_results = self.detector.detect_hand(screen)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.detector.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x = int(index_finger_tip.x * self.mouse_controller.screen_width)
                y = int(index_finger_tip.y * self.mouse_controller.screen_height)

                self.mouse_controller.move_and_click(x, y)
                print(f"Tamnho da tela no monitor Size: {self.mouse_controller.screen_width}x{self.mouse_controller.screen_height}, Clicked at ({x}, {y})")

        elements = self.element_detector.detect_elements(screen)
        for element in elements['boxes']:
            cv2.rectangle(screen, (element['x'], element['y']), (element['x'] + element['width'], element['y'] + element['height']), (0, 255, 0), 2)

        cv2.imshow("Screen with Hand Detection ;) ", screen)

# Dependency Injection: We inject dependencies instead of creating instances inside the class.
if __name__ == "__main__":
    
    try:
        print("Concotrle Gestos e Clicks com IA")
        
        
        hand_detector = HandDetector()
        mouse_controller = MouseController()
        screen_capture = ScreenCapture()
        element_detector = ElementDetector()
        sistema_operacional = OSsystemController()
        sistema_operacional.iniciar()

        hand_mouse_control = HandMouseControl(hand_detector, mouse_controller, screen_capture, element_detector)
    
        while True:
            hand_mouse_control.process_frame()
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        cv2.destroyAllWindows()
    except Error as e:
        print("\n\nSomething went wrong :(  " ,e)
    finally:
        print("The 'try except' is finished") 

        
      
