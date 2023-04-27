from pynput.keyboard import Key, Listener, Controller
from time import sleep

keyboard = Controller()

pressed = []
target = "didnt deserve it"
out = [
    [
        "is a rampant antisemite who uses his position of fame in order to further a position of hate and obvious racism in our country. ",
        "While his music stands up to scrutiny and forever will, this cannot make up for the huge, purposeful statements of hatred towards Jews in America he has made both on twitter which he was recently reinstated on and on a number of podcasts in which he has made appearances. ",

    ],
    [
        "I miss the old Kanye, straight from the 'Go Kanye",
        "Chop up the soul Kanye, set on his goals Kanye",
        "I hate the new Kanye, the bad mood Kanye",
        # "The always rude Kanye, spaz in the news Kanye",
        # "I miss the sweet Kanye, chop up the beats Kanye",
        # "I gotta to say at that time I'd like to meet Kanye",
        # "See I invented Kanye, it wasn't any Kanyes",
        # "And now I look and look around and there's so many Kanyes",
        # "I used to love Kanye, I used to love Kanye",
        # "I even had the pink polo, I thought I was Kanye",
        # "What if Kanye made a song about Kanye",
        # "Called 'I Miss The Old Kanye, ' man that would be so Kanye",
        # "That's all it was Kanye, we still love Kanye",
        # "And I love you like Kanye loves Kanye",
    ]
]


def on_press(key):
    if key == Key.backspace and len(pressed) > 0:
        pressed.pop()
    else:
        if key == Key.space:
            key = " "
        pressed.append(key)
    print(pressed)
    check()

    if key == Key.esc:
        return False


def check():
    p = "".join(str(i).strip("'").lower() for i in pressed)
    if target in p:
        print("")
        pressed.clear()
        write()


def write():
    sleep(0.25)
    with keyboard.pressed(Key.shift):
        for i in range(len(target)):
            keyboard.press(Key.left)
            sleep(0.1)
    sleep(0.5)
    keyboard.press(Key.delete)
    sleep(0.5)

    for j in out[0]:
        for k in j:
            keyboard.type(k)
            sleep(0.01)
        sleep(.25)

    keyboard.press(Key.enter)
    sleep(.5)

    for j in out[1]:
        for k in j:
            keyboard.type(k)
            sleep(0.01)
        keyboard.press(Key.enter)
        sleep(.25)

    pressed.clear()


def on_release(key):
    pass


# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
