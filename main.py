import pyautogui
from pynput.keyboard import Key, KeyCode, Listener, Controller, GlobalHotKeys

signals = {
    "run": True,
    "pause": False,
    "fun1": False,
    "fun2": False
}


def log(msg):
    print(msg)


def _exit():
    log("[EXIT]")
    signals["run"] = False


def pause():
    signals["pause"] = not signals["pause"]
    log(f'[PAUSE] Pause is {signals["pause"]}')


def function_1():
    signals["fun1"] = not signals["fun1"]
    log(f"[FUN 1] Set to {signals['fun1']}")


def function_2():
    signals["fun2"] = not signals["fun2"]
    log(f"[FUN 2] Set to {signals['fun2']}")


combination_to_function = {
    frozenset([Key.shift, Key.ctrl_l, KeyCode(vk=81)]): _exit,  # shift + ctrl + q
    frozenset([Key.shift, KeyCode(vk=27)]): pause,  # shift + esc
    frozenset([Key.shift, KeyCode(vk=116)]): function_1,  # shift + f5
    frozenset([Key.shift, KeyCode(vk=117)]): function_2,  # shift + f6
}


def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk


def get_char(key):
    return key.char if hasattr(key, 'char') else key.value.char


def is_combination_pressed(combination):
    return all([get_vk(key) in pressed_vks for key in combination])


pressed_vks = set()


def clear_key(key):
    if not isinstance(key, int):
        key = get_vk(key)
    if key in pressed_vks:
        pressed_vks.remove(key)


def on_press(key):
    vk = get_vk(key)
    log(f"Pressed {key}, vk: {vk}")
    pressed_vks.add(vk)

    for combination in combination_to_function:
        # log(f"[DEBUG] combination: {combination}")
        if is_combination_pressed(combination):
            log(f"[DEBUG] matched to: {pressed_vks}")
            for key in combination:
                clear_key(key)
            combination_to_function[combination]()


def on_release(key):
    clear_key(key)


listener = Listener(on_release=on_press, on_releas=on_release)
listener.start()
log(f"[DEBUG] Initial signals: {signals}")
while signals["run"]:
    if not signals["pause"] and signals["fun1"]:
        # Function 1
        pyautogui.rightClick(pyautogui.position())
        pyautogui.PAUSE = 0.1
    if not signals["pause"] and signals["fun2"]:
        # Function 2
        pyautogui.hotkey('ctrl', 'shift', 'f12')
        pyautogui.PAUSE = 0.1
listener.stop()
