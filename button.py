from constants import GRAY_COLOR, WHITE_COLOR

import pygame

class Button:
    """A simple button class to represent a button on the GUI. A button has a position (left, top), size (width, height),
    text to display, text position relative to the button, and color. An active button has its color displayed,
    while an inactive button is displayed in gray.
    """
    def __init__(self, left: int, top: int, width: int, height: int,
                 text: str, text_pos: tuple[int, int], color: tuple[int, int, int], is_active=True):
        self.rect = pygame.Rect(left, top, width, height)
        self.text = text
        self.text_pos = (self.rect.x + text_pos[0], self.rect.y + text_pos[1])
        self.color = color
        self.is_active = is_active

    def draw(self, screen: pygame.surface.Surface, font: pygame.font.Font):
        color = self.color if self.is_active else GRAY_COLOR
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(font.render(self.text, True, WHITE_COLOR), self.text_pos)
