import tkinter as tk
from tkinter import ttk
from playsound import playsound
import logging
from datetime import datetime


class KeyboardInterface(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, padx=10, pady=10)
        self.pack()
        self.create_widgets()

        # Second row: Keyboard buttons
        button_up = tk.Button(self, text='↑ Up', width=8,
                              height=4, command=self.goUp)
        button_up.grid(row=1, column=3, pady=10)
        button_up = tk.Button(self, text='<↑ LeftUp',
                              width=8, height=4, command=self.goLeftUp)
        button_up.grid(row=1, column=2, pady=10)
        button_up = tk.Button(self, text='↑> RightUp',
                              width=8, height=4, command=self.goRightUp)
        button_up.grid(row=1, column=4, pady=10)

        button_left = tk.Button(self, text='← Left',
                                width=8, height=4, command=self.goLeft)
        button_left.grid(row=2, column=2)

        button_right = tk.Button(self,  text='STOP',
                                 width=8, height=4, command=self.Stop)
        button_right.grid(row=2, column=3)
        button_down = tk.Button(self, text='→ Right',
                                width=8, height=4, command=self.goRight)
        button_down.grid(row=2, column=4)

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

    def play_sound(self, sound_file):
        self.update_progress(0)
        playsound(sound_file)
        self.update_progress(100)

    def goUp(self):
        self.play_sound('Forward.mp3')
        logger.info(
            f"Command: goUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def Stop(self):
        self.play_sound('Stop.mp3')
        logger.info(
            f"Command: Stop, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def goLeft(self):
        self.play_sound('Left.mp3')
        logger.info(
            f"Command: goLeft, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def goLeftUp(self):
        self.play_sound('SLeft.mp3')
        logger.info(
            f"Command: goLeftUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def goRightUp(self):
        self.play_sound('SRight.mp3')
        logger.info(
            f"Command: goRightUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def goRight(self):
        self.play_sound('Right.mp3')
        logger.info(
            f"Command: goRight, Timestamp: {self.timestamp()}, Participant: {participant_name}")

    def sb_set_default(self, sb, value):
        sb.delete(0, 'end')
        sb.insert(0, value)


if __name__ == '__main__':
    participant_name = input('Please enter your name: ')
    logger = logging.getLogger('UserStudyLogger')
    logger.setLevel(logging.INFO)
    log_file = "./logs/sound/"+participant_name + '-SoundTest.txt'
    file_handler = logging.FileHandler(log_file)
    logger.addHandler(file_handler)
    root = tk.Tk()
    keyboard = KeyboardInterface(root)
    root.mainloop()
