import cv2
import threading
import time

class CameraThread(threading.Thread):
    def __init__(self, camera):
        self.camera = camera
        self.last_frame = None
        self.be_live = True

        super(CameraThread, self).__init__()
        print('Going to start the camera thread')
        self.start()
    
    def run(self):
        while self.be_live:
            ret, self.last_frame = self.camera.read()

    def close(self):
        self.be_live = False

class ImageReader:
    def __init__(self, url):
        self.url = url
        # open the feed
        self.cap = cv2.VideoCapture(url)
        print('Connected to {}'.format(url))
        self.camera_thread = CameraThread(self.cap)
        time.sleep(1) # Wait for the thread to start
        
    def get_a_frame(self):
        """Returns a tuple (has_frame, frame) 
           has_frame Boolean: True if frame was captured, False otherwise
           frame Numpy: Image in numpy array format
           """
        # read next frame, Returns (Boolean,Numpy Array)
        return (self.camera_thread.last_frame is not None), self.camera_thread.last_frame
    
    def save_a_frame(self, file_path):
        has_frame,frame = self.get_a_frame()
        
        if has_frame:
            cv2.imwrite(file_path, frame)
            print("Saved at {}".format(file_path))
            return True
        else:
            print('Camera feed not available!')
            return False
        
    def close(self):
        # close the connection and close all windows
        self.camera_thread.close()
        self.camera_thread.join()

        self.cap.release()
        cv2.destroyAllWindows()
        print('Closed the connection')


if __name__ == "__main__":
    url = "rtsp://192.168.1.101:8080/h264_ulaw.sdp"
    img_reader = ImageReader(url)
    counter = 0
    while counter <= 30:
        counter += 1
        img_reader.save_a_frame('/tmp/debug_imgs/{}.png'.format(counter))
        time.sleep(1)
    
    img_reader.close()