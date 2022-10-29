from pygame import Surface, sprite, mouse


class Shovel(sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.initial_pos = (1000, 20)
        self.image = Surface((50, 50))
        self.image.fill("purple")
        self.rect = self.image.get_rect(topleft=self.initial_pos)
        self.isDragging = False

        self.selected_plant = None

    def update(self):
        if self.isDragging:
            self.rect.center = mouse.get_pos()
        else:
            self.rect.topleft = self.initial_pos

        if self.selected_plant is not None:
            self.selected_plant.image.fill("brown")

    def collide_logic(self, plant):
        self.selected_plant = plant

    def collide_detach(self):
        if self.selected_plant is not None:
            self.selected_plant.image.fill("white")
        self.selected_plant = None


class Grass(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = Surface((25, 25))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=pos)
        self.is_dragging = False
        self.has_plant = False

    def check_click(self, mouse):
        if self.rect.colliderect(mouse):
            return True
        