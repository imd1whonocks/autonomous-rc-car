import urllib.request
import cv2
import numpy as np
import time
import pygame
from pygame.locals import *
import os

# collect training data

class CollectTrainingData(object):
    def __init__(self):
        self.url = 'http://192.168.43.1:8080/shot.jpg'

        # create serial connection with board

        # create labels
        # [Left Right Forward Back]
        self.labels = np.zeros((4, 4), 'float')
        for i in range(4):
            self.labels[i, i] = 1
        # label[0] for left,1 for right,2 for forward,3 for reverse
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):


        frameNo = 1
        flag = True
        pygame.display.set_mode((1, 1))
        while flag:

            imgResp = urllib.request.urlopen(self.url)
            #covert image respose to bytearray and datatype is usigned int 8B
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            image = cv2.imdecode(imgNp, -1)
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Original', img)
            # select lower half of image
            roi = img[120:240, :]
            # cv2.imshow('ROT',roi)
            # save image
            cv2.imwrite('training_images/frame{:05}.jpg'.format(frameNo),img)

            # roi image into one row 120X320=38400
            temp_array = roi.reshape(1, 38400).astype(np.float32)
            frameNo = frameNo + 1

            # input from human

            for event in pygame.event.get():
                print(event)
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    print(key_input)

                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")

                    elif key_input[pygame.K_UP]:
                        print("Forward")

                    elif key_input[pygame.K_DOWN]:
                        print("Down")

                    elif key_input[pygame.K_LEFT]:
                        print("Left")

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("exit")
                        flag = False
                        break
                elif event.type == pygame.KEYUP:
                    print("ssd")


if __name__ == '__main__':
    CollectTrainingData()
