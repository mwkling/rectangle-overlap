class Rectangle:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        # So we can track how far the rectangle moved from original position
        self.original_left = left
        self.original_top = top

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def original_right(self):
        return self.original_left + self.width

    @property
    def original_bottom(self):
        return self.original_top + self.height

    @property
    def midx(self):
        return (self.left + self.right) / 2

    @property
    def midy(self):
        return (self.top + self.bottom) / 2

    @property
    def original_midx(self):
        return (self.original_left + self.original_right) / 2

    @property
    def original_midy(self):
        return (self.original_top + self.original_bottom) / 2

    def overlap(self, other):
        if(self.left >= other.right or other.left >= self.right): 
            return False
        if(self.top >= other.bottom or other.top >= self.bottom): 
            return False
        return True

    def center_vec(self, other):
        return (self.midx - other.midx, self.midy - other.midy)

    def as_tuple(self):
        return (self.left, self.top, self.width, self.height)

    def __str__(self):
        return "Rect" + str(self.as_tuple())
