import cvzone
import cv2
import numpy as np

class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def close(self):
        self.cap.release()

class ImageProcessor:
    def __init__(self, webcam):
        self.webcam = webcam
        self.img = None

    def process(self):
        ret, frame = self.webcam.get_frame()
        if ret:
            self.img = frame
            self.process_image()

    def process_image(self):
        # Example of using the stackImages function
        imgList = [self.img, cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)]
        self.img = cvzone.stackImages(imgList, 2, 0.8)

        # Example of using the cornerRect function
        bbox = (200, 200, 300, 200)
        self.img = cvzone.cornerRect(self.img, bbox, l=30, t=5, rt=1,
                                    colorR=(255, 0, 255), colorC=(0, 255, 0))

        # Example of using the rotateImage function
        self.img = cvzone.rotateImage(self.img, 60, scale=1, keepSize=True)

        # Example of using the overlayPNG function
        img_path  = "/home/pedrov/Documentos/GitHub/IA-Imersao-Alura/Computer_Vision/cv_zone_Modules/cvzoneLogo.png"
        imgPNG = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        self.img = cvzone.overlayPNG(self.img, imgPNG, pos=[-30, 100])

        # Example of using the findContours function
        imgCanny = cv2.Canny(self.img, 50, 150)
        imgDilated = cv2.dilate(imgCanny, np.ones((5, 5), np.uint8), iterations=1)
        self.img, _ = cvzone.findContours(self.img, imgDilated, minArea=1000, sort=True,
                                        filter=None, drawCon=True, c=(255, 0, 0), ct=(255, 0, 255),
                                        retrType=cv2.RETR_EXTERNAL, approxType=cv2.CHAIN_APPROX_NONE)

        # Example of using the putTextRect function
        self.img, _ = cvzone.putTextRect(self.img, "CVZone", (50, 50),
                                        scale=3, thickness=3,
                                        colorT=(255, 255, 255), colorR=(255, 0, 255),
                                        font=cv2.FONT_HERSHEY_PLAIN, offset=10,
                                        border=5, colorB=(0, 255, 0))

if __name__ == "__main__":
    webcam = Webcam()
    img_processor = ImageProcessor(webcam)

    while True:
        img_processor.process()
        cv2.imshow("Image", img_processor.img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.close()