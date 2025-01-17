import serial
import pygame
from pygame.locals import *

class RCTest(object):

    def __init__(self):
        pygame.init()
        
        self.ser = serial.Serial('COM3', 250000, timeout=1)
        self.send_inst = True
        self.steer()

    def steer(self):
        pygame.display.set_mode((1, 1))
        print('hi')
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.ser.write(b'right\n')

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        self.ser.write(b'left\n')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.ser.write(b'brake\n')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.ser.write(b'brake\n')

                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        self.ser.write(b'forward\n')

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.ser.write(b'brake\n')

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.ser.write(b'right\n')

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.ser.write(b'left\n')

                    #exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print ('Exit')
                        self.send_inst = False
                        #self.ser.write(b'')
                        self.ser.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(b'')

if __name__ == '__main__':
    RCTest()