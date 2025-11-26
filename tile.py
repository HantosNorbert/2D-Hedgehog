from constants import PIVOT_Y, PIVOT_L_X, PIVOT_R_X, TILE_POSITION_ADJUSTMENT
from constants import ROTATION_ANIM_SPEED, SMOOTH_MOVEMENT_SPEED, SPEED_MIN_VALUE, SPEED_MAX_VALUE
from constants import TRANSLATION_TOLERANCE, ROTATION_TOLERANCE

import math
import pygame

class Tile:
    """A class to represent a Hedgehog tile on the 2x4 grid. A tile has an image and a grid position.

    A tile can smoothly move from one grid position to another, as well as rotate around its center and/or around a pivot point.
    For example, during an R turn, a tile can rotate around the R pivot point while moving to its new grid position;
    and also rotate around its own center to achieve the desired final orientation.
    """
    def __init__(self, image: pygame.surface.Surface, grid_pos: tuple[int, int], speed_adjustment: float):
        self.image = image
        self.grid_pos = grid_pos  # (row, col)
        self.current_pixel_pos = self._get_pixel_pos(grid_pos)
        self.target_pixel_pos = self.current_pixel_pos
        self.current_angle = 0  # the tile's rotation angle around its center point (current)
        self.target_angle = 0   # the tile's rotation angle around its center point (target, in case of animation)
        self.speed_adjustment = speed_adjustment  # a speed multiplier for the animation; coming from the slider

        # rotation control: if pivot point is set, a rotation is ongoing around the pivot point
        self.pivot_point = None
        self.pivot_rotation_angle = 0  # the tile's current rotation angle around the pivot point

    def _get_pixel_pos(self, pos) -> list[int, int]:
        """Calculate the actual pixel position of the tile based on its grid position."""
        row, col = pos
        # if the tile is on the top row, we pull the tile up relative to the pivot point, else we push it down
        y = PIVOT_Y - TILE_POSITION_ADJUSTMENT if row == 0 else PIVOT_Y + TILE_POSITION_ADJUSTMENT
        # we push the tile left or right relative to the left or right pivot points
        if col == 0:
            x = PIVOT_L_X - TILE_POSITION_ADJUSTMENT
        elif col == 1:
            x = PIVOT_L_X + TILE_POSITION_ADJUSTMENT
        elif col == 2:
            x = PIVOT_R_X - TILE_POSITION_ADJUSTMENT
        else:  # col == 3
            x = PIVOT_R_X + TILE_POSITION_ADJUSTMENT
        return [x, y]

    def set_grid_pos(self, new_pos: tuple[int, int]):
        self.grid_pos = new_pos
        self.target_pixel_pos = self._get_pixel_pos(new_pos)

    def update(self, dt: float):
        """Update the tile's position and rotation. If a pivot point is set, perform pivot rotation update;
        otherwise, perform smooth movement update."""
        if self.pivot_point is not None:
            self._pivot_update(dt)
        else:
            self._smooth_update(dt)

    def _distance_between_current_and_target_pixel_pos(self) -> float:
        return math.hypot(self.current_pixel_pos[0] - self.target_pixel_pos[0],
                          self.current_pixel_pos[1] - self.target_pixel_pos[1])

    def _pivot_update(self, dt):
        """Update the tile's position and rotation around the pivot point.
        The main idea here is to rotate the tile around the pivot point, but with each step we have to get closer to the target.
        If this does not happen, we stop the rotation animation and switch to smooth movement updates.
        """

        # before moving the tile, calculate distance between current_pixel_pos and target_pixel_pos
        distance_before = self._distance_between_current_and_target_pixel_pos()

        # calculate angle between target_pixel_pos, pivot_point, and current_pixel_pos
        # point P represents the center of the tile; point C represents the pivot point
        px, py = self.current_pixel_pos[0], self.current_pixel_pos[1]
        cx, cy = self.pivot_point[0], self.pivot_point[1]

        # how much to rotate in this update step
        rotation_amount = self.pivot_rotation_angle * ROTATION_ANIM_SPEED * self.speed_adjustment * dt

        # rotate the tile position around pivot
        p_vector = pygame.math.Vector2((px, py))
        c_vector = pygame.math.Vector2((cx, cy))
        p_relative_to_c = p_vector - c_vector
        rotated_p_relative_to_c = p_relative_to_c.rotate(rotation_amount)
        new_p_vector = rotated_p_relative_to_c + c_vector
        # the updated tile position is the top-left corner of the tile
        self.current_pixel_pos = [new_p_vector.x, new_p_vector.y]

        # we have to rotate the tile itself too around its center
        angle_diff = (self.target_angle - self.current_angle) % 360
        if angle_diff != 0:
            self.current_angle = (self.current_angle + rotation_amount) % 360

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
                # smooth movement, based on dt
                self.current_pixel_pos[i] += diff * SMOOTH_MOVEMENT_SPEED * self.speed_adjustment * dt
            else:
                # snap to position
                self.current_pixel_pos[i] = self.target_pixel_pos[i]

        # Smooth rotation
        angle_diff = (self.target_angle - self.current_angle) % 360
        if angle_diff != 0:
            if angle_diff > 180:
                angle_diff -= 360
            self.current_angle = (self.current_angle + angle_diff * SMOOTH_MOVEMENT_SPEED * self.speed_adjustment * dt) % 360
            # if we are close to the target angle, just snap to it; note that we have to consider the wrap-around at 360 degrees
            if abs(self.current_angle - self.target_angle) < ROTATION_TOLERANCE \
                    or abs((self.current_angle - 360) - self.target_angle) < ROTATION_TOLERANCE:
                self.current_angle = self.target_angle

    def draw(self, surface: pygame.surface.Surface):
        rotated_image = pygame.transform.rotate(self.image, -self.current_angle)
        rect = rotated_image.get_rect(center=(self.current_pixel_pos[0],
                                              self.current_pixel_pos[1]))
        surface.blit(rotated_image, rect)

    def update_speed(self, x):
        """Based on the slider position x (which can vary from 1 to 100), update the speed adjustment factor for this tile.
        We have to transform the linear slider to a logarithmic speed scale, so that x=1 maps to SPEED_MIN_VALUE,
        x=50 maps to 1.0, and x=100 maps to SPEED_MAX_VALUE."""
        L = math.log(SPEED_MIN_VALUE)
        H = math.log(SPEED_MAX_VALUE)
        if x <= 50:
            t = (x - 1.0) / 49.0
            speed = math.exp((1.0-t)*L)
        else:
            t = (x - 50.0) / 50.0
            speed = math.exp(t * H)

        self.speed_adjustment = speed
