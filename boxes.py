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
        self.image.fill("Orange")
        self.price = 100

    def getPlant(self, pos):
        return plant.Peashooter(pos)


class SunflowerBox(PlantBox):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill("Gold")
        self.price = 50

    def getPlant(self, pos):
        return plant.Sunflower(pos)