import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

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


font = pygame.font.SysFont('Arial', 30)
boundInc = 10
isWriting = False
x_move_value = []
y_move_value = []
img_count = 1
predict = True

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

        if event.type == MOUSEBUTTONDOWN:
            isWriting = True

        if event.type == MOUSEBUTTONUP:
            isWriting = False
            x_move_value = sorted(x_move_value)
            y_move_value = sorted(y_move_value)

            x_min, x_max = max(0, x_move_value[0]-boundInc), min(x_size, x_move_value[-1]+boundInc)
            y_min, y_max = max(0, y_move_value[0]-boundInc), min(y_size, y_move_value[-1]+boundInc)
            
            x_move_value = []
            y_move_value = []

            image_array = np.array(pygame.PixelArray(displaySurface))[x_min:x_max, y_min:y_max].T.astype(np.float32)

            if image_save:
                cv2.imwrite('image.png')
                img_count += 1
            
            if predict:
                image_array = cv2.resize(image_array, (28, 28))
                image_array = np.pad(image_array, (10, 10), 'constant', constant_values=0)
                # image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
                # ValueError, cannot reshape array of size 2304 into shape (1,28,28,1), what to do?
                image_array = cv2.resize(image_array, (28, 28))/255

                label = str(labels[np.argmax(model.predict(image_array.reshape(1, 28, 28, 1)))])

                textSurface = font.render(label, True, red)
                textRect = textSurface.get_rect()
                # note if error shows from using x_min, y_max, use x_min, y_min
                textRect.left, textRect.bottom = x_min, y_max

                displaySurface.blit(textSurface, textRect)

                # prediction = model.predict(image_array)
                # print(str(labels[np.argmax(prediction)]))
            
            if event.type == KEYDOWN:
                if event.unicode == 'n':
                    displaySurface.fill(white)

    
    pygame.display.update()