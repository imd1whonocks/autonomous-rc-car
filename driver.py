import urllib.request
import serial
import cv2
import numpy as np

class NeuralNetwork(object):
    def __init__(self):
        self.model = cv2.ANN_MLP()

    def create(self):
        #to be changed
        layer_size = np.int32([38400, 32, 4])
        self.model.create(layer_size)
        self.model.load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)


class RCControl(object):
    def __init__(self):
        self.car = serial.Serial('COM5', 250000, timeout=1)

    def steer(self, prediction):
        if prediction == 0:
            self.car.write(b'forward\n')
            print("Forward")
        elif prediction == 3:
            self.car.write(b'left\n')
            print("Left")
        elif prediction == 1:
            self.car.write(b'right\n')
            print("Right")
        elif prediction == 2:
            self.car.write(b'reverse\n')
            print("Reverse")
        else:
            self.stop()
            print("Stop")

    def stop(self):
        self.car.write(b'stop\n')


class Driver():
    model = NeuralNetwork()
    model.create()
    rc_car = RCControl()
    url = 'http://192.168.1.4:8080/shot.jpg'
    def handle(self):
        try:
            while True:
                imgResp = urllib.request.urlopen(url)

                # covert image respose to bytearray and datatype is usigned int 8B
                imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                image = cv2.imdecode(imgNp, -1)
                cv2.imshow('Camera',image)
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # select lower half of image
                roi = img_gray[120:240, :]

                # roi image into one row 120X320=38400
                image_array = roi.reshape(1, 38400).astype(np.float32)

                # neural network makes prediction
                prediction = self.model.predict(image_array)
                self.rc_car.steer(prediction)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.rc_car.stop()
                    break
            cv2.destroyAllWindows()
        finally:
            print("Connection closed")


if __name__ == '__main__':
    Driver()
