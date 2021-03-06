# Spritesheet Loader
# Loads images from a spritesheet for use with my games
# by Sarah Pierce

# Spritesheet(image,width,height,rows,cols,crop)  Spritesheet object with properties: spritesheet image,spritesheet width, spritesheet height, rows of images in spritesheet, cols of images in spritesheet, crop - yes/no?
# get_frame(row,col,scale,color)  Method to get an individual frame at row/col in spritesheet, with scaling factor 'scale' & transparancy 'color'
# get_frames(scale,color)  Method to get all frames from spritesheet and return them as a list, with scaling factor 'scale' & transparancy 'color'

import pygame

class Spritesheet():
    def __init__(self,image,width,height,rows,cols,crop):
        self.sheet = image  #spritesheet image
        self.width = width  #width of spritesheet
        self.height = height  #height of spritesheet
        self.rows = rows  #max rows of images in spritesheet
        self.cols = cols  #mas cols of images in spritesheet
        self.crop = crop  #whether to crop or not
        self.multiple = False  #used to flag multiple frame operation, to re-use same rect to keep image size consistant
        self.first = False  #used to mark first frame operation with multiple, in order to grab the rect to use for the rest

    #grab individual frame from the spritesheet (frame row/col, scaled, color is transparent)
    def get_frame(self,row,col,scale,color):
        image = pygame.Surface(((self.width//self.cols),(self.height//self.rows)), pygame.SRCALPHA)  #create surface the size of a frame (sheet size divided by rows/cols) (using int division)
        image.blit(self.sheet,(0,0),((col * (self.width//self.cols)),(row * (self.height//self.rows)),(self.width//self.cols), (self.height//self.rows)))  #display the area (starting 0,0 to w,h) at 0,0
        image = pygame.transform.scale(image,((self.width//self.cols) * scale,(self.height//self.rows) * scale))  #scale image
        image.set_colorkey(color)  #set transparency
        # crop if necessary
        if self.crop:
            if self.first and self.multiple:
                self.rect = image.get_bounding_rect()
                self.first = False
                image = image.subsurface(self.rect)
            elif self.multiple:
                image = image.subsurface(self.rect)
            else:
                rect = image.get_bounding_rect()  # find image size without extra padding
                image = image.subsurface(rect)  # crop image to remove extra padding
        return image

    #grab all the frames from the spreadsheet (scaled, color is transparent)
    def get_frames(self,scale,color):
        frames = []  #empty list for frame images
        self.multiple = True
        for row in range(self.rows):
            for col in range(self.cols):
                if row == 0 and col == 0:
                    self.first = True
                frames.append(self.get_frame(row,col,scale,color))  #grab the frame from spritesheet
        return frames





