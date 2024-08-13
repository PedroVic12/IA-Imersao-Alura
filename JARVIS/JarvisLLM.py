

import cv2
import mediapipe as mp
import pyautogui
from PIL import ImageGrab
import requests
import numpy as np

class LLMJARVIS:
    def __init__(self):
        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Screen and Mouse properties
        self.screen_width, self.screen_height = pyautogui.size()
        self.api_endpoint = "https://api.gemini-pro-vision.com/analyze"  # Hypothetical API endpoint
    
    def iniciar(self):
        _prompt = "Execute +xhost no terminal"
        print(_prompt)
    
    def detect_hand(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return results

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y)
        print(f"Moved mouse to ({x}, {y})")

    def click_mouse(self):
        pyautogui.click()
        print("Mouse clicked")

    def scroll_mouse(self, direction):
        pyautogui.scroll(direction)
        print(f"Scrolled {'up' if direction > 0 else 'down'}")

    def capture_screen(self):
        screenshot = ImageGrab.grab()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def detect_elements(self, image):
        _, img_encoded = cv2.imencode('.jpg', image)
        response = requests.post(self.api_endpoint, files={"image": img_encoded.tobytes()})
        return response.json()

    def generate_description(self, image):
        # Hypothetical implementation, assuming the API provides a description of the image
        response = self.detect_elements(image)
        if "description" in response:
            return response["description"]
        else:
            return "Description not available."

    def process_frame(self):
        screen = self.capture_screen()
        hand_results = self.detect_hand(screen)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                
                x = int(index_finger_tip.x * self.screen_width)
                y = int(index_finger_tip.y * self.screen_height)

                # Calculating distance between index finger tip and thumb tip
                thumb_x, thumb_y = int(thumb_tip.x * self.screen_width), int(thumb_tip.y * self.screen_height)
                distance = np.linalg.norm([x - thumb_x, y - thumb_y])

                # Determine gesture based on the relative position and distance
                if distance < 40:
                    self.click_mouse()
                elif distance > 70:
                    self.move_mouse(x, y)
                elif 50 < distance < 70:
                    self.scroll_mouse(-100 if thumb_y < y else 100)

                print(f"Screen Size: {self.screen_width}x{self.screen_height}, Gesture at ({x}, {y}) with distance {distance}")

        elements = self.detect_elements(screen)
        for element in elements.get('boxes', []):
            cv2.rectangle(screen, (element['x'], element['y']), (element['x'] + element['width'], element['y'] + element['height']), (0, 255, 0), 2)

        cv2.imshow("Screen with Hand Detection", screen)
        
        # Generate and print the description of the screen
        description = self.generate_description(screen)
        print(f"Screen Description: {description}")

    def run(self):
        self.iniciar()
        while True:
            self.process_frame()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

# Main Execution
if __name__ == "__main__":
    try:
        print("Controle Gestos e Clicks com IA")
        jarvis = LLMJARVIS()
        jarvis.run()

    except Exception as e:
        print("Something went wrong :(", e)
    finally:
        print("The 'try except' is finished")
