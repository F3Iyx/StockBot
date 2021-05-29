from pygame import mixer


def beepInit():
    mixer.init()
    mixer.music.load('beep-05.wav')


def beep(repetition):
    mixer.music.play(repetition, 0.0)
