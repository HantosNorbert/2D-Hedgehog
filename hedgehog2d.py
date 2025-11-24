from constants import *
from tile import Tile
from button import Button
from model3d import Model3D

import pygame

class Hedgehog2D:
    """Main class to run the Hedgehog 2D application. Handles initialization, main loop, event handling, and rendering."""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2D Hedgehog")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.model3d = Model3D()

        # load the tile images, rescale, and build the 2x4 grid
        tile_images = [pygame.image.load(f"tile_images/{i+1}.png").convert_alpha() for i in range(8)]
        tile_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in tile_images]
        self.tiles = [Tile(tile_images[i], (i // COLS, i % COLS)) for i in range(8)]

        self._init_buttons()

    def _init_buttons(self):
        """Prepare the buttons for user interaction. Position and size values are defined here instead of constants.py,
        as they are closely related to the main application layout."""
        self.buttons = {}
        # First row buttons
        self.buttons["x"]  = Button(20+0*50, WINDOW_HEIGHT - 100, 40, 40, "x",  (10, 8), PURPLE_COLOR)
        self.buttons["xp"] = Button(20+1*50, WINDOW_HEIGHT - 100, 40, 40, "x'", (10, 8), PURPLE_COLOR)
        self.buttons["L"]  = Button(20+2*50, WINDOW_HEIGHT - 100, 40, 40, "L",  (10, 8), BLUE_COLOR)
        self.buttons["Lp"] = Button(20+3*50, WINDOW_HEIGHT - 100, 40, 40, "L'", (10, 8), BLUE_COLOR)
        self.buttons["R"]  = Button(20+4*50, WINDOW_HEIGHT - 100, 40, 40, "R",  (10, 8), BLUE_COLOR)
        self.buttons["Rp"] = Button(20+5*50, WINDOW_HEIGHT - 100, 40, 40, "R'", (10, 8), BLUE_COLOR)
        self.buttons["U2"] = Button(20+6*50, WINDOW_HEIGHT - 100, 40, 40, "U2", (5, 8),  BLUE_COLOR)
        self.buttons["D2"] = Button(20+7*50, WINDOW_HEIGHT - 100, 40, 40, "D2", (5, 8),  BLUE_COLOR)
        self.buttons["F2"] = Button(20+8*50, WINDOW_HEIGHT - 100, 40, 40, "F2", (5, 8),  BLUE_COLOR)
        self.buttons["B2"] = Button(20+9*50, WINDOW_HEIGHT - 100, 40, 40, "B2", (5, 8),  BLUE_COLOR)
        # Second row buttons; yb is the only button that is inactive: it works only after ya
        self.buttons["ya"] =    Button(20+0*170, WINDOW_HEIGHT - 50, 150, 40, "y (gyro) 1/2",   (10, 8), PINK_COLOR)
        self.buttons["yb"] =    Button(20+1*170, WINDOW_HEIGHT - 50, 150, 40, "y (gyro) 2/2",   (10, 8), PINK_COLOR, is_active=False)
        self.buttons["y"]  =    Button(20+2*170, WINDOW_HEIGHT - 50, 150, 40, "y (gyro) full",  (10, 8), PURPLE_COLOR)
        self.buttons["yp"] =    Button(20+3*170, WINDOW_HEIGHT - 50, 150, 40, "y' (gyro) full", (5, 8),  PURPLE_COLOR)
        self.buttons["Reset"] = Button(20+4*170, WINDOW_HEIGHT - 50, 90,  40, "Reset",          (15, 8), DARK_GRAY_COLOR)

    def _which_button_is_clicked(self, mouse_pos) -> str | None:
        for button_id, button in self.buttons.items():
            if button.rect.collidepoint(mouse_pos) and button.is_active:
                return button_id
        return None

    def _do_turn(self, turn_config: dict):
        """Execute a turn based on the provided turn configuration dictionary. If pivot point is specified, it is a rotation."""
        selected_tiles = [next(tile for tile in self.tiles if tile.grid_pos == pos) for pos in turn_config["from"]]
        for tile, new_pos in zip(selected_tiles, turn_config["to"]):
            tile.set_grid_pos(new_pos)
            if "pivot_point" in turn_config:
                tile.pivot_point = turn_config["pivot_point"]
                tile.pivot_rotation_angle = turn_config["rotation_degree"]
                tile.target_angle = (tile.target_angle + turn_config["target_angle_diff"]) % 360

    def _do_yb_turn(self):
        """Execute the second part of the gyro turn, which contains only local rotations."""
        for tile in self.tiles:
            if sum(tile.grid_pos) % 2 == 0:
                tile.target_angle = (tile.target_angle + 30) % 360
            else:
                tile.target_angle = (tile.target_angle - 30) % 360

    def _reset_tiles(self):
        """Bring all tiles back to their original positions and orientations, with animation."""
        for i, tile in enumerate(self.tiles):
            pos = (i // COLS, i % COLS)
            tile.set_grid_pos(pos)
            tile.target_angle = 0
            tile.pivot_point = None

    def display(self) -> bool:
        """Main loop to run the Hedgehog application. Returns false if the application should quit."""
        dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

        self.screen.fill(BACKGROUND_COLOR)

        # write text with a shadow
        shadow_text = self.font.render("2D Hedgehog v1.0", True, BLACK_COLOR)
        self.screen.blit(shadow_text, (13, 13))
        info_text = self.font.render("2D Hedgehog v1.0", True, WHITE_COLOR)
        self.screen.blit(info_text, (10, 10))

        for tile in self.tiles:
            tile.update(dt)
            tile.draw(self.screen)

        for button in self.buttons.values():
            button.draw(self.screen, self.font)

        self.model3d.render(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

        pygame.display.update()
        return True

    def _handle_mouse_click(self, event):
        button_id = self._which_button_is_clicked(event.pos)
        match button_id:
            case "x":
                self._do_turn(CW_R_TURN_CONFIG)
                self._do_turn(CCW_L_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_R)
                self.model3d.permute_stickers(STICKER_PERMUTATION_L, repetition=3)
            case "xp":
                self._do_turn(CCW_R_TURN_CONFIG)
                self._do_turn(CW_L_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_R, repetition=3)
                self.model3d.permute_stickers(STICKER_PERMUTATION_L)
            case "R":
                self._do_turn(CW_R_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_R)
            case "Rp":
                self._do_turn(CCW_R_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_R, repetition=3)
            case "L":
                self._do_turn(CW_L_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_L)
            case "Lp":
                self._do_turn(CCW_L_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_L, repetition=3)
            case "U2":
                self._do_turn(U2_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_U2)
            case "D2":
                self._do_turn(D2_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_D2)
            case "F2":
                self._do_turn(F2_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_F2)
            case "B2":
                self._do_turn(B2_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_B2)
            case "ya":
                self._do_turn(YA_TURN_CONFIG)
                self.model3d.permute_stickers(STICKER_PERMUTATION_Y)
                # after a ya move, only yb and reset buttons are active
                for button in self.buttons.values():
                    if button.text != "Reset":
                        button.is_active = not button.is_active
            case "yb":
                self._do_yb_turn()
                # after a yb move, everything else is active again
                for button in self.buttons.values():
                    if button.text != "Reset":
                        button.is_active = not button.is_active
            case "y":
                self._do_turn(YA_TURN_CONFIG)
                self._do_yb_turn()
                self.model3d.permute_stickers(STICKER_PERMUTATION_Y)
            case "yp":
                for _ in range(3):
                    self._do_turn(YA_TURN_CONFIG)
                    self._do_yb_turn()
                self.model3d.permute_stickers(STICKER_PERMUTATION_Y, repetition=3)
            case "Reset":
                self._reset_tiles()
                self.model3d.reset()
                for button in self.buttons.values():
                    button.is_active = button.text != "y (gyro) 2/2"
