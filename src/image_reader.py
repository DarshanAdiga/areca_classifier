import cv2

class ImageReader:
    def __init__(self, url):
        self.url = url
        # open the feed
        self.cap = cv2.VideoCapture(url)
        print('Connected to {}'.format(url))
        
    def get_a_frame(self):
        """Returns a tuple (has_frame, frame) 
           has_frame Boolean: True if frame was captured, False otherwise
           frame Numpy: Image in numpy array format
           """
        # read next frame
        has_frame, frame = cap.read() # Returns (Boolean,Numpy Array)
        return has_frame,frame
    
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
        self.cap.release()
        cv2.destroyAllWindows()
        print('Closed the connection')