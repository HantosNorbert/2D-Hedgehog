from constants import *

import pygame

class Model3D:
    """A simple class to represent the 3D model of the cube. We render only the visible stickers, but it acts as a fully functional 3D puzzle."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.sticker_colors = STICKER_COLORS.copy()

    def permute_stickers(self, permutation: list[int], repetition=1):
        for _ in range(repetition):
            self.sticker_colors = [self.sticker_colors[i] for i in permutation]

    def render(self, screen: pygame.surface.Surface):
        for sticker_color, sticker_pos in zip(self.sticker_colors, STICKER_POSITIONS):
            sticker = [(x / MODEL_STICKER_ORIGIN_SIZE[0] * MODEL_STICKER_TARGET_SIZE[0] + WINDOW_WIDTH // 2 - MODEL_STICKER_TARGET_SIZE[0] // 2,
                        y / MODEL_STICKER_ORIGIN_SIZE[1] * MODEL_STICKER_TARGET_SIZE[1] + MODEL_3D_TOP_MARGIN)
                    for (x, y) in sticker_pos]
            pygame.draw.polygon(screen, sticker_color, sticker, 0)
