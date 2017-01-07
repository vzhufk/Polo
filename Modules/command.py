from pygame.rect import Rect

from Libraries.load import *
import Source.font as font

height = 50
width = 50
size = (50, 50)
location = "Source/"
expansion = ".png"


class Command(pygame.sprite.Sprite):
    def __init__(self, name, image_name, placement=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image, self.rect = image(image_name, -1)
        self.original = self.image
        self.rect = Rect(placement[0], placement[1], self.rect[0] + self.rect[2],
                         self.rect[1] + self.rect[3])
        self.font = font.font
        self.fade = False
        self.countable = True
        self.amount = 10
        self.update()

    def update(self):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.fade:
            temp = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA).convert()
            temp.blit(self.original, (0, 0))
            temp.set_alpha(85)
            surf.blit(temp, (0, 0))
        else:
            surf.blit(self.original, (0, 0))
        if self.countable:
            text = self.font.render(str(self.amount), 2, (0, 0, 0))
            surf.blit(text, (self.rect.width - 1.5 * font.size, 0))
        self.image = surf.convert_alpha()

    def collision(self, position):
        # CORRECTION
        position = (position[0], position[1])
        return self.rect.collidepoint(position)

    def set_placement(self, placement):
        self.rect.x = placement[0]
        self.rect.y = placement[1]

    def set_amount(self, amount):
        self.amount = amount
        self.update()

    def change_amount(self, dif):
        self.amount += dif
        if self.amount == 0:
            self.fade = True
            self.update()
        elif self.amount < 0:
            self.amount = 0
        elif self.amount > 0:
            self.fade = False
            self.update()

    def fade_out(self):
        self.fade = True
        self.update()

    def fade_in(self):
        self.fade = False
        self.update()

    def get_amount(self):
        return self.amount

    def uncountable(self):
        self.countable = False

    def countable(self):
        self.countable = True

    def recountable(self):
        self.countable = not self.countable
        self.update()
