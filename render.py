import pygame
import sys
import argparse
import random

from strategies.separation import Separation
from strategies.top_down import TopDown
from strategies.annealing import Annealing
from rectangle import Rectangle

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

def random_rect():
    left = random.randint(250, 749)
    top = random.randint(250, 749)

    width = height = ratio = None
    def gen_dims():
        nonlocal width, height, ratio
        width = random.randint(1, min(750 - left, 100))
        height = random.randint(1, min(750 - top, 50))
        ratio = width / height

    gen_dims()
    while ratio < 0.1 or ratio > 10:
        gen_dims()

    return Rectangle(left, top, width, height)

class Renderer:
    def __init__(self, rectangles, framerate, strategy):
        C = getattr(sys.modules[__name__], strategy)
        self.stepper = C([random_rect() for i in range(rectangles)])
        self.framerate = framerate

        pygame.init()
        size = width, height = 1000, 1000
        self.screen = pygame.display.set_mode(size)

    def draw_rectangle(self, rect):
        pygame.draw.rect(self.screen, BLUE, rect.as_tuple())
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.top), (rect.right, rect.top))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.top), (rect.right, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.bottom), (rect.left, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.bottom), (rect.left, rect.top))

        pygame.draw.line(self.screen, RED, (rect.midx, rect.midy), (rect.original_midx, rect.original_midy))

    def run(self):
        clock = pygame.time.Clock()
        done = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WHITE)
            for r in self.stepper.rectangles:
                self.draw_rectangle(r)

            if not done:
                self.stepper.step()
                if not Rectangle.has_overlaps(self.stepper.rectangles):
                    print("No remaining overlaps!")
                    print("Total movement: ", Rectangle.total_movement(self.stepper.rectangles))
                    done = True

            pygame.display.update()
            clock.tick(self.framerate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rectangles", type=int, default=100)
    parser.add_argument("-f", "--framerate", type=int, default=30)
    parser.add_argument("-s", "--strategy", default="Separation")
    args = parser.parse_args()

    renderer = Renderer(args.rectangles, args.framerate, args.strategy)
    renderer.run()
