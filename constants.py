#############################################
# TILES
#############################################
TILE_SIZE = 170    # hedgehog tile size in pixel
ROWS, COLS = 2, 4  # hedgehog grid size

TILE_POSITION_ADJUSTMENT = 65  # bring the tiles closer to the center by this amount in pixel

TRANSLATION_TOLERANCE = 3  # tolerance in pixel for snapping tiles to their target positions
ROTATION_TOLERANCE = 0.05  # tolerance in degrees for snapping tiles to their target angles

#############################################
# MAIN WINDOW
#############################################
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

FPS = 60  # animation FPS
BACKGROUND_COLOR = (68, 68, 68)
SHADOW_OFFSET = 3  # shadow offset in pixels for texts and slider

#############################################
# SLIDER
#############################################
SLIDER_X = 530
SLIDER_Y = WINDOW_HEIGHT - 85
SLIDER_WIDTH = 250
SLIDER_TEXT_POS = (SLIDER_X + 80, SLIDER_Y - 50)

#############################################
# COLORS
#############################################
# For buttons and slider
GRAY_COLOR = (100, 100, 100)
PURPLE_COLOR = (138, 43, 226)
BLUE_COLOR = (70, 130, 180)
PINK_COLOR = (255, 0, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)
DARK_GRAY_COLOR = (30, 30, 30)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# For stickers
U_SIDE_STICKER_COLOR = (255, 255, 255)  # white
F_SIDE_STICKER_COLOR = (0, 128, 0)      # green
R_SIDE_STICKER_COLOR = (255, 0, 0)      # red
L_SIDE_STICKER_COLOR = (255, 165, 0)    # orange
B_SIDE_STICKER_COLOR = (0, 0, 255)      # blue
D_SIDE_STICKER_COLOR = (255, 255, 0)    # yellow

#############################################
# TURNING CONFIGURATIONS
#############################################
ROTATION_ANIM_SPEED = 1.0    # base speed for rotation animations
SMOOTH_MOVEMENT_SPEED = 3.0  # base speed for smooth movement animations
SPEED_MIN_VALUE = 1.0/3.0    # minimum speed multiplier from the slider
SPEED_MAX_VALUE = 3.0        # maximum speed multiplier from the slider

# Pivot points are the centers of the 2x2 tile groups; one on the left, one on the right
PIVOT_Y = 200
PIVOT_L_X = WINDOW_WIDTH // 2 - 160
PIVOT_R_X = WINDOW_WIDTH // 2 + 160
# In case of an L turn, the tiles turn rotate this point
PIVOT_POINT_L = (PIVOT_L_X, PIVOT_Y)
# In case of an R turn, the tiles turn rotate this point
PIVOT_POINT_R = (PIVOT_R_X, PIVOT_Y)
# In case of an F or B turn, the tiles rotate around this point
PIVOT_POINT_FB = (WINDOW_WIDTH // 2, PIVOT_Y)

CW_R_TURN_CONFIG = {"from": [(0, 2), (0, 3), (1, 3), (1, 2)], "to": [(0, 3), (1, 3), (1, 2), (0, 2)],
                    "rotation_degree": 90, "target_angle_diff": 90, "pivot_point": PIVOT_POINT_R}
CCW_R_TURN_CONFIG = {"from": [(0, 2), (0, 3), (1, 3), (1, 2)], "to": [(1, 2), (0, 2), (0, 3), (1, 3)],
                     "rotation_degree": -90, "target_angle_diff": -90, "pivot_point": PIVOT_POINT_R}
CW_L_TURN_CONFIG = {"from": [(0, 0), (0, 1), (1, 1), (1, 0)], "to": [(0, 1), (1, 1), (1, 0), (0, 0)],
                    "rotation_degree": 90, "target_angle_diff": 90, "pivot_point": PIVOT_POINT_L}
CCW_L_TURN_CONFIG = {"from": [(0, 0), (0, 1), (1, 1), (1, 0)], "to": [(1, 0), (0, 0), (0, 1), (1, 1)],
                     "rotation_degree": -90, "target_angle_diff": -90, "pivot_point": PIVOT_POINT_L}
U2_TURN_CONFIG = {"from": [(0, 0), (0, 1), (0, 2), (0, 3)], "to": [(0, 2), (0, 3), (0, 0), (0, 1)]}
D2_TURN_CONFIG = {"from": [(1, 0), (1, 1), (1, 2), (1, 3)], "to": [(1, 2), (1, 3), (1, 0), (1, 1)]}
F2_TURN_CONFIG = {"from": [(0, 1), (0, 2), (1, 2), (1, 1)], "to": [(1, 2), (1, 1), (0, 1), (0, 2)],
                  "rotation_degree": 180, "target_angle_diff": 180, "pivot_point": PIVOT_POINT_FB}
B2_TURN_CONFIG = {"from": [(0, 0), (0, 3), (1, 3), (1, 0)], "to": [(1, 3), (1, 0), (0, 0), (0, 3)],
                  "rotation_degree": 180, "target_angle_diff": 180, "pivot_point": PIVOT_POINT_FB}
YA_TURN_CONFIG = {"from": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)],
                  "to": [(0, 3), (0, 0), (0, 1), (0, 2), (1, 3), (1, 0), (1, 1), (1, 2)]}

#############################################
# 3D MODEL CONSTANTS
#############################################
MODEL_STICKER_ORIGIN_SIZE = (855, 664)  # The sticker coordinates were measured on a 855x664 image by hand
MODEL_STICKER_TARGET_SIZE = (260, 200)  # This is the size we want to render the stickers at

MODEL_3D_TOP_MARGIN = 380  # the 3D model is rendered horizontally centered, and vertically starting from this y position

STICKER_POSITIONS = [[(20, 39),   (218, 17),  (306, 55),  (90, 81)],    # Ulb
                     [(567, 52),  (634, 14),  (839, 31),  (788, 73)],   # Ubr
                     [(558, 57),  (782, 78),  (719, 131), (471, 105)],  # Urf
                     [(100, 86),  (316, 59),  (425, 106), (190, 139)],  # Ufl
                     [(195, 153), (434, 119), (434, 359), (205, 405)],  # Flu
                     [(464, 118), (714, 145), (704, 397), (464, 360)],  # Fur
                     [(464, 376), (703, 412), (693, 642), (464, 597)],  # Frd
                     [(206, 421), (434, 375), (434, 595), (215, 651)],  # Fdl
                     [(729, 143), (790, 90),  (779, 314), (717, 392)],  # Rfu
                     [(799, 83),  (847, 41),  (834, 244), (786, 306)],  # Rub
                     [(784, 323), (833, 260), (821, 448), (774, 525)],  # Rbd
                     [(716, 410), (776, 334), (767, 536), (706, 635)],  # Rdf
                     [(10, 50),   (82, 92),   (95, 317),  (25, 256)],   # Lbu
                     [(90, 98),   (181, 152), (191, 402), (103, 325)],  # Luf
                     [(104, 341), (192, 419), (202, 646), (116, 549)],  # Lfd
                     [(26, 272),  (95, 334),  (108, 541), (40, 462)],   # Ldb
]

STICKER_COLORS = [U_SIDE_STICKER_COLOR,  # 0:  Ulb
                  U_SIDE_STICKER_COLOR,  # 1:  Ubr
                  U_SIDE_STICKER_COLOR,  # 2:  Urf
                  U_SIDE_STICKER_COLOR,  # 3:  Ufl

                  F_SIDE_STICKER_COLOR,  # 4:  Flu
                  F_SIDE_STICKER_COLOR,  # 5:  Fur
                  F_SIDE_STICKER_COLOR,  # 6:  Frd
                  F_SIDE_STICKER_COLOR,  # 7:  Fdl

                  R_SIDE_STICKER_COLOR,  # 8:  Rfu
                  R_SIDE_STICKER_COLOR,  # 9:  Rub
                  R_SIDE_STICKER_COLOR,  # 10: Rbd
                  R_SIDE_STICKER_COLOR,  # 11: Rdf

                  L_SIDE_STICKER_COLOR,  # 12: Lbu
                  L_SIDE_STICKER_COLOR,  # 13: Luf
                  L_SIDE_STICKER_COLOR,  # 14: Lfd
                  L_SIDE_STICKER_COLOR,  # 15: Ldb

                  B_SIDE_STICKER_COLOR,  # 16: Bru
                  B_SIDE_STICKER_COLOR,  # 17: Bul
                  B_SIDE_STICKER_COLOR,  # 18: Bld
                  B_SIDE_STICKER_COLOR,  # 19: Bdr

                  D_SIDE_STICKER_COLOR,  # 20: Dlf
                  D_SIDE_STICKER_COLOR,  # 21: Dfr
                  D_SIDE_STICKER_COLOR,  # 22: Drb
                  D_SIDE_STICKER_COLOR,  # 23: Dbl
]

# after certain moves, the stickers get permuted according to these lists
STICKER_PERMUTATION_R =  [ 0,  5,  6,  3,  4, 21, 22,  7, 11,  8,  9, 10, 12, 13, 14, 15,  2, 17, 18,  1, 20, 19, 16, 23]
STICKER_PERMUTATION_L =  [18,  1,  2, 17,  0,  5,  6,  3,  8,  9, 10, 11, 15, 12, 13, 14, 16, 23, 20, 19,  4, 21, 22,  7]
STICKER_PERMUTATION_U2 = [ 2,  3,  0,  1, 16, 17,  6,  7, 12, 13, 10, 11,  8,  9, 14, 15,  4,  5, 18, 19, 20, 21, 22, 23]
STICKER_PERMUTATION_D2 = [ 0,  1,  2,  3,  4,  5, 18, 19,  8,  9, 14, 15, 12, 13, 10, 11, 16, 17,  6,  7, 22, 23, 20, 21]
STICKER_PERMUTATION_F2 = [ 0,  1, 20, 21,  6,  7,  4,  5, 14,  9, 10, 13, 12, 11,  8, 15, 16, 17, 18, 19,  2,  3, 22, 23]
STICKER_PERMUTATION_B2 = [22, 23,  2,  3,  4,  5,  6,  7,  8, 15, 12, 11, 10, 13, 14,  9, 18, 19, 16, 17, 20, 21,  0,  1]
STICKER_PERMUTATION_Y =  [ 3,  0,  1,  2,  8,  9, 10, 11, 16, 17, 18, 19,  4,  5,  6,  7, 12, 13, 14, 15, 21, 22, 23, 20]

# sanity check
assert sorted(STICKER_PERMUTATION_R)  == list(range(24))
assert sorted(STICKER_PERMUTATION_L)  == list(range(24))
assert sorted(STICKER_PERMUTATION_U2) == list(range(24))
assert sorted(STICKER_PERMUTATION_D2) == list(range(24))
assert sorted(STICKER_PERMUTATION_F2) == list(range(24))
assert sorted(STICKER_PERMUTATION_B2) == list(range(24))
assert sorted(STICKER_PERMUTATION_Y)  == list(range(24))
