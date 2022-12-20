import os
from dotenv import load_dotenv
import uuid
import threading
from fileservices import create_folder, upload_files
from Camera import Camera


load_dotenv()

output_path = os.getenv('OUTPUT_PATH', './tmp')
clips_per_upload = int(os.getenv('CLIPS_PER_UPLOAD', 50))
clip_length = int(os.getenv('CLIP_LENGTH', 30))
camera_name = os.getenv('CAMERA_NAME', f'CAMERA_{uuid.uuid4().hex[:8]}')


if __name__ == '__main__':
    print(f'Output configuration:\nClips per upload: {clips_per_upload}\nClip length: {clip_length}s\nCamera name: {camera_name}')
    camera = Camera(camera_name, clip_length)

    video_writer = None

    create_folder(output_path) 

    try:
        clips_since_last_upload = 0
        uploading_thread = None
        while True:
            camera.record_clip()
            clips_since_last_upload += 1
            
            if clips_since_last_upload >= clips_per_upload:
                if uploading_thread is not None:
                    if uploading_thread.is_alive():
                        print('Thread still running in background')
                        continue
                    
                uploading_thread = threading.Thread(target=upload_files, name="FileUploader", args=(output_path,))
                uploading_thread.start()
                clips_since_last_upload = 0
            
    except Exception as e:
        print(f'An error occurred: {e}')
        if video_writer is not None:
            video_writer.release()
    camera.release()

