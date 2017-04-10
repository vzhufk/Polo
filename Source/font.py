import pygame

pygame.font.init()
size = 16
location = "Source/"
medium = pygame.font.Font(location+"SF Orson Casual Medium.ttf", size)
message_text = pygame.font.Font(location + "SF Orson Casual Heavy.ttf", int(1.3 * size))
heavy = pygame.font.Font(location+"SF Orson Casual Heavy.ttf", int(1.5*size))
shaded = pygame.font.Font(location + "SF Orson Casual Shaded.ttf", 32)
