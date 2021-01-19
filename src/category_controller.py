from stepper_controller import StepperController
from classifier import GOOD, BAD, CLASS_DICT

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
    import time
    cc = CategoryController()
    
    print('Moving GOOD')
    cc.move_controller(GOOD)
    time.sleep(3)

    print('Moving BAD')
    cc.move_controller(BAD)
    time.sleep(3)

    print('Moving GOOD')
    cc.move_controller(GOOD)
    time.sleep(3)

    print('Moving BAD')
    cc.move_controller(BAD)
    time.sleep(3)