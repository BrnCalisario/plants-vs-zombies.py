import pygame
import random




class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        
        zombie_walk1 = pygame.image.load("graphics/zombie/zombie_walk1.png").convert_alpha()
        zombie_walk2 = pygame.image.load("graphics/zombie/zombie_walk2.png").convert_alpha()
        zombie_walk3 = pygame.image.load("graphics/zombie/zombie_walk3.png").convert_alpha()


        cabeludo_walk = []
        careca_walk = []
        carecalvo_walk = []
        flechado_walk = []
        picaretado_walk = []
        toca_walk = []

        for i in range(1, 4):
            cabeludo_walk.append(pygame.image.load(f"graphics/zombie/cabeludo_{i}.png").convert_alpha())
            careca_walk.append(pygame.image.load(f"graphics/zombie/careca_{i}.png").convert_alpha())
            carecalvo_walk.append(pygame.image.load(f"graphics/zombie/carecalvo_{i}.png").convert_alpha())
            flechado_walk.append(pygame.image.load(f"graphics/zombie/flechado_{i}.png").convert_alpha())
            picaretado_walk.append(pygame.image.load(f"graphics/zombie/picaretado_{i}.png").convert_alpha())
            toca_walk.append(pygame.image.load(f"graphics/zombie/toca_{i}.png").convert_alpha())


        cabeludo_walk.append(cabeludo_walk[1])
        careca_walk.append(careca_walk[1])
        carecalvo_walk.append(carecalvo_walk[1])
        flechado_walk.append(flechado_walk[1])
        picaretado_walk.append(picaretado_walk[1])
        toca_walk.append(toca_walk[1])
        self.zombie_walk = [zombie_walk1, zombie_walk2, zombie_walk3, zombie_walk2]


        self.zombie_index = 0

        self.zombie_type = random.choice([cabeludo_walk, careca_walk, carecalvo_walk, flechado_walk, picaretado_walk, toca_walk])
        self.image = self.zombie_type[self.zombie_index]

        # self.image = Surface((50, 50))
        # self.image.fill("green")
        self.rect = self.image.get_rect(topleft=pos)
        
        self.damage_delay = 0
        self.speed = 0

        self.health = 50
        self.damage = 5

    def update(self):
        self.rect.x -= self.speed
        self.animation_state()
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()

    def recive_damage(self, damage):
        self.health -= damage
        print(self.health)
        if (self.health <= 0):
            self.kill()

    def give_damage(self, plant):
        if self.damage_delay == 200:
            self.damage_delay = 0
            plant.recive_damage(self.damage)
        else: self.damage_delay += 5

    def animation_state(self):
        self.zombie_index += 0.05
        if self.zombie_index >= len(self.zombie_type) : self.zombie_index = 0
        self.image = self.zombie_type[int(self.zombie_index)]
