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

WIDTH = 400
HEIGHT = 400
BUFFER = 50

def random_rect(uniform=False):
    left = random.randint(BUFFER, WIDTH)
    top = random.randint(BUFFER, HEIGHT)

    width = height = ratio = None

    def gen_dims():
        nonlocal width, height, ratio
        width = random.randint(10, max(min(WIDTH - left, 75), 10))
        max_height = 75 if uniform else width
        height = random.randint(10, max(min(HEIGHT - top, max_height), 10))
        ratio = width / height

    gen_dims()
    while ratio < 0.1 or ratio > 10:
        gen_dims()

    return Rectangle(left, top, width, height)

class Renderer:
    def __init__(self, rectangles, framerate, strategy, input_rectangles, output_rectangles,
                 output_gif, uniform, graphics=True):
        self.framerate = framerate
        self.input_rectangles = input_rectangles
        self.output_rectangles = output_rectangles
        self.output_gif = output_gif

        C = getattr(sys.modules[__name__], strategy)

        if input_rectangles:
            start_rectangles = Rectangle.from_csv(input_rectangles)
        else:
            start_rectangles = [random_rect(uniform) for i in range(rectangles)]

        if output_rectangles: Rectangle.to_csv(start_rectangles, output_rectangles)

        self.stepper = C(start_rectangles)

        if output_gif:
            shutil.rmtree("frames", ignore_errors=True)
            os.mkdir("frames")

        if graphics:
            pygame.init()
            size = width, height = WIDTH + 2 * BUFFER, HEIGHT + 2 * BUFFER
            self.screen = pygame.display.set_mode(size)

    def draw_rectangle(self, rect, fill=BLUE):
        pygame.draw.rect(self.screen, fill, rect.as_tuple())
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.top), (rect.right, rect.top))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.top), (rect.right, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.right, rect.bottom), (rect.left, rect.bottom))
        pygame.draw.line(self.screen, BLACK, (rect.left, rect.bottom), (rect.left, rect.top))

        # More could be drawn here - for example, a line connecting the original rectangle
        # position with the current rectangle position

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

        # Overall length should be 5 seconds
        per_frame = 4.0 / frames
        frame_array = [per_frame] * frames + [1.0]

        with imageio.get_writer(self.output_gif, mode="I", duration=frame_array) as writer:
            for i in range(frames):
                writer.append_data(imageio.imread(FRAME_PATH.format(i)))
            # Add final frame at the end
            writer.append_data(imageio.imread(FRAME_PATH.format(frames)))
        pygifsicle.optimize(self.output_gif)

    def run_no_graphics(self):
        while Rectangle.has_overlaps(self.stepper.rectangles):
            self.stepper.step()
        print(Rectangle.total_movement(self.stepper.rectangles))

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
    parser.add_argument("-s", "--strategy", default="Separation", help="Separation|TopDown|Annealing|WorstFirst")
    parser.add_argument("-i", "--input_rectangles", help="CSV with saved rectangle configuration")
    parser.add_argument("-o", "--output_rectangles", help="CSV to write generated rectangles to")
    parser.add_argument("-g", "--output_gif", help="GIF file to render output to")
    parser.add_argument("-u", "--uniform", help="generate random rectangles uniformly",
                        action="store_true")
    parser.add_argument("-l", "--loop", type=int, default=0, help="Run without graphics loop number of times.")
    parser.add_argument("-d", "--screen_size", type=int, default=500)

    args = parser.parse_args()


    if args.loop > 0:
        for _ in range(args.loop):
            renderer = Renderer(args.rectangles, args.framerate, args.strategy,
                                args.input_rectangles, args.output_rectangles, args.output_gif,
                                args.uniform, graphics=False)
            renderer.run_no_graphics()
    else:
        renderer = Renderer(args.rectangles, args.framerate, args.strategy,
                            args.input_rectangles, args.output_rectangles, args.output_gif, args.uniform)
        renderer.run()
