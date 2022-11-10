import os
from dotenv import load_dotenv
import uuid
import asyncio
from fileservices import create_folder, upload_files
from cameraservices import calibrate_camera, record_clip


load_dotenv()

output_path = os.getenv('OUTPUT_PATH', './tmp')
clips_per_upload = int(os.getenv('CLIPS_PER_UPLOAD', 50))


if __name__ == '__main__':
    print('Calibrating camera...')
    camera, fps, width, height = calibrate_camera()
    print(f'Camera calibration complete.\nDimensions: {width}x{height}\nFPS: {fps}')

    video_writer = None

    create_folder(output_path) 

    try:
        clips_since_last_upload = 0
        while True:
            record_clip(camera, fps, width, height)
            clips_since_last_upload += 1
            
            if clips_since_last_upload >= clips_per_upload:
                asyncio.run(upload_files(output_path))
                clips_since_last_upload = 0
    except Exception as e:
        print(f'An error occurred: {e}')
        if video_writer is not None:
            video_writer.release()
    camera.release()

