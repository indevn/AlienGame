from pygame import mixer
import time
class GameSound():
    """游戏过程中播放BGM"""

    def __init__(self, index):
        """初始化BGM内容"""

        mixer.init()
        if index == 1:
            self.__mus_bgm()

    def __mus_bgm(self):

        # Starting the mixer
        mixer.init()

        # Loading the song
        mixer.music.load("bgm.mp3")

        # Setting the volume
        mixer.music.set_volume(0.7)

        # Start playing the song
        mixer.music.play()

        # # infinite loop
        # while True:
        #
        #     print("Press 'p' to pause, 'r' to resume")
        #     print("Press 'e' to exit the program")
        #     query = input("  ")
        #
        #     if query == 'p':
        #         # Pausing the music
        #         mixer.music.pause()
        #     elif query == 'r':
        #         # Resuming the music
        #         mixer.music.unpause()
        #     elif query == 'e':
        time.sleep(10)
                # Stop the mixer
        # mixer.music.stop()
                # break
        # mixer.music.load("bgm.mp3")
        # mixer.music.set_volume(0.7)
        #
        # mixer.music.play()
        #
        # #
        # while True:
        #     if not pygame.mixer.music.get_busy():
        #         pygame.mixer.music.play()


if __name__ == "__main__":
    bgm = GameSound(1)