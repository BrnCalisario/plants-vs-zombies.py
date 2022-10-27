import pygame

def change_size(image, size, angle=0):
  return pygame.transform.rotozoom(image, angle, size)

def image_load(path):
    return pygame.image.load(path).convert_alpha()

class Cursor(pygame.sprite.Sprite):
    def __init__(self, size=0.25):
        super().__init__()

        self.size = size
        self.isHovering = False
        self.isClicking = False
        self.object_dragged = None
        self.isDragging = False

        # Sprites
        self.cursor_1 = change_size(image_load(
           'graphics/cursor/cursor_1.png'), self.size)
        self.cursor_2 = change_size(image_load(
           'graphics/cursor/cursor_2.png'), self.size)

        self.cursor_hold_1 = change_size(image_load(
           'graphics/cursor/cursor_hold_1.png'), self.size)
        self.cursor_hold_2 = change_size(image_load(
           'graphics/cursor/cursor_hold_2.png'), self.size)

        self.cursor = [self.cursor_1, self.cursor_2,
           self.cursor_hold_2, self.cursor_hold_1]
        self.index = 0

        self.image = self.cursor[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.cursor[self.index]
        self.rect.center = pygame.mouse.get_pos()

        if self.isHovering and not self.isClicking:
                self.index = 2
        elif not self.isHovering:
                self.index = 0

    def mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isClicking = True
            
            if self.isHovering:
                self.index = 3
            else:
                self.index = 1


        if event.type == pygame.MOUSEBUTTONUP:
            self.isClicking = False
            if self.object_dragged:
                self.object_dragged.isDragging = False
                self.object_dragged = None
            self.index = 0


    def mouse_interact(self, object):
        self.object_dragged = object
        self.isDragging = True
        self.object_dragged.isDragging = True

    
    def mouse_events(self, event, obj_list):
        flag = True
        flag2 = True

        if event.type == pygame.MOUSEMOTION:
            # for obj in obj_list:
            if flag2:
                if pygame.sprite.spritecollide(self, obj_list, False):
                    flag2 = False
                    self.isHovering = True
                else:
                    self.isHovering = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.sprite.spritecollide(self, obj_list, False) and flag:
                flag = False
                # self.cursor.mouse_interact(obj)

        self.mouse_click(event)