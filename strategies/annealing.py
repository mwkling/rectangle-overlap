import random
import math

class Annealing:
    def __init__(self, rectangles):
        self.rectangles = rectangles
        self.temperature = 1.0

        # TODO how to set/configure these parameters in a smarter way
        self.magnitude = 10
        self.rounds = 5000

    # Energy measure is the total area of overlap of this rectangle with others
    def energy(self, idx):
        rect = self.rectangles[idx]

        # TODO incorporate distance from original position?
        return sum([rect.overlapx(r) * rect.overlapy(r) for i, r in enumerate(self.rectangles)
                if i != idx and rect.overlap(r)])

    def step(self):
        if self.temperature <= 0:
            return

        tries = 0
        while tries < 10000:
            # TODO make smarter random choice here in some way?
            i = random.randint(0, len(self.rectangles) - 1)
            e = self.energy(i)

            if e > 0:
                # Now, randomly translate, but remember old position
                rect = self.rectangles[i]
                old_top = rect.top
                old_left = rect.left

                # TODO incorporate rotational moves as well?
                if random.random() > 0.5:
                    rect.top += (random.random() * 15) * (random.random() - 0.5)
                    rect.left += (random.random() * 15) * (random.random() - 0.5)
                else:
                    theta = random.random() * 2 * 3.1416
                    rect.rotate(theta)

                newe = self.energy(i)

                # Acceptance check compares new energy with previous w/temperature
                accept = False
                if newe < e and False:
                    accept = True
                else:
                    try:
                        accept = random.random() < math.exp((e - newe) / self.temperature)
                    except OverflowError:
                        # Not accepted
                        pass

                if accept:
                    break
                else:
                    rect.top = old_top
                    rect.left = old_left
            tries += 1

        self.temperature -= 1 / self.rounds
