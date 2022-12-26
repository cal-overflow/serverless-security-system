import os
from dotenv import load_dotenv
import time
import threading
from fileservices import create_folder, get_camera_id, upload_videos, get_and_parse_settings_files
from Camera import Camera
import logging


load_dotenv()
output_path = os.getenv('OUTPUT_PATH', './tmp')
completed_video_output_path = f'{output_path}/completed'

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)




def sync_configuration():
    global camera_id
    global settings
    global time_since_last_config_sync


    if 'camera_id' not in globals(): # if the camera_id has not already been fetched
        camera_id = get_camera_id()

    settings = get_and_parse_settings_files(camera_id)
    time_since_last_config_sync = time.time()

    logging.info('Configuration synced')


if __name__ == '__main__':
    sync_configuration()

    camera = Camera()
    camera.calibrate()

    create_folder(completed_video_output_path) 

    try:
        clips_since_last_upload = 0
        uploading_thread = None

        logging.info('Beginning footage capture')
        while True:
            if time_since_last_config_sync < time.time() - 3600:
                settings_sync_thread = threading.Thread(target=sync_configuration, name="SettingsSyncer", args=())
                settings_sync_thread.start()

            camera.record_clip(settings)
            clips_since_last_upload += 1
            
            if clips_since_last_upload >= settings['clips_per_upload']:
                if uploading_thread is not None:
                    if uploading_thread.is_alive():
                        continue
                    
                uploading_thread = threading.Thread(target=upload_videos, name="VideoUploader", args=(completed_video_output_path, camera_id,))
                uploading_thread.start()
                clips_since_last_upload = 0
            
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    camera.release()

