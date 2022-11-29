from pygame import Surface, sprite, mouse, image, transform


class Shovel(sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.initial_pos = (1075, 30)
        self.image = transform.smoothscale(image.load("graphics\pa\pa.png").convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=self.initial_pos)
        self.isDragging = False

        self.selected_plant = None

    def update(self):
        if self.isDragging:
            self.rect.center = mouse.get_pos()
        else:
            self.rect.topleft = self.initial_pos

    def collide_logic(self, plant):
        self.selected_plant = plant

    def collide_detach(self):
        self.selected_plant = None


class Grass(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = Surface((25, 25))
        self.image.fill('green')
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.is_dragging = False
        self.has_plant = False

        