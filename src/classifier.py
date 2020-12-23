import os
import random
import numpy as np
from datetime import datetime

import keras
from keras.models import load_model

from PIL import Image, ImageOps
import cv2

#-----------Configurations expected by the model------------
#Pixel coordinates for the crop, Left,Top,Right,Bottom 
I_WIDTH, I_HEIGHT = (1080, 2336)
STD_CROP_LTRB = (0, 650, I_WIDTH, I_HEIGHT-750)
# Std size expected by the model
STD_SHAPE = (256, 256)

# Dict to decode the predictions
CLASS_DICT = {0: 'GOOD', 1: 'BAD'}
#-----------------------------------------------------------

class Predictor:
    def __init__(self, model_path, debug=0, debug_img_loc='/tmp/debug_imgs/'):
        """Initializes the image classifier

        Args:
            model_path (str): Model file to be loaded
            debug (int, optional): Indicates debug level, possible values [0,1,2,3]. 0 indicates no debug, 3 indicates full debug. Defaults to 0.

            debug_img_loc (str, optional): Location where images and predictions to be saved. Defaults to '/tmp/debug_imgs/'.
        """
        self.model = self.__load_model(model_path)
        print('Loaded the model from {}'.format(model_path))
        
        # Debugging settings
        self.debug_img_loc = debug_img_loc
        self.debug = debug % 4 # To truncate between 0 and 3
        # For storing the debug images
        if debug > 0 and not os.path.exists(debug_img_loc):
            os.makedirs(debug_img_loc)

    def __load_model(self, model_path):
        model = load_model(model_path)
        return model

    def __crop_to_std_size(self, img):
        """Crop the image to a standard size"""
        return img.crop(STD_CROP_LTRB)

    def __reshape_to_std_size(self, img):
        """Reshape the image to a standard size"""
        return img.resize(STD_SHAPE)
    
    def __transform_np_image(self, frame_np):
        """Transforms and converts the numpy image data 'frame_np' and returns image in numpy format
        frame_np: Image in numpy array format
        """
        # Load image from numpy array
        img = Image.fromarray(frame_np)
        img = self.__crop_to_std_size(img)
        img = self.__reshape_to_std_size(img)
        # Convert back to numpy
        return np.array(img)

    def __save_frame(self, frame_np, trans_np, pred):
        """Save the given raw frame, transformed image along with the prediction value
        """
        dt = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        pred = CLASS_DICT[pred]
        # Prepare the iamge file names
        frame_path = '{}_frame_{}.png'.format(dt, str(pred))
        trans_path = '{}_trans_{}.png'.format(dt, str(pred))
        # Save the images
        cv2.imwrite(self.debug_img_loc + frame_path, frame_np)
        cv2.imwrite(self.debug_img_loc + trans_path, trans_np)

    def __save_frame_randomly(self, frame_np, img_np, pred):
        """Save the raw frame, transformed image and the predictions for debugging purpose"""
        
        # Depending on debug level, randomly decide whether to save these images and results
        # Goal: higher the debug, higher should be the chance of debug  
        inv = 4 - self.debug # Invert the debug value 
        rnum = random.randint(1, inv+1) # any num between 1 to 3 inclusive
        if rnum == 1: # chances will be lesser as inv is heigher
            # Save the frame and results
            self.__save_frame(frame_np, img_np, pred)

    def predict_on_frame(self, frame_np):
        """Run the predictions on the given 'frame_np'. 

        Args:
            frame_np (Numpy): Usually frame_np will be an image frame read from a camera.
            
        Returns:
            int: Indicating the predicted class. It can be decoded using CLASS_DICT.
        """

        # Transform the image
        img_np = self.__transform_np_image(frame_np)
        # Run predictions
        img_np = np.array([img_np])
        pred = self.model.predict(img_np)
        pred = np.argmax(pred, axis=1)[0]
        # Optionally save the input and output
        if self.debug > 0:
            self.__save_frame_randomly(frame_np, img_np, pred)
        
        # Return the predicted class
        return pred
