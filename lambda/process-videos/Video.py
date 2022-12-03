import cv2 as cv

THRESHOLD = 7500 # Movement detection threshold


class Video:
    def __init__(self, file):
        self.file = file
        self.contains_motion = None

    def check_for_motion(self):
        self.contains_motion = False
        cap = cv.VideoCapture(self.file)

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        
        while cap.isOpened() and frame1 is not None:
            difference = cv.absdiff(frame1, frame2)
            gray_difference = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray_difference, (5, 5), 0)
            __, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
            dilated = cv.dilate(thresh, None, iterations=3)
            contours, __ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv.contourArea(contour) >= THRESHOLD:
                    self.contains_motion = True
                    return

            frame1 = frame2
            ret, frame1 = cap.read()

        return

