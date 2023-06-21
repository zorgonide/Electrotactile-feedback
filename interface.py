import tkinter as tk
from serial import Serial
import sys
from stim8updated import *

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
        button_up = tk.Button(self, text='<= LeftUp',
                              width=8, height=4, command=self.goLeftUp)
        button_up.grid(row=1, column=2, pady=10)
        button_up = tk.Button(self, text='=> RightUp',
                              width=8, height=4, command=self.goRightUp)
        button_up.grid(row=1, column=4, pady=10)

        button_left = tk.Button(self, text='← Left',
                                width=8, height=4, command=self.goLeft)
        button_left.grid(row=2, column=2)

        button_right = tk.Button(self,  text='X STOP',
                                 width=8, height=4, command=self.Stop)
        button_right.grid(row=2, column=3)
        button_down = tk.Button(self, text='→ Right',
                                width=8, height=4, command=self.goRight)
        button_down.grid(row=2, column=4)

    def goUp(self):
        for c in range(4):
            self.fes.stimulate(self.tactons[LF])
            self.fes.stimulate(self.tactons[RF])

    def Stop(self):
        for c in range(4):
            self.fes.stimulate(self.tactons[L])
            self.fes.stimulate(self.tactons[R])

    def goLeft(self):
        self.fes.stimulate(self.tactons[L])

    def goLeftUp(self):
        self.tactons[L].duration = 1
        self.tactons[LF].duration = 1
        for c in range(2):
            self.fes.stimulate(self.tactons[L])
            self.fes.stimulate(self.tactons[LF])
        self.tactons[L].duration = self.duration
        self.tactons[LF].duration = self.duration

    def goRightUp(self):
        self.tactons[R].duration = 1
        self.tactons[RF].duration = 1
        for c in range(2):
            self.fes.stimulate(self.tactons[R])
            self.fes.stimulate(self.tactons[RF])
        self.tactons[R].duration = self.duration
        self.tactons[RF].duration = self.duration

    def goRight(self):
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

    # root = tk.Tk()
    # for c in range(1, 9):
    #     tacton = Tacton(channel=c, frequency=1, amplitude=7,
    #                     duration=-1, pulse_width=310)
    #     UIChannelControl(root, fes, tacton)
    # root.mainloop()
    root = tk.Tk()
    keyboard = KeyboardInterface(root, fes)
    root.mainloop()
    fes.stop()
    fes.disconnect()
