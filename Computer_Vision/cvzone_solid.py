import cv2
import cvzone
import numpy as np

class ShapeDetector:
    def __init__(self, url):
        self.url = url
        self.imgShapes = cvzone.downloadImageFromUrl(url)
        self.imgCanny = None
        self.imgDilated = None
        self.imgContours = None
        self.conFound = None
        self.imgContoursFiltered = None
        self.conFoundFiltered = None

    def edge_detection(self):
        self.imgCanny = cv2.Canny(self.imgShapes, 50, 150)

    def dilate_edges(self):
        self.imgDilated = cv2.dilate(self.imgCanny, np.ones((5, 5), np.uint8), iterations=1)

    def find_contours_no_filtering(self):
        self.imgContours, self.conFound = cvzone.findContours(
            self.imgShapes, self.imgDilated, minArea=1000, sort=True,
            filter=None, drawCon=True, c=(255, 0, 0), ct=(255, 0, 255),
            retrType=cv2.RETR_EXTERNAL, approxType=cv2.CHAIN_APPROX_NONE
        )

    def find_contours_filtered(self):
        self.imgContoursFiltered, self.conFoundFiltered = cvzone.findContours(
            self.imgShapes, self.imgDilated, minArea=1000, sort=True,
            filter=[3, 4], drawCon=True, c=(255, 0, 0), ct=(255, 0, 255),
            retrType=cv2.RETR_EXTERNAL, approxType=cv2.CHAIN_APPROX_NONE
        )

    def run(self):
        self.edge_detection()
        self.dilate_edges()
        self.find_contours_no_filtering()
        self.find_contours_filtered()



class contornosObjetos:
    def __init__(self):
        pass

    def createColorFinder(self):
        myColorFinder = cvzone.ColorFinder(trabckbar = True)


        
if __name__ == "__main__":
    url = 'https://github.com/cvzone/cvzone/blob/master/Results/shapes.png?raw=true'
    detector = ShapeDetector(url)
    if detector:
        print("Ok!")
    detector.run()
    # ... (process results as needed)