import cv2 as cv
import uuid

IS_MOTION_OUTLINED = os.environ.get('IS_MOTION_OUTLINED')
MOTION_THRESHOLD = os.environ.get('MOTION_THRESHOLD')


def get_contours_between_frames(frame1, frame2):
    '''Returns a list of contours between the two given frames'''

    if frame1 is None or frame2 is None:
        return []

    difference = cv.absdiff(frame1, frame2)
    gray_difference = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_difference, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours



class Video:
    def __init__(self, file):
        self.file = file
        self.processed_file = file
        self.contains_motion = None


    def check_for_and_outline_motion(self):
        cap = cv.VideoCapture(self.file)
        width = int(cap.get(3))
        height = int(cap.get(4))
        FPS = cap.get(cv.CAP_PROP_FPS)
        
        # TODO - change this to avc1 encoding
        fourcc = cv.VideoWriter(*'mp4v')
        self.processed_file = f'/tmp/{str(uuid.uuid4())}.mp4'
        video_writer = cv.VideoWriter(self.processed_file, fourcc, FPS, (width, height))
        video_writer = self.create_processed_file_video_writer(cap)

        _, frame1 = cap.read()
        _, frame2 = cap.read()
        
        while cap.isOpened() and frame1 is not None:
            contours = get_contours_between_frames(frame1, frame2)
             
            for contour in contours:
               if cv.contourArea(contour) >= MOTION_THRESHOLD:
                   self.contains_motion = True
                   cv.rectangle(frame1, (x, y), (x+w, y+h), (255, 255, 255), 1)

                   break

            video_writer.write(frame1)

            frame1 = frame2
            _, frame2 = cap.read()
        
        cap.release()
        video_writer.release()

        return self.contains_motion


    def check_for_motion(self):
        if self.contains_motion is not None:
            return self.contains_motion

        self.contains_motion = False

        if IS_MOTION_OUTLINED:
            return self.check_for_and_outline_motion()

        cap = cv.VideoCapture(self.file)

        _, frame1 = cap.read()
        _, frame2 = cap.read()
        
        while cap.isOpened() and frame1 is not None:
            contours = get_contours_between_frames(frame1, frame2)
             
            for contour in contours:
                if cv.contourArea(contour) >= MOTION_THRESHOLD:
                    self.contains_motion = True
                    return self.contains_motion

            frame1 = frame2
            _, frame2 = cap.read()

        cap.release()

        return self.contains_motion


