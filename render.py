import pygame
import sys
import argparse
import random
import shutil
import os
import imageio
import pygifsicle

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
FRAME_PATH = "frames/frame_{0}.png"


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
    def __init__(self, rectangles, framerate, strategy, input_rectangles, output_rectangles,
                 output_gif):
        self.framerate = framerate
        self.input_rectangles = input_rectangles
        self.output_rectangles = output_rectangles
        self.output_gif = output_gif

        C = getattr(sys.modules[__name__], strategy)

        if input_rectangles:
            start_rectangles = Rectangle.from_csv(input_rectangles)
        else:
            start_rectangles = [random_rect() for i in range(rectangles)]

        if output_rectangles: Rectangle.to_csv(start_rectangles, output_rectangles)

        self.stepper = C(start_rectangles)

        if output_gif:
            shutil.rmtree("frames", ignore_errors=True)
            os.mkdir("frames")

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

    def draw_rectangles(self):
        # Draw rectangles themselves
        for r in self.stepper.rectangles:
            self.draw_rectangle(r)

        # Draw overlaping sections of the rectangles in green
        for r in Rectangle.overlap_rectangles(self.stepper.rectangles):
            self.draw_rectangle(r, fill=GREEN)

    def save_frame(self, i):
        pygame.image.save(self.screen, FRAME_PATH.format(i))

    def save_gif(self, frames):
        # Last frame wasn't saved previously
        self.save_frame(frames)

        with imageio.get_writer(self.output_gif, mode="I") as writer:
            for i in range(frames):
                writer.append_data(imageio.imread(FRAME_PATH.format(i)))
            # Add 10 copies of final frame at the end
            for _ in range(10):
                writer.append_data(imageio.imread(FRAME_PATH.format(frames)))
        pygifsicle.optimize(self.output_gif)

    def run(self):
        clock = pygame.time.Clock()
        done = False
        frame = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.output_gif:
                        self.save_gif(frame)

                    pygame.quit()
                    sys.exit()

            self.screen.fill(WHITE)
            self.draw_rectangles()

            if not done:
                self.stepper.step()

                if self.output_gif:
                    self.save_frame(frame)
                    frame += 1

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
    parser.add_argument("-g", "--output_gif", help="GIF file to render output to")

    args = parser.parse_args()

    renderer = Renderer(args.rectangles, args.framerate, args.strategy,
                        args.input_rectangles, args.output_rectangles, args.output_gif)
    renderer.run()
