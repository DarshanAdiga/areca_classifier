import classifier
from classifier import CLASS_DICT
import image_reader
import category_controller

import time

def run_test():
    model_path = 'model/model_20201126_1448'
    url = "rtsp://192.168.1.100:8080/h264_ulaw.sdp"

    PREDICTION_DELAY_SEC = 1 

    predictor = classifier.Predictor(model_path)
    img_reader = image_reader.ImageReader(url)
    category_controller = CategoryController()

    print('Starting the test')
    while True:
        (has_frame,frame_np) = img_reader.get_a_frame()
        if has_frame:
            pred = predictor.predict_on_frame(frame_np)
            print('Prediction:', CLASS_DICT[pred])
            
            # Move the controller based on predictions
            category_controller.move_controller(pred)

            # Wait for few seconds
            time.sleep(PREDICTION_DELAY_SEC)
        else:
            print('No frame captured! Exiting now..')
            img_reader.close()
            break

    print('Done with the test')

if __name__ == "__main__":
    run_test()
