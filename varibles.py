import webbrowser

import pygame

FPS = 60
window_title = 'Polo'
screen_resolution = (800, 600)
screen_mode = pygame.FULLSCREEN
level_path = r"/Levels/"

about = "Polo \n" \
        "Created by Zhufyak V.V. \n" \
        "Music by Baglay R. I." \
        "Special thanks: \n" \
        "Baglay Roman \n" \
        "Kappa"
git_link = "https://github.com/zhufyakvv/Polo"


def about():
    print(about)
    webbrowser.open(url=git_link)
