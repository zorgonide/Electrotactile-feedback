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
        self.amplitude = 8
        self.frequency = 1
        self.pulse_width = 200
        self.duration = -1
        self.tactons = list((
            Tacton(channel=L+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=-1, pulse_width=self.pulse_width),
            Tacton(channel=R+1, frequency=self.frequency, amplitude=self.amplitude,
                   duration=-1, pulse_width=self.pulse_width),
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

        # define button as intvars
        self.button_up_active = tk.IntVar()
        self.button_left_up_active = tk.IntVar()
        self.button_right_up_active = tk.IntVar()
        self.button_left_active = tk.IntVar()
        self.button_right_active = tk.IntVar()
        self.button_down_active = tk.IntVar()

        # Second row: Keyboard buttons
        button_up = tk.Button(self, text='↑ Up', width=8,
                              height=4, command=self.goUp)
        button_up.grid(row=1, column=3, pady=10)
        self.button_up_active.set(0)

        self.button_left_up = tk.Button(self, text='<↑ LeftUp',
                                        width=8, height=4, command=self.goLeftUp)
        self.button_left_up.grid(row=1, column=2, pady=10)
        self.button_left_up_active.set(0)

        self.button_right_up = tk.Button(self, text='↑> RightUp',
                                         width=8, height=4, command=self.goRightUp)
        self.button_right_up.grid(row=1, column=4, pady=10)
        self.button_right_up_active.set(0)

        self.button_left = tk.Button(self, text='← Left',
                                     width=8, height=4, command=self.goLeft)
        self.button_left.grid(row=2, column=2)
        self.button_left_active.set(0)

        self.button_down = tk.Button(self,  text='STOP',
                                     width=8, height=4, command=self.Stop)
        self.button_down.grid(row=2, column=3)
        self.button_down_active.set(0)

        self.button_right = tk.Button(self, text='→ Right',
                                      width=8, height=4, command=self.goRight)
        self.button_right.grid(row=2, column=4)
        self.button_right_active.set(0)
        self.start_button = tk.Button(
            self, text='Start', width=11, height=5, command=self.start)
        self.start_button.grid(row=3, column=2, pady=10, padx=10)

        self.stop_button = tk.Button(
            self, text='Exit', width=11, height=5, command=self.stop)
        self.stop_button.grid(row=3, column=3, pady=10, padx=10)

    def start(self):
        logger.info(
            f"Start: Timestamp: {self.timestamp()}, Participant: {participant_name}, Amplitude: {self.amplitude}, Pulse width: {self.pulse_width}")

    def stop(self):
        logger.info(
            f"Stop: Timestamp: {self.timestamp()}, Participant: {participant_name}, Amplitude: {self.amplitude}, Pulse width: {self.pulse_width}")

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
            f"Command: goForward, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.fes.stimulate(self.tactons[LF])
        self.fes.stimulate(self.tactons[RF])
        time.sleep(3)
        self.fes.stop(self.tactons[LF])
        self.fes.stop(self.tactons[RF])

    def Stop(self):
        logger.info(
            f"Command: Stop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
        self.fes.stimulate(self.tactons[L])
        self.fes.stimulate(self.tactons[R])
        time.sleep(3)
        self.fes.stop(self.tactons[L])
        self.fes.stop(self.tactons[R])

    def goLeft(self):
        if self.button_left_active.get() == 0:
            logger.info(
                f"Command: goLeft, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(self.button_left_active, self.button_left)
            self.fes.stimulate(self.tactons[L])
        else:
            logger.info(
                f"Command: goLeftStop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(self.button_left_active, self.button_left)
            self.fes.stop(self.tactons[L])

    def goLeftUp(self):
        if self.button_left_up_active.get() == 0:
            logger.info(
                f"Command: goLeftUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_left_up_active, self.button_left_up)
            self.fes.stimulate(self.tactons[LF])
        else:
            logger.info(
                f"Command: goLeftUpStop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_left_up_active, self.button_left_up)
            self.fes.stop(self.tactons[LF])

    def goRightUp(self):
        if self.button_right_up_active.get() == 0:
            logger.info(
                f"Command: goRightUp, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_right_up_active, self.button_right_up)
            self.fes.stimulate(self.tactons[RF])
        else:
            logger.info(
                f"Command: goRightUpStop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_right_up_active, self.button_right_up)
            self.fes.stop(self.tactons[RF])

    def goRight(self):
        if self.button_right_active.get() == 0:
            logger.info(
                f"Command: goRight, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_right_active, self.button_right)
            self.fes.stimulate(self.tactons[R])
        else:
            logger.info(
                f"Command: goRightStop, Timestamp: {self.timestamp()}, Participant: {participant_name}")
            self.toggle_button_color(
                self.button_right_active, self.button_right)
            self.fes.stop(self.tactons[R])

    def update_amplitude(self):
        logger.info(
            f"Command: updated Amplitude to {self.sb_amplitude.get()}, Timestamp: {self.timestamp()}, Participant: {participant_name}")
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

    def toggle_button_color(self, button_state, button):
        if button_state.get() == 0:
            button.config(bg="red")
            button_state.set(1)
        else:
            # Replace with the original color of your button
            button.config(bg="SystemButtonFace")
            button_state.set(0)


if __name__ == '__main__':
    participant_name = input('Please enter your name-age-gender(M/F/O): ')
    logger = logging.getLogger('UserStudyLogger')
    logger.setLevel(logging.INFO)
    log_file = "./logs/haptic/"+participant_name + '-HapticTestDiscontinuous.txt'
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
