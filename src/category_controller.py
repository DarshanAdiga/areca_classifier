from stepper_controller import StepperController
from classifier import GOOD, BAD, CLASS_DICT
from mqtt_service import MqttService

class CategoryController():
    def __init__(self):
        self.stepper_controller = StepperController()
        self.current_category = BAD # The index of CLASS_DICT dictionary, default to BAD category
        
    
    def move_controller(self, category):
        """Move the stepper controller towards the category

        Args:
            category (int): Index of CLASS_DICT indicating the predicted category
        """

        if category == self.current_category:
            return None # Nothing to do here

        # Else
        if category == GOOD:
            # Move forward from bad to good category
            self.stepper_controller.forward()
        else :
            # Move backward from good to bad category
            self.stepper_controller.backward()
        
        # Update the current state of the controller
        self.current_category = category
        return None

if __name__ == '__main__':
    category_controller = CategoryController()

    MQTT_BROKER_HOST = "localhost"
    MQTT_TOPIC = "areca"
    m_subscriber = MqttService(MQTT_TOPIC, host=MQTT_BROKER_HOST)

    def on_message(msg):
        """Receive the MQTT message and move the controller"""
        pred = int(msg)
        print('Received:', str(pred))
        category_controller.move_controller(pred)

    # Register and wait continuously for the messages
    m_subscriber.subscribe_and_wait(on_message)