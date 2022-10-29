import pygame
from cursor import Cursor
from plant import Peashooter, Plant
from enemy import Enemy
from terrain import Shovel, Grass

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_NAME = 'Plantas vs Zumbis'

size = [SCREEN_WIDTH, SCREEN_HEIGHT]


def dark_color(color_tuple):
    reduce = 40
    return color_tuple[0] - reduce, color_tuple[1] - reduce, color_tuple[2] - reduce


class PeashooterBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("Orange")
        self.rect = self.image.get_rect(topleft=(250, 50))
        self.preview_plant = None
        self.price = 50

    def getPlant(self, pos):
        return Peashooter(pos)



class Game:
    def add_plant(self, grass: Grass):
        grass.has_plant = True
        print("Adicionou")
        plant = Peashooter(grass.rect.center)
        self.plant_group.add(plant)
        self.sprite_group.add(plant)

    def display_money(self, screen):
        self.money_surf = self.game_font.render(f'{self.money}$', False, (255, 255, 255))
        self.money_rect = self.money_surf.get_rect(center=(125, 75))
        screen.blit(self.money_surf, self.money_rect)

    def __init__(self):
        self.game_over = False

        self.game_font = pygame.font.Font('font/font.ttf', 75)


        self.sprite_group = pygame.sprite.Group()
        self.plant_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.grass_group = pygame.sprite.Group()
        self.bullets_groups = pygame.sprite.Group()
        self.draggable_group = pygame.sprite.Group()


        self.plant_box = PeashooterBox()
        self.sprite_group.add(self.plant_box)
        self.draggable_group.add(self.plant_box)


        self.money = 250

        self.dragging_plant = None
        self.dragging_plant_group = pygame.sprite.GroupSingle()

        self.grass_x = 100
        self.grass_y = 200
        self.grass_gap = 120

        for i in range(5):
            for j in range(8):
                grass = Grass((self.grass_x + (j * self.grass_gap), self.grass_y + (i * self.grass_gap)))
                self.grass_group.add(grass)
                self.sprite_group.add(grass)

        for i in range(5):
            enemy = Enemy((1000, self.grass_y + (i * self.grass_gap) - 25))
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    for i in range(5):
                        enemy = Enemy((1000, self.grass_y + (i * self.grass_gap) - 25))
                        self.enemy_group.add(enemy)
                        self.sprite_group.add(enemy)


            if event.type == pygame.MOUSEBUTTONDOWN:
                # Shovel Click Logic
                if self.shovel.rect.colliderect(self.cursor.rect):
                    self.shovel.isDragging = True

                if self.plant_box.rect.colliderect(self.cursor.rect) and self.money >= self.plant_box.price:
                    # self.dragging_plant = Plant(pygame.mouse.get_pos())
                    self.dragging_plant = self.plant_box.getPlant(pygame.mouse.get_pos()) 
                    
                    self.dragging_plant_group.add(self.dragging_plant)
                    self.draggable_group.add(self.dragging_plant)
                else:
                    if self.dragging_plant:
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
                    grass = pygame.sprite.spritecollide(self.dragging_plant, self.grass_group, False)
                    if grass:
                        if not grass[0].has_plant:
                            self.money -= self.plant_box.price
                            self.add_plant(grass[0])
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

            self.display_money(screen)

            if self.dragging_plant is not None:
                grass = pygame.sprite.spritecollide(self.dragging_plant, self.grass_group, False)
                if grass:
                    if not grass[0].has_plant:
                        temp_image = Peashooter().image
                        temp_image.fill(dark_color(Peashooter().color))
                        temp_rect = temp_image.get_rect(center=(grass[0].rect.center))
                        screen.blit(temp_image, temp_rect)


            if self.dragging_plant is not None:
                self.dragging_plant_group.draw(screen)
                self.dragging_plant.rect.center = pygame.mouse.get_pos()

            
            self.cursor_sprite.update()
            self.cursor_sprite.draw(screen)



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
