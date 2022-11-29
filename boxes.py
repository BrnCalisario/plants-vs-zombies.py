import pygame
import plant


class PlantBox(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("Red")
        self.rect = self.image.get_rect(topleft=(pos))
        self.preview_plant = None
        self.price = 0


class PeashooterBox(PlantBox):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.transform.scale2x(pygame.image.load("graphics/peashooter/pea_0.png").convert_alpha())
        self.price = 100

    def getPlant(self, pos):
        return plant.Peashooter(pos)


class SunflowerBox(PlantBox):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.transform.scale2x(pygame.image.load("graphics/sunflower/sunflower_0.png").convert_alpha())
        self.price = 50

    def getPlant(self, pos):
        return plant.Sunflower(pos)


class WallnutBox(PlantBox):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.transform.smoothscale(pygame.image.load("graphics/wallnut/wallnut_0.png").convert_alpha(),(64, 64))
        self.price = 50

    def getPlant(self, pos):
        return plant.Wallnut(pos)
        