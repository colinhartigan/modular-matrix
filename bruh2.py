from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()

pressed = []

def on_press(key):
    if key == Key.backspace and len(pressed) > 0:
        pressed.pop()
    else:
        pressed.append(key)
    print(pressed)
    check()

    if key == Key.esc:
        return False

def check():
    p = "".join(str(i).strip("'").lower() for i in pressed)
    if "eric" in p:
        print("eric detected")
        pressed.clear()
        write()

def write():
    for i in range(4):
        keyboard.press(Key.backspace)
    keyboard.type("dick")

def on_release(key):
    pass

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()