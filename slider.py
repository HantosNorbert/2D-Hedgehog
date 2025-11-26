from constants import SHADOW_OFFSET, BLACK_COLOR, LIGHT_GRAY_COLOR

import pygame

class Slider:
    """A simple horizontal slider UI component. (x,y) is the center position of the left end of the slider track."""
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.x = x
        self.y = y
        self.width = width
        height = 6
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        self.track_rect = pygame.Rect(x, y - height // 2, width, height)
        self.track_rect_shadow = pygame.Rect(x + SHADOW_OFFSET, y + SHADOW_OFFSET - height // 2, width, height)
        self.knob_radius = 10

        self.knob_x = self._value_to_pos(start_val)
        self.dragging = False

    def _value_to_pos(self, value):
        """Convert slider value to pixel position"""
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.x + ratio * self.width

    def _pos_to_value(self, px):
        """Convert pixel position to slider value"""
        ratio = (px - self.x) / self.width
        ratio = max(0, min(1, ratio))
        value = self.min_val + ratio * (self.max_val - self.min_val)
        return int(value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Check if clicking knob
            if (mx - self.knob_x)**2 + (my - self.y)**2 <= self.knob_radius**2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = event.pos
            # Clamp knob to slider range
            self.knob_x = max(self.x, min(self.x + self.width, mx))
            self.value = self._pos_to_value(self.knob_x)

    def draw(self, screen):
        # track
        pygame.draw.rect(screen, BLACK_COLOR, self.track_rect_shadow)
        pygame.draw.rect(screen, LIGHT_GRAY_COLOR, self.track_rect)
        # knob
        pygame.draw.circle(screen, BLACK_COLOR, (int(self.knob_x) + SHADOW_OFFSET, self.y + SHADOW_OFFSET), self.knob_radius)
        pygame.draw.circle(screen, LIGHT_GRAY_COLOR, (int(self.knob_x), self.y), self.knob_radius)
