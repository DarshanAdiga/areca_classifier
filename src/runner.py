import classifier
from classifier import CLASS_DICT
import image_reader
from mqtt_service import MqttService

import time

def run_test():
    model_path = 'model/model_20201126_1448'
    url = "rtsp://192.168.1.101:8080/h264_ulaw.sdp"
    
    PREDICTION_DELAY_SEC = 1 
    
    predictor = classifier.Predictor(model_path, debug=3)
    img_reader = image_reader.ImageReader(url)
    
    MQTT_BROKER_HOST = "localhost"
    MQTT_TOPIC = "areca"
    m_publisher = MqttService(MQTT_TOPIC, host=MQTT_BROKER_HOST)

    print('Starting the test')
    while True:
        # WARN: Initializing ImageReader everytime is a hack!
        (has_frame,frame_np) = img_reader.get_a_frame()
        if has_frame:
            pred = predictor.predict_on_frame(frame_np)
            print('Prediction:', CLASS_DICT[pred])
            
            # Send the MQTT message 
            m_publisher.publish(str(pred))

            # Wait for few seconds
            time.sleep(PREDICTION_DELAY_SEC)
        else:
            print('No frame captured! Exiting now..')
            img_reader.close()
            # Stop the subscriber as well
            m_publisher.publish('END')
            m_publisher.close()
            break

    print('Done with the test')

if __name__ == "__main__":
    run_test()
