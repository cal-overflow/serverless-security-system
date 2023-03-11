import cv2 as cv
import time
import os
import logging
from dotenv import load_dotenv
import uuid
from fileservices import create_folder


load_dotenv()
output_path = os.getenv('OUTPUT_PATH', './tmp')
WIDTH = int(os.getenv('WIDTH', '0'))
HEIGHT = int(os.getenv('HEIGHT', '0'))


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



class Camera:
    def __init__(self):
        self.camera = None
        self.width = WIDTH
        self.height = HEIGHT
        self.fps = None


    def calibrate(self):
        '''Calibrate the camera. Get the true FPS (including processing) from the camera'''

        logging.info('Calibrating camera...')
        self.camera = cv.VideoCapture(0)

        if not self.camera.isOpened():
            # Attempt to open capture device once more, after a failure
            self.camera.open()
            if not self.camera.isOpened():
                logging.error('Unable to open camera')
                exit(1)

        start_time = time.time()
        count = 0
        while int(time.time() - start_time) < 10:
            _, _ = self.camera.read()
            count += 1 # number of frames

        if self.width == 0 or self.height == 0:
            self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))

        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        self.fps = int(count / 10)
        self.camera.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG')) # this fourcc allows for faster processing - https://stackoverflow.com/a/74234176

        logging.info(f'Camera calibration complete - {self.width}x{self.height} at {self.fps} fps')
        return


    def record_clip(self, settings):
        '''Record a video clip. Will calibrate the camera if it has not already been calibrated.'''
        if self.camera is None:
            self.calibrate()

        motion_threshold = settings['camera']['motion_threshold'] if 'camera' in settings else settings['default_motion_threshold']
        is_motion_outlined = settings['is_motion_outlined']

        start_time = time.time()
        temp_video_filename = f"{output_path}/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))}.mp4"
       
        fourcc = cv.VideoWriter_fourcc(*'avc1')
        video_writer = cv.VideoWriter(temp_video_filename, fourcc, self.fps, (self.width, self.height))


        prev_frame = None
        contains_motion = False

        for i in range(self.fps * settings['clip_length']):
            _, frame = self.camera.read() # read frame from camera
            frame_copy = frame.copy() # Copy the previous frame before the timestamp or motion-outline boxes are drawn
            timestamp = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(time.time()))


            if prev_frame is not None:
                contours = get_contours_between_frames(frame, prev_frame)

                for contour in contours:
                   if cv.contourArea(contour) >= motion_threshold:
                       if not contains_motion:
                           contains_motion = True
                       if is_motion_outlined:
                           (x, y, w, h) = cv.boundingRect(contour)
                           cv.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 1)

                       break

            # Draw a timestamp on the frame
            # draw twice to give "outline" effect (ensure the text is visible regardless of frame)
            frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv.LINE_AA)
            frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            video_writer.write(frame)

            prev_frame = frame_copy

            cv.waitKey(1)

        video_writer.release()

        if contains_motion and settings['days_to_keep_motionless_videos'] == 0:
            os.rm(temp_video_filename)
            return

        motion_flag = "CONTAINS-MOTION" if contains_motion else "NO-MOTION"
        completed_video_filename = f"{output_path}/completed/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))}_{motion_flag}.mp4"
        os.rename(temp_video_filename, completed_video_filename)



    def release(self):
        if self.camera is not None:
            self.camera.release()

