import pygame
import sys
import argparse
import random

from strategies.separation import Separation
from strategies.top_down import TopDown
from strategies.annealing import Annealing
from strategies.worst_first import WorstFirst
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
    def __init__(self, rectangles, framerate, strategy, input_rectangles, output_rectangles):
        self.framerate = framerate
        self.input_rectangles = input_rectangles
        self.output_rectangles = output_rectangles

        C = getattr(sys.modules[__name__], strategy)

        if input_rectangles:
            start_rectangles = Rectangle.from_csv(input_rectangles)
        else:
            start_rectangles = [random_rect() for i in range(rectangles)]

        if output_rectangles: Rectangle.to_csv(start_rectangles, output_rectangles)

        self.stepper = C(start_rectangles)

        pygame.init()
        size = width, height = 1000, 1000
        self.screen = pygame.display.set_mode(size)

    def draw_rectangle(self, rect, fill=BLUE):
        pygame.draw.rect(self.screen, fill, rect.as_tuple())
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.top), (rect.right, rect.top))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.top), (rect.right, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.bottom), (rect.left, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.bottom), (rect.left, rect.top))

        pygame.draw.line(self.screen, RED, (rect.midx, rect.midy),
                         (rect.original_midx, rect.original_midy))

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

            for r in Rectangle.overlap_rectangles(self.stepper.rectangles):
                self.draw_rectangle(r, fill=GREEN)

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
    parser.add_argument("-i", "--input_rectangles", help="CSV with saved rectangle configuration")
    parser.add_argument("-o", "--output_rectangles", help="CSV to write generated rectangles to")

    args = parser.parse_args()

    renderer = Renderer(args.rectangles, args.framerate, args.strategy,
                        args.input_rectangles, args.output_rectangles)
    renderer.run()
