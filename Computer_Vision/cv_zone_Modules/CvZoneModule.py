import cv2
import numpy as np
import urllib.request

class CVZone:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def stackImages(self, imgList, cols, scale):
        width1, height1 = imgList[0].shape[1], imgList[0].shape[0]
        totalImages = len(imgList)
        rows = totalImages // cols if totalImages // cols * cols == totalImages else totalImages // cols + 1
        blankImages = cols * rows - totalImages
        imgBlank = np.zeros((height1, width1, 3), np.uint8)
        imgList.extend([imgBlank] * blankImages)
        for i in range(cols * rows):
            imgList[i] = cv2.resize(imgList[i], (width1, height1), interpolation=cv2.INTER_AREA)
            imgList[i] = cv2.resize(imgList[i], (0, 0), None, scale, scale)
            if len(imgList[i].shape) == 2:
                imgList[i] = cv2.cvtColor(imgList[i], cv2.COLOR_GRAY2BGR)
        hor = [imgBlank] * rows
        for y in range(rows):
            line = []
            for x in range(cols):
                line.append(imgList[y * cols + x])
            hor[y] = np.hstack(line)
        ver = np.vstack(hor)
        return ver

    def cornerRect(self, img, bbox, l=30, t=5, rt=1, colorR=(255, 0, 255), colorC=(0, 255, 0)):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        if rt!= 0:
            cv2.rectangle(img, bbox, colorR, rt)
        cv2.line(img, (x, y), (x + l, y), colorC, t)
        cv2.line(img, (x, y), (x, y + l), colorC, t)
        cv2.line(img, (x1, y), (x1 - l, y), colorC, t)
        cv2.line(img, (x1, y), (x1, y + l), colorC, t)
        cv2.line(img, (x, y1), (x + l, y1), colorC, t)
        cv2.line(img, (x, y1), (x, y1 - l), colorC, t)
        cv2.line(img, (x1, y1), (x1 - l, y1), colorC, t)
        cv2.line(img, (x1, y1), (x1, y1 - l), colorC, t)
        return img

    def findContours(self, img, imgPre, minArea=1000, maxArea=float('inf'), sort=True, filter=None, drawCon=True, c=(255, 0, 0), ct=(255, 0, 255), retrType=cv2.RETR_EXTERNAL, approxType=cv2.CHAIN_APPROX_NONE):
        conFound = []
        imgContours = img.copy()
        contours, hierarchy = cv2.findContours(imgPre, retrType, approxType)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if minArea < area < maxArea:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                if filter is None or len(approx) in filter:
                    if drawCon:
                        cv2.drawContours(imgContours, cnt, -1, c, 3)
                        x, y, w, h = cv2.boundingRect(approx)
                        cv2.putText(imgContours, str(len(approx)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ct, 2)
                    cx, cy = x + (w // 2), y + (h // 2)
                    cv2.rectangle(imgContours, (x, y), (x + w, y + h), c, 2)
                    cv2.circle(imgContours, (x + (w // 2), y + (h // 2)), 5, c, cv2.FILLED)
                    conFound.append({"cnt": cnt, "area": area, "bbox": [x, y, w, h], "center": [cx, cy]})
        if sort:
            conFound = sorted(conFound, key=lambda x: x["area"], reverse=True)
        return imgContours, conFound

    def overlayPNG(self, imgBack, imgFront, pos=[0, 0]):
        hf, wf, cf = imgFront.shape
        hb, wb, cb = imgBack.shape
        *pos, yf, xf = pos
        for i in range(hf):
            for j in range(wf):
                if imgFront[i, j][3]!= 0:
                    imgBack[yf + i, xf + j] = imgFront[i, j][:3]
        return imgBack

    def rotateImage(self, imgInput, angle, scale=1, keepSize=False):
        (h, w) = imgInput.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), angle, scale)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        if keepSize:
            imgOutput = cv2.warpAffine(imgInput, M, (w, h))
        else:
            imgOutput = cv2.warpAffine(imgInput, M, (nW, nH))
        return imgOutput

    def putTextRect(self, img, text, pos, scale=3, thickness=3, colorT=(255, 255, 255), colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN, offset=10, border=None, colorB=(0, 255, 0)):
        x, y = pos
        (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
        img = cv2.rectangle(img, (x, y + offset), (x + w, y - h + offset), colorR, cv2.FILLED)
        if border is not None:
            cv2.rectangle(img, (x, y + offset), (x + w, y - h + offset), colorB, border)
        cv2.putText(img, text, (x, y), font, scale, colorT, thickness)
        return img

    def downloadImageFromUrl(self, url, keepTransparency=False):
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        if keepTransparency:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    
    def exemplo_stack_imagens(self):
        cap = cv2.VideoCapture(0)
        
        
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to capture image from camera. Exiting...")
                break
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgSmall = cv2.resize(img, (0, 0), None, 0.1, 0.1)
            imgBig = cv2.resize(img, (0, 0), None, 3, 3)
            imgCanny = cv2.Canny(imgGray, 50, 150)
            imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            imgList = [img, imgGray, imgCanny, imgSmall, imgBig, imgHSV]
            stackedImg = self.stackImages(imgList, 3, 0.7)
            cv2.imshow("stackedImg", stackedImg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def main(self):
        while True:
            success, img = self.cap.read()
            choice = int(input("Enter 1 for Gestures, 2 for Stack Images: "))
            if choice == 1:
                # Implement gesture-based functionality here
                pass
            elif choice == 2:
                # Implement stack images functionality here
                self.exemplo_stack_imagens()
                pass
            else:
                print("Invalid choice. Please enter 1 or 2.")
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()



def exemplo_stack_imagens():
    cap = cv2.VideoCapture(0)
    
    cvzone = CVZone()
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera. Exiting...")
            break
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgSmall = cv2.resize(img, (0, 0), None, 0.1, 0.1)
        imgBig = cv2.resize(img, (0, 0), None, 3, 3)
        imgCanny = cv2.Canny(imgGray, 50, 150)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        imgList = [img, imgGray, imgCanny, imgSmall, imgBig, imgHSV]
        stackedImg = cvzone.stackImages(imgList, 3, 0.7)
        cv2.imshow("stackedImg", stackedImg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cv_zone = CVZone()
    cv_zone.main()
    
