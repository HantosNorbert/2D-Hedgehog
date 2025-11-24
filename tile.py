from constants import *

import math
import pygame

class Tile:
    """A class to represent a Hedgehog tile on the 2x4 grid. A tile has an image and a grid position.

    A tile can smoothly move from one grid position to another, as well as rotate around its center and/or around a pivot point.
    For example, during an R turn, a tile can rotate around the R pivot point while moving to its new grid position;
    and also rotate around its own center to achieve the desired final orientation.
    """
    def __init__(self, image: pygame.surface.Surface, grid_pos: tuple[int, int]):
        self.image = image
        self.original_grid_pos = grid_pos
        self.grid_pos = grid_pos  # (row, col)
        self.current_pixel_pos = self._get_pixel_pos(grid_pos)
        self.target_pixel_pos = self.current_pixel_pos
        self.current_angle = 0  # the tile's rotation angle around its center point (current)
        self.target_angle = 0   # the tile's rotation angle around its center point (target, in case of animation)

        # rotation control: if pivot point is set, a rotation is ongoing around the pivot point
        self.pivot_point = None
        self.pivot_rotation_angle = 0  # the tile's rotation angle around the pivot point (current)

    def _get_pixel_pos(self, pos) -> list[int, int]:
        """Calculate the actual pixel position of the tile based on its grid position."""
        row, col = pos
        # bring the tiles closer to the center by TILE_POSITION_ADJUSTMENT
        adjust_y = TILE_POSITION_ADJUSTMENT if self.grid_pos[0] == 0      else -TILE_POSITION_ADJUSTMENT
        adjust_x = TILE_POSITION_ADJUSTMENT if self.grid_pos[1] in [0, 2] else -TILE_POSITION_ADJUSTMENT
        x = TILE_MARGIN + col * (TILE_SIZE + TILE_MARGIN) + adjust_x
        y = TILE_MARGIN + row * (TILE_SIZE + TILE_MARGIN) + adjust_y
        return [x, y]

    def set_grid_pos(self, new_pos: tuple[int, int]):
        self.grid_pos = new_pos
        self.target_pixel_pos = self._get_pixel_pos(new_pos)

    def update(self, dt: float):
        """Update the tile's position and rotation. If a pivot point is set, perform pivot rotation update;
        otherwise, perform smooth movement update."""
        if self.pivot_point is not None:
            self._pivot_update()
        else:
            self._smooth_update(dt)

    def _distance_between_current_and_target_pixel_pos(self) -> float:
        return math.hypot(self.current_pixel_pos[0] - self.target_pixel_pos[0],
                          self.current_pixel_pos[1] - self.target_pixel_pos[1])

    def _pivot_update(self):
        """Update the tile's position and rotation around the pivot point.
        The main idea here is to rotate the tile around the pivot point, but with each step we have to get closer to the target.
        If this does not happen, we stop the rotation animation and switch to smooth movement updates.
        """

        # before moving the tile, calculate distance between current_pixel_pos and target_pixel_pos
        distance_before = self._distance_between_current_and_target_pixel_pos()

        # calculate angle between target_pixel_pos, pivot_point, and current_pixel_pos
        # point P represents the center of the tile; point C represents the pivot point
        px, py = self.current_pixel_pos[0] + TILE_SIZE // 2, self.current_pixel_pos[1] + TILE_SIZE // 2
        cx, cy = self.pivot_point[0], self.pivot_point[1]

        # Rotate the tile position around pivot
        p_vector = pygame.math.Vector2((px, py))
        c_vector = pygame.math.Vector2((cx, cy))
        p_relative_to_c = p_vector - c_vector
        rotated_p_relative_to_c = p_relative_to_c.rotate(self.pivot_rotation_angle)
        new_p_vector = rotated_p_relative_to_c + c_vector
        # the updated tile position is the top-left corner of the tile
        self.current_pixel_pos = [new_p_vector.x - TILE_SIZE // 2, new_p_vector.y - TILE_SIZE // 2]

        # we have to rotate the tile itself too around its center
        angle_diff = (self.target_angle - self.current_angle) % 360
        if angle_diff != 0:
            self.current_angle = (self.current_angle + self.pivot_rotation_angle) % 360

        # if we are close to the destination, just snap the tile to its place
        if abs(self.target_pixel_pos[0] - self.current_pixel_pos[0]) + abs(self.target_pixel_pos[1] - self.current_pixel_pos[1]) < TRANSLATION_TOLERANCE:
            self.current_pixel_pos = self.target_pixel_pos
            self.current_angle = self.target_angle
            self.pivot_point = None

        # if we start moving further from the target, we turn off the rotation animation
        distance_after = self._distance_between_current_and_target_pixel_pos()
        if distance_after > distance_before:
            self.pivot_point = None

    def _smooth_update(self, dt: float):
        """Update the tile's position and rotation smoothly towards the target position and angle."""
        for i in (0, 1):
            diff = self.target_pixel_pos[i] - self.current_pixel_pos[i]
            if abs(diff) > TRANSLATION_TOLERANCE:
                self.current_pixel_pos[i] += diff * min(dt * 3, 1)  # smooth movement, based on dt
            else:
                self.current_pixel_pos[i] = self.target_pixel_pos[i]  # snap to position

        # Smooth rotation
        angle_diff = (self.target_angle - self.current_angle) % 360
        if angle_diff != 0:
            if angle_diff > 180:
                angle_diff -= 360
            self.current_angle = (self.current_angle + angle_diff * min(dt * 3, 1)) % 360
            # if we are close to the target angle, just snap to it; note that we have to consider the wrap-around at 360 degrees
            if abs(self.current_angle - self.target_angle) < ROTATION_TOLERANCE \
                    or abs((self.current_angle - 360) - self.target_angle) < ROTATION_TOLERANCE:
                self.current_angle = self.target_angle

    def draw(self, surface: pygame.surface.Surface):
        rotated_image = pygame.transform.rotate(self.image, -self.current_angle)
        rect = rotated_image.get_rect(center=(self.current_pixel_pos[0] + TILE_SIZE // 2,
                                              self.current_pixel_pos[1] + TILE_SIZE // 2))
        surface.blit(rotated_image, rect)
