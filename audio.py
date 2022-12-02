import pygame

pygame.mixer.init()
my_sound = pygame.mixer.Sound('audio/smw_coin.wav')
my_sound.play()
pygame.time.wait(int(my_sound.get_length() * 1000))