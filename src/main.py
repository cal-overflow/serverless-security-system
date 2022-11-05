import cv2 as cv
import time
import os
from fileservices import create_folder

clip_length = int(os.getenv('CLIP_LENGTH', 30))
output_path = os.getenv('OUTPUT_PATH', './tmp')

def calibrate_camera():
    '''Calibrate the camera. Get the true FPS (including processing) from the camera'''
    camera = cv.VideoCapture(0)

    if not camera.isOpened():
        # Attempt to open capture device once more, after a failure
        camera.open()
        if not camera.isOpened():
            print('Unable to open camera')
            exit()

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

    filename = f"{folder}/{time.strftime('%H-%M-%S', time.localtime(start_time))}.mp4"
    print(f'New file: {filename}')
   
    # Figure out if this video encoding is sufficient (I want it to work on all devices without issues)
    video_writer = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'mp4v'), fps, (width, height))


    for i in range(fps * clip_length):
        ret, frame = camera.read() # read frame from camera
        frame = cv.putText(frame, time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(time.time())), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv.LINE_AA)
        video_writer.write(frame)

        cv.waitKey(1)
    video_writer.release()


if __name__ == '__main__':
    print('Calibrating camera...')
    camera, fps, width, height = calibrate_camera()
    print(f'Camera calibration complete.\nDimensions: {width}x{height}\nFPS: {fps}')
    print(f'Creating {clip_length} second video clips')

    video_writer = None

    create_folder(output_path)

    try:
        while True:
            record_clip(camera, fps, width, height)
    except Exception as e:
        print(f'An error occurred: {e}')
        if video_writer is not None:
            video_writer.release()
    camera.release()

