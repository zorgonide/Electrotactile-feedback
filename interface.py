import tkinter as tk
from serial import Serial
import sys
from stim8updated import *
from tkinter import ttk
import logging
from datetime import datetime
L = 0
R = 1
LF = 2
RF = 3


class KeyboardInterface(tk.Frame):
    def __init__(self, master, fes):
        tk.Frame.__init__(self, master, padx=10, pady=10)
        self.pack()
        self.fes = fes
        self.amplitude = 10
        self.frequency = 1
        self.pulse_width = 500
        self.duration = 1
        self.tactons = list((
            Tacton(channel=L+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=self.duration, pulse_width=self.pulse_width),
            Tacton(channel=R+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=self.duration, pulse_width=self.pulse_width),
            Tacton(channel=LF+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=self.duration, pulse_width=self.pulse_width),
            Tacton(channel=RF+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=self.duration, pulse_width=self.pulse_width),
        ))
        self.create_widgets()

        # First row: Amplitude, Pulse Width, Frequency
        tk.Label(self, text='Amplitude').grid(row=0, column=0)
        self.sb_amplitude = tk.Spinbox(
            self, from_=1, to=20, width=5, command=self.update_amplitude)
        self.sb_set_default(self.sb_amplitude, self.tactons[0].amplitude)
        self.sb_amplitude.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(self, text='Pulse Width').grid(row=0, column=2)
        self.sb_pulse_width = tk.Spinbox(
            self, from_=1, to=1000, width=5, command=self.update_pulse_width)
        self.sb_set_default(self.sb_pulse_width, self.tactons[0].pulse_width)
        self.sb_pulse_width.grid(row=0, column=3, padx=5, pady=10)

        tk.Label(self, text='Frequency').grid(row=0, column=4)
        self.sb_frequency = tk.Spinbox(
            self, from_=1, to=20, width=5, command=self.update_frequency)
        self.sb_set_default(self.sb_frequency, self.tactons[0].frequency)
        self.sb_frequency.grid(row=0, column=5, padx=5, pady=10)

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

    def goUp(self):
        logger.info(
            f"Command: goUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.update_progress(0)
        for c in range(4):
            self.fes.stimulate(self.tactons[LF])
            self.fes.stimulate(self.tactons[RF])
            self.update_progress((c+1)*25)

    def Stop(self):
        logger.info(
            f"Command: Stop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.update_progress(0)
        for c in range(4):
            self.fes.stimulate(self.tactons[L])
            self.fes.stimulate(self.tactons[R])
            self.update_progress((c+1)*25)

    def goLeft(self):
        logger.info(
            f"Command: goLeft, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.fes.stimulate(self.tactons[L])

    def goLeftUp(self):
        logger.info(
            f"Command: goLeftUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.tactons[L].duration = 1
        self.tactons[LF].duration = 1
        for c in range(2):
            self.fes.stimulate(self.tactons[L])
            self.fes.stimulate(self.tactons[LF])
        self.tactons[L].duration = self.duration
        self.tactons[LF].duration = self.duration

    def goRightUp(self):
        logger.info(
            f"Command: goRightUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.tactons[R].duration = 1
        self.tactons[RF].duration = 1
        for c in range(2):
            self.fes.stimulate(self.tactons[R])
            self.fes.stimulate(self.tactons[RF])
        self.tactons[R].duration = self.duration
        self.tactons[RF].duration = self.duration

    def goRight(self):
        logger.info(
            f"Command: goRight, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.fes.stimulate(self.tactons[R])

    def update_amplitude(self):
        for c in range(1, 5):
            self.tactons[c - 1].amplitude = int(self.sb_amplitude.get())
        # self.tacton.amplitude = int(self.sb_amplitude.get())
        # self.update_fes()  # not necessary for now

    def update_pulse_width(self):
        for c in range(1, 5):
            self.tactons[c - 1].pulse_width = int(self.sb_pulse_width.get())
        # self.tacton.pulse_width = int(self.sb_pulse_width.get())
        # self.update_fes()  # not necessary for now

    def update_frequency(self):
        for c in range(1, 5):
            self.tactons[c - 1].frequency = int(self.sb_frequency.get())
        # self.tacton.frequency = int(self.sb_frequency.get())
        # self.update_fes()  # not necessary for now

    # def update_duration(self):
    #     for c in range(1, 5):
    #         self.tactons[c - 1].duration = int(self.sb_duration.get())
    #     # self.tacton.duration = int(self.sb_duration.get())
    #     # self.update_fes()  # not necessary for now

    def update_fes(self):
        for c in range(1, 5):
            self.fes.stimulate(self.tactons[c - 1])

    def sb_set_default(self, sb, value):
        sb.delete(0, 'end')
        sb.insert(0, value)


if __name__ == '__main__':
    participant_name = input('Please enter your name-age-gender(M/F/O): ')
    logger = logging.getLogger('UserStudyLogger')
    logger.setLevel(logging.INFO)
    log_file = "./logs/haptic/"+participant_name + '-HapticTest.txt'
    file_handler = logging.FileHandler(log_file)
    logger.addHandler(file_handler)
    # initialise FES Controller
    port = 'COM3'  # changed from 12
    # port = '/dev/tty.usbserial-FTWTCB3C'
    baudrate = 38400
    if len(sys.argv) > 1:
        port = sys.argv[1]
    fes = FESDriver(port, 38400)
    if not fes.connect():
        print("Error opening serial connection on port {}".format(port))
        exit(-1)
    fes.enable_refresh_lcd()
    root = tk.Tk()
    keyboard = KeyboardInterface(root, fes)
    root.mainloop()
    fes.stop()
    fes.disconnect()
