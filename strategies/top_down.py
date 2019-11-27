# This strategy starts at the top, works it's way down, shifting rectangles downward as needed
# so they don't overlap previous rectangles above
class TopDown:
    def __init__(self, rectangles):
        self.rectangles = sorted(rectangles, key=lambda r: r.top)
        self.index = 1

    def overlaps_previous(self, i):
        r = self.rectangles[i]
        for rect in self.rectangles[:i]:
            if r.overlap(rect):
                return True
        return False

    def step(self):
        while self.index < len(self.rectangles) and not self.overlaps_previous(self.index):
            self.index += 1

        if self.index >= len(self.rectangles):
            # No more overlaps, so exit without doing anything
            return

        current = self.rectangles[self.index]
        translation = 0
        # Find the maximum vertical overlap of this rectangle with all previous rectangles
        for r in self.rectangles[:self.index]:
            if current.overlap(r):
                translation = max(translation, abs(r.bottom - current.top))

        current.top += translation
        # When sorting again, everything prior to self.index should stay in same order
        # Others may jump ahead of current now that it has been translated down
        self.rectangles = sorted(self.rectangles, key=lambda r: r.top)
