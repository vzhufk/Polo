import webbrowser

import pygame

"""Main setup"""
FPS = 60
window_title = 'Polo'
screen_resolution = (800, 600)
screen_mode = pygame.FULLSCREEN
level_path = r"/Levels/"

"""Fonts and Language"""
language = "en"  # "en"
pygame.font.init()
size = 16
message_line_length = 70
font_location = "Source/Fonts/"
orson_location = font_location + "SFOrson/"
silver_location = font_location + "SilverAge/"
ghost_location = font_location + "Ghost/"
font_medium = pygame.font.Font(orson_location + "SFOrsonCasualMedium.ttf", size)
font_heavy = pygame.font.Font(orson_location + "SFOrsonCasualHeavy.ttf", int(1.5 * size))
font_shaded = pygame.font.Font(orson_location + "SFOrsonCasualShaded.ttf", 2 * size)
font_message_text = pygame.font.Font(ghost_location + "T-FLEXTypeB.ttf", int(1.6 * size))

"""User"""
user_config_file = "cfg"


def about():
    out_about = "Polo \n" \
                "Created by Zhufyak V.V. \n" \
                "Music by Baglay R. I." \
                "Special thanks: \n" \
                "Baglay Roman \n" \
                "Kappa"
    git_link = "https://github.com/zhufyakvv/Polo"
    print(out_about)
    webbrowser.open(url=git_link)
