import os
from dotenv import load_dotenv
import time
import threading
from fileservices import create_folder, upload_files, get_and_parse_settings_file
from Camera import Camera


load_dotenv()
output_path = os.getenv('OUTPUT_PATH', './tmp')



def sync_configuration():
    global settings
    settings = get_and_parse_settings_file()

    global time_since_last_config_sync
    time_since_last_config_sync = time.time()

    print(f'---\nConfiguration synced:\nClips per upload: {settings["clips_per_upload"]}\nClip length: {settings["clip_length"]}s\nOutline motion: {settings["is_motion_outlined"]}\n---\n')


if __name__ == '__main__':
    sync_configuration()

    camera = Camera()

    create_folder(output_path) 

    try:
        clips_since_last_upload = 0
        uploading_thread = None
        while True:
            if time_since_last_config_sync < time.time() - 3600:
                settings_sync_thread = threading.Thread(target=sync_configuration, name="SettingsSyncer", args=())
                settings_sync_thread.start()

            camera.record_clip(settings['clip_length'], settings['is_motion_outlined'])
            clips_since_last_upload += 1
            
            if clips_since_last_upload >= settings['clips_per_upload']:
                if uploading_thread is not None:
                    if uploading_thread.is_alive():
                        continue
                    
                uploading_thread = threading.Thread(target=upload_files, name="FileUploader", args=(output_path,))
                uploading_thread.start()
                clips_since_last_upload = 0
            
    except Exception as e:
        print(f'An error occurred: {e}')
    camera.release()

