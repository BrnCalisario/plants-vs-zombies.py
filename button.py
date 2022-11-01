import pygame


def change_size(image, size, angle=0):
    return pygame.transform.rotozoom(image, angle, size)


def image_load(path):
    return pygame.image.load(path).convert_alpha()


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        self.initial_pos = (400, pos)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.initial_pos)
        self.isHovering = False

    def check_click(self, mouse):
        self.change_image()

        if self.rect.collidepoint(mouse):
            self.isHovering = True
            return True
        else:
            self.isHovering = False

    def change_image(self):
        pass

    def do_action(self):
        pass


class ButtonStart(Button):
    def __init__(self, pos):
        super().__init__(pos, 'graphics/buttons/play1.png')

    def change_image(self):
        if self.isHovering:
            self.image = pygame.image.load('graphics/buttons/play2.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/buttons/play1.png').convert_alpha()

    def do_action(self):
        return "start"


class ButtonConfig(Button):
    def __init__(self, pos):
        super().__init__(pos, 'graphics/buttons/options1.png')

    def change_image(self):
        if self.isHovering:
            self.image = pygame.image.load('graphics/buttons/options2.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/buttons/options1.png').convert_alpha()

    def do_action(self):
        return None


class ButtonExit(Button):
    def __init__(self, pos):
        super().__init__(pos, 'graphics/buttons/exit1.png')

    def change_image(self):
        if self.isHovering:
            self.image = pygame.image.load('graphics/buttons/exit2.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/buttons/exit1.png').convert_alpha()

    def do_action(self):
        return "exit"
