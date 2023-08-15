import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
# import cv2

x_size = 720
y_size = 480

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

image_save = False
model = load_model('best_model.h5')
labels = {0:'zero', 1:'one',
          2:'two', 3:'three',
          4:'four', 5:'five',
          6:'six', 7:'seven',
          8:'eight', 9:'nine',}

#initializing module
pygame.init()

displaySurface = pygame.display.set_mode((x_size, y_size))

pygame.display.set_caption('handwriting board')

isWriting = False
x_move_value = []
y_move_value = []

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEMOTION and isWriting:
            x_move, y_move = event.pos
            pygame.draw.circle(displaySurface, black, (x_move, y_move), 4, 0)
            x_move_value.append(x_move)
            y_move_value.append(y_move)
        
        if event.type == MOUSEBUTTONDOWN:
            isWriting = True

        if event.type == MOUSEBUTTONUP:
            isWriting = False
            x_move_value = sorted(x_move_value)
            y_move_value = sorted(y_move_value)