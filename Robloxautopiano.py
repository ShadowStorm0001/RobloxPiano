import tkinter as tk
import time
import threading
from pynput.keyboard import Controller, Key
import keyboard

is_replaying = False
play_thread = None
keyboard_controller = Controller()

shift_chars = {
    ')': '0', '!': '1', '@': '2', '#': '3', '$': '4',
    '%': '5', '^': '6', '&': '7', '*': '8', '(': '9',
    'O': 'o', 'Y': 'y', 'W': 'w', 'I': 'i', 'U': 'u',
    'T': 't', 'L': 'l', 'J': 'j', 'Z': 'z'
}

def press_char(c):
    if c in shift_chars:
        keyboard_controller.press(Key.shift)
        keyboard_controller.press(shift_chars[c])
        keyboard_controller.release(shift_chars[c])
        keyboard_controller.release(Key.shift)
    elif c.isupper():
        keyboard_controller.press(Key.shift)
        keyboard_controller.press(c.lower())
        keyboard_controller.release(c.lower())
        keyboard_controller.release(Key.shift)
    else:
        keyboard_controller.press(c)
        keyboard_controller.release(c)

def type_notes(notes):
    for note in notes.split():
        if not is_replaying:
            break
        if note.startswith('[') and note.endswith(']'):
            simultaneous_notes = note[1:-1]
            for n in simultaneous_notes:
                press_char(n)
        else:
            for char in note:
                press_char(char)
        time.sleep(delay / 1000)

def start_playing(continuous=False):
    global is_replaying, delay, play_thread
    if is_replaying and play_thread and play_thread.is_alive():
        return
    notes = input_box.get("1.0", "end-1c")
    try:
        delay_input = delay_box.get()
        delay = int(delay_input)
    except ValueError:
        delay = 0
    def replay():
        while is_replaying:
            type_notes(notes)
            if not continuous:
                break
    is_replaying = True
    play_thread = threading.Thread(target=replay)
    play_thread.start()

def toggle_replay():
    global is_replaying
    if is_replaying:
        is_replaying = False
    else:
        start_playing(continuous=True)

def listen_f6_key():
    keyboard.add_hotkey('F6', toggle_replay)

def listen_f5_key():
    keyboard.add_hotkey('F5', lambda: start_playing(continuous=True))

threading.Thread(target=listen_f6_key, daemon=True).start()
threading.Thread(target=listen_f5_key, daemon=True).start()

root = tk.Tk()
root.title("Sheet Music Player")

input_label = tk.Label(root, text="Enter sheet music:")
input_label.pack()

input_box = tk.Text(root, height=10, width=40)
input_box.pack()

delay_label = tk.Label(root, text="Enter delay (ms) between notes:")
delay_label.pack()

delay_box = tk.Entry(root)
delay_box.pack()

play_button = tk.Button(root, text="Play Once (F6)", command=lambda: start_playing(continuous=False))
play_button.pack()

continuous_button = tk.Button(root, text="Continuous Replay (F5)", command=lambda: start_playing(continuous=True))
continuous_button.pack()

def on_closing():
    global is_replaying
    is_replaying = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
