import classifier
from classifier import CLASS_DICT
import image_reader

import time

def run_test():
    model_path = '/home/adiga/my_work/arecanut-images/areca_classifier/model/model_20201126_1448'
    url = "rtsp://192.168.1.100:8080/h264_ulaw.sdp"

    predictor = classifier.Predictor(model_path)
    img_reader = image_reader.ImageReader(url)

    print('Starting the test')
    while True:
        (has_frame,frame_np) = img_reader.get_a_frame()
        if has_frame:
            pred = predictor.predict_on_frame(frame_np)
            print('Prediction:', CLASS_DICT[pred])
            # Wait for 2 seconds
            time.sleep(5)
        else:
            print('No frame captured! Exiting now..')
            img_reader.close()
            break

    print('Done with the test')

if __name__ == "__main__":
    run_test()
