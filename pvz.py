import pygame
from cursor import Cursor
from plant import Plant, Grass, Shovel
from enemy import Enemy

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_NAME = 'Plants vz Zombies'

size = [SCREEN_WIDTH, SCREEN_HEIGHT]


class PlantBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("Orange")
        self.rect = self.image.get_rect(topleft=(150, 50))
        self.preview_plant = None



class Game:
    def add_plant(self, grass: Grass):
        grass.has_plant = True
        print("Adicionou")
        plant = Plant(grass.rect.center)
        self.plant_group.add(plant)
        self.sprite_group.add(plant)

    def __init__(self):
        self.game_over = False

        self.sprite_group = pygame.sprite.Group()
        self.plant_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.grass_group = pygame.sprite.Group()
        self.bullets_groups = pygame.sprite.Group()
        self.draggable_group = pygame.sprite.Group()

        self.plant_box = PlantBox()
        self.sprite_group.add(self.plant_box)
        self.draggable_group.add(self.plant_box)


        self.dragging_plant = None
        self.dragging_plant_group = pygame.sprite.GroupSingle()


        grass_x = 100
        grass_y = 200
        grass_gap = 120

        for i in range(5):
            for j in range(8):
                grass = Grass((grass_x + (j * grass_gap), grass_y + (i * grass_gap)))
                self.grass_group.add(grass)
                self.sprite_group.add(grass)

        for i in range(5):
            enemy = Enemy((1000, grass_y + (i * grass_gap) - 25))
            self.enemy_group.add(enemy)
            self.sprite_group.add(enemy)

        self.shovel = Shovel()
        self.shovel_sprite = pygame.sprite.GroupSingle()
        self.shovel_sprite.add(self.shovel)
        self.draggable_group.add(self.shovel)

        self.cursor = Cursor()
        self.cursor_sprite = pygame.sprite.GroupSingle()
        self.cursor_sprite.add(self.cursor)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return True
            
            self.cursor.mouse_events(event, self.draggable_group)

            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Shovel Click Logic
                if self.shovel.rect.colliderect(self.cursor.rect):
                    self.shovel.isDragging = True

                # Grass click logic
                for grass in self.grass_group:
                    if grass.check_click(self.cursor.rect) and not grass.has_plant:
                        self.add_plant(grass)

                if self.plant_box.rect.colliderect(self.cursor.rect):
                    self.dragging_plant = Plant(pygame.mouse.get_pos())
                    self.dragging_plant_group.add(self.dragging_plant)
                else:
                    self.dragging_plant.kill()
                    self.dragging_plant = None
                    
            
            # Shovel Logic
            if event.type == pygame.MOUSEBUTTONUP:    
                if self.shovel.isDragging:
                    if self.shovel.selected_plant is not None:
                        grass = pygame.sprite.spritecollide(self.shovel.selected_plant, self.grass_group, False)
                        grass[0].has_plant = False

                        self.shovel.selected_plant.kill()
                    self.shovel.isDragging = False

                if self.dragging_plant is not None:
                    if not pygame.sprite.spritecollide(self.dragging_plant, self.grass_group, False):
                        self.dragging_plant.kill()
                        self.dragging_plant = None

    def run_logic(self):
        if not self.game_over:
            for enemy in self.enemy_group:
                collide_plant = pygame.sprite.spritecollide(enemy, self.plant_group, False)

                if collide_plant:
                    enemy.speed = 0
                    enemy.give_damage(collide_plant[0])
                else:
                    enemy.speed = 0.5

            for plant in self.plant_group:
                bullets = None
                if pygame.sprite.spritecollide(plant.plant_range, self.enemy_group, False):
                    bullets = plant.shoot()

                if bullets is not None:
                    self.bullets_groups.add(bullets)
                    self.sprite_group.add(bullets)

            for bullet in self.bullets_groups:
                collide_enemy = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
                if collide_enemy:
                    bullet.give_damage(collide_enemy[0])

            collide_shovel = pygame.sprite.spritecollide(self.shovel, self.plant_group, False)

            if collide_shovel:
                self.shovel.collide_logic(collide_shovel[0])
            else:
                self.shovel.collide_detach()


    def display_frame(self, screen):
        screen.fill('Black')
        if not self.game_over:
            self.sprite_group.draw(screen)
            self.sprite_group.update()

            self.shovel_sprite.update()
            self.shovel_sprite.draw(screen)

            
            if self.dragging_plant is not None:
                self.dragging_plant_group.draw(screen)
                self.dragging_plant.rect.center = pygame.mouse.get_pos()

            

            self.cursor_sprite.update()
            self.cursor_sprite.draw(screen)

            for plant in self.plant_group:
                plant.update_bullets(self.enemy_group)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)
    pygame.display.set_caption(GAME_NAME)

    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
