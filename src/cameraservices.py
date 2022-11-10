import cv2 as cv
import time
import os
from dotenv import load_dotenv
import uuid
from fileservices import create_folder

load_dotenv()

clip_length = int(os.getenv('CLIP_LENGTH', 30))
output_path = os.getenv('OUTPUT_PATH', './tmp')
camera_name = os.getenv('CAMERA_NAME', f'CAMERA_{uuid.uuid4().hex[:8]}')

def calibrate_camera():
    '''Calibrate the camera. Get the true FPS (including processing) from the camera'''
    camera = cv.VideoCapture(0)

    if not camera.isOpened():
        # Attempt to open capture device once more, after a failure
        camera.open()
        if not camera.isOpened():
            print('Unable to open camera')
            exit(1)

    start_time = time.time()
    count = 0
    while int(time.time() - start_time) < 10:
        ret, frame = camera.read()
        count += 1 # number of frames

    width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(count / 10)

    return camera, fps, width, height


def record_clip(camera, fps, width, height):
    start_time = time.time()
    folder = f"{output_path}/{time.strftime('%Y-%m-%d', time.localtime(start_time))}"
    create_folder(folder)

    filename = f"{folder}/{time.strftime('%H-%M-%S', time.localtime(start_time))}_{camera_name}.mp4"
    print('Recording clip')
   
    # Figure out if this video encoding is sufficient (I want it to work on all devices without issues)
    # This video encoding might be what I'm looking for. It looks like it is creating mp4 videos that are playing in chrome well. TODO - tesst in other browsers
    fourcc = cv.VideoWriter_fourcc(*'avc1')
    video_writer = cv.VideoWriter(filename, fourcc, fps, (width, height))


    for i in range(fps * clip_length):
        ret, frame = camera.read() # read frame from camera

        timestamp = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(time.time()))
        
        # draw the text twice to give "outline" effect (ensure the text is visible regardless of frame)
        frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv.LINE_AA)
        frame = cv.putText(frame, timestamp, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        video_writer.write(frame)

        cv.waitKey(1)
    video_writer.release()

