import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime
import time
import threading
import pygame


class KeyboardInterface(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, padx=10, pady=10)
        self.pack()
        self.create_widgets()
        # Second row: Keyboard buttons
        self.button_up = tk.Button(self, text='↑ Up', width=8,
                                   height=4, command=self.goUp)
        self.button_up.grid(row=1, column=3, pady=10)
        self.button_left_up = tk.Button(self, text='<↑ LeftUp',
                                        width=8, height=4, command=self.goLeftUp)
        self.button_left_up.grid(row=1, column=2, pady=10)
        self.button_right_up = tk.Button(self, text='↑> RightUp',
                                         width=8, height=4, command=self.goRightUp)
        self.button_right_up.grid(row=1, column=4, pady=10)

        self.button_left = tk.Button(self, text='← Left',
                                     width=8, height=4, command=self.goLeft)
        self.button_left.grid(row=2, column=2)

        self.button_down = tk.Button(self,  text='STOP',
                                     width=8, height=4, command=self.Stop)
        self.button_down.grid(row=2, column=3)

        self.button_right = tk.Button(self, text='→ Right',
                                      width=8, height=4, command=self.goRight)
        self.button_right.grid(row=2, column=4)
        pygame.init()
        # button states
        self.button_up_active = {"state": 0, "button": self.button_up}
        self.button_left_up_active = {
            "state": 0, "button": self.button_left_up}
        self.button_right_up_active = {
            "state": 0, "button": self.button_right_up}
        self.button_left_active = {"state": 0, "button": self.button_left}
        self.button_right_active = {"state": 0, "button": self.button_right}
        self.button_down_active = {"state": 0, "button": self.button_down}
        # array of button states
        self.arrayOfButtonStates = [self.button_up_active, self.button_left_up_active, self.button_right_up_active,
                                    self.button_left_active, self.button_right_active, self.button_down_active]
        self.sound_thread = None
        self.is_sound_playing = False

    def create_widgets(self):
        # Create the progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Red.Horizontal.TProgressbar', background='red')
        style.configure('Green.Horizontal.TProgressbar', background='green')

        self.progress_bar = ttk.Progressbar(
            self.master, length=200, mode='determinate', style='Green.Horizontal.TProgressbar')
        self.progress_bar.pack(pady=10)

        # Create other widgets and layout

    def update_progress(self, value):
        self.progress_bar['value'] = value
        if value == 100:
            self.progress_bar['style'] = 'Green.Horizontal.TProgressbar'
        else:
            self.progress_bar['style'] = 'Red.Horizontal.TProgressbar'
        self.master.update()  # Update the Tkinter window

    def timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def check_button_active(self):
        for button in self.arrayOfButtonStates:
            if button["state"] == 1:
                self.toggle_button_color(button, button['button'])

    def toggle_button_color(self, button_state, button):
        if button_state["state"] == 0:
            button.config(bg="red")
            button_state["state"] = 1
        else:
            button.config(bg="SystemButtonFace")
            button_state["state"] = 0

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def goUp(self):
        self.check_button_active()
        self.toggle_button_color(self.button_up_active, self.button_up)
        if self.button_up_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('Forward.mp3', self.button_up_active, "Forward", 6))
            self.sound_thread.start()

    def play_sound_thread(self, sound, button_state, direction, timestamp=4):
        while button_state["state"] == 1:
            self.play_sound(sound)
            logger.info(
                f"Command: {direction}, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            time.sleep(timestamp)

    def Stop(self):
        self.check_button_active()
        self.play_sound('Stop.mp3')
        time.sleep(1)
        self.play_sound('Stop.mp3')
        logger.info(
            f"Command: Stop, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def goLeft(self):
        self.check_button_active()
        self.toggle_button_color(self.button_left_active, self.button_left)
        if self.button_left_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('Left.mp3', self.button_left_active, "Left"))
            self.sound_thread.start()

    def goLeftUp(self):
        self.check_button_active()
        self.toggle_button_color(
            self.button_left_up_active, self.button_left_up)
        if self.button_left_up_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('SLeft.mp3', self.button_left_up_active, "LeftUp"))
            self.sound_thread.start()

    def goRightUp(self):
        self.check_button_active()
        self.toggle_button_color(
            self.button_right_up_active, self.button_right_up)
        if self.button_right_up_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('SRight.mp3', self.button_right_up_active, "RightUp"))
            self.sound_thread.start()

    def goRight(self):
        self.check_button_active()
        self.toggle_button_color(self.button_right_active, self.button_right)
        if self.button_right_active["state"] == 1:
            self.sound_thread = threading.Thread(
                target=self.play_sound_thread, args=('Right.mp3', self.button_right_active, "Right"))
            self.sound_thread.start()

    def sb_set_default(self, sb, value):
        sb.delete(0, 'end')
        sb.insert(0, value)


if __name__ == '__main__':
    # participant_name = input('Please enter your name: ')
    participant_name = "test"
    logger = logging.getLogger('UserStudyLogger')
    logger.setLevel(logging.INFO)
    log_file = "./logs/sound/"+participant_name + '-SoundTest.txt'
    file_handler = logging.FileHandler(log_file)
    logger.addHandler(file_handler)
    root = tk.Tk()
    keyboard = KeyboardInterface(root)
    root.mainloop()
