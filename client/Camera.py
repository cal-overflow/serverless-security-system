import cv2 as cv
import time
import os
from dotenv import load_dotenv
import uuid
from fileservices import create_folder

load_dotenv()
output_path = os.getenv('OUTPUT_PATH', './tmp')


class Camera:
    def __init__(self, camera_name, clip_length):
        self.name = camera_name
        self.clip_length = clip_length
        self.camera = None
        self.width = None
        self.height = None
        self.fps = None


    def calibrate_camera(self):
        '''Calibrate the camera. Get the true FPS (including processing) from the camera'''

        print('Calibrating camera...')
        self.camera = cv.VideoCapture(0)

        if not self.camera.isOpened():
            # Attempt to open capture device once more, after a failure
            self.camera.open()
            if not self.camera.isOpened():
                print('Unable to open camera')
                exit(1)

        start_time = time.time()
        count = 0
        while int(time.time() - start_time) < 10:
            ret, frame = self.camera.read()
            count += 1 # number of frames

        self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(count / 10)

        print(f'Camera calibration complete.\nDimensions: {self.width}x{self.height}\nFPS: {self.fps}')
        return


    def record_clip(self):
        '''Record a video clip. Will calibrate the camera if it has not already been calibrated.'''
        if self.camera is None:
            self.calibrate_camera()

        start_time = time.time()
        filename = f"{output_path}/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))}_{self.name}.mp4"
        print('Recording clip')
       
        # Figure out if this video encoding is sufficient (I want it to work on all devices without issues)
        # This video encoding might be what I'm looking for. It looks like it is creating mp4 videos that are playing in chrome well. TODO - tesst in other browsers
        fourcc = cv.VideoWriter_fourcc(*'avc1')
        video_writer = cv.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))


        for i in range(self.fps * self.clip_length):
            ret, frame = self.camera.read() # read frame from camera

            timestamp = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(time.time()))
            
            # draw the text twice to give "outline" effect (ensure the text is visible regardless of frame)
            frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv.LINE_AA)
            frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            video_writer.write(frame)

            cv.waitKey(1)
        video_writer.release()


    def release(self):
        if self.camera is not None:
            self.camera.release()

