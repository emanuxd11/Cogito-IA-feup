import pygame


class Sound:
    @staticmethod
    def playBackgroundTheme():
        pygame.mixer.music.load("../audio/cogito.mp3")                                 
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    @staticmethod
    def playMoveSound():
        sound_path = "../audio/arrow_click.mp3"
        arrow_sfx = pygame.mixer.Sound(sound_path)
        arrow_sfx.play()

    @staticmethod
    def playWinMusic():
        win_music_path = "../audio/win_music.mp3"
        pygame.mixer.music.load(win_music_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): # wait for music to stop playing
            pygame.time.Clock().tick(10)

