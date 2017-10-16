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
        self.url = 'http://192.168.1.4:8080/shot.jpg'

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
        totalFrame = 0
        savedFrame = 0
        frameNo = 1

        label_array = np.zeros((1,4))
        image_array = np.zeros((1,38400))

        pygame.display.set_mode((1, 1))
        flag = True
        while flag:

            imgResp = urllib.request.urlopen(self.url)
            #covert image respose to bytearray and datatype is usigned int 8B
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            image = cv2.imdecode(imgNp, -1)
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Camera', img)

            # select lower half of image
            roi = img[120:240, :]

            # cv2.imshow('ROT',roi)

            # save image
            if not os.path.exists('training_images'):
                os.makedirs('training_images')
            try:
                cv2.imwrite('training_images/frame{:05}.jpg'.format(frameNo),img)
            except IOError as e:
                print(e)

            # roi image into one row 120X320=38400
            temp_array = roi.reshape(1, 38400).astype(np.float32)
            print(temp_array)
            frameNo = frameNo + 1
            totalFrame += 1

            # input from human
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[1]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[0]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")

                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[2]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_DOWN]:
                        print("Down")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[3]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[0]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        image_array = np.vstack((image_array,temp_array))
                        label_array = np.vstack((label_array,self.labels[1]))
                        savedFrame += 1
                        #signal to ardunio

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("exit")
                        flag = False
                        break
                elif event.type == pygame.KEYUP:
                    #print("ssd")
        #saving labels
        train_images = image_array[1:,:] #for removing first entry
        train_labels = label_array[1:,:]

        #save training data as a np file
        file_name = str(int(time.time()))
        directory = "training_data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            np.savez(directory + '/' + file_name + '.npz', train_images=train_images, train_labels=train_labels)
        except IOError as e:
            print(e)

        print(train_images.shape)
        print(train_labels.shape)
        print('Total frame: ', + totalFrame)
        print('Saved frame: ', + savedFrame)
        print('Dropped frame :', + totalFrame - savedFrame)




if __name__ == '__main__':
    CollectTrainingData()
