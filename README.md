# Areca Classifier
A proof-of-concept showcasing the applicability of deep learning for classifying good and bad quality arecanuts.  


| Good Image    | Bad Image    |
| - | - |
| <img src="sample_data/img_good/good-20201125_210407.mp4-135.jpeg" alt="Good Image" style="float: center; margin-right: 10px;" width="100" height="300" /> | <img src="sample_data/img_bad/bad-20201123_205649.mp4-117.jpeg" alt="Bad Image" style="float: center; margin-right: 10px;" width="100" height="300" />|


This project has two components Prediction Component and a Stepper Motor Controller.

## Image Reader and Prediction Component
This is my personal laptop capable of loading the Keras model, streaming the IP Camera video stream and a MQTT broker.
The entry point of this component is `runner.py`.

## Stepper Motor Controller
This is the RaspberryPi 4 that listens to the MQTT topic and controls the stepper motor.
The entry point of this component is `category_controller.py`.

## How to run the project
Follow the below steps in the exact order.

1. Run the Stepper Motor controller:
    ```bash
    python src/category_controller.py
    ```
2. Start the IP Camera
3. Run the Image Reader & Prediction component:
    ```bash
    python src/runner.py
    ```