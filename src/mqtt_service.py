import paho.mqtt.client as mqtt

class MqttService:
    def __init__(self, topic, host='localhost', port=1883):
        self.topic = topic
        self.client = mqtt.Client()
        self.client.connect(host, port, 60)
        print('MQTT:Connected to {}:{}'.format(host, port))
    
    def publish(self, message):
        """Publishes the given message on the topic

        Args:
            message (str): Message
        """
        self.client.publish(self.topic, message)

    def subscribe_and_wait(self, subscriber):
        """Registers the subscriber method to the given topic and waits indefinitely for the messages.
        The message 'END' is a special message that terminates the subscriber and the infinite loop.

        Args:
            subscriber (method): Callback method of signature: subscriber(message: str) to be called on receipt of a message
        """
        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            if message == 'END':
                print('Received END. Terminating.')
                self.close()
            else:
                subscriber(message)
        
        # Subscribe and register the callback method
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        print('Subscribed to {}'.format(self.topic))
        self.client.loop_forever()

    def close(self):
        self.client.disconnect()
        print('MQTT service closed.')

if __name__ == "__main__":
    ms = MqttService("test")

    def on_msg(msg):
        print('Received:', msg)

    ms.subscribe_and_wait(on_msg)
    #ms.publish("tadaa")