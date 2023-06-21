from serial import Serial
import sys
import tkinter as tk
from stim8updated import *


class UIChannelControl(tk.LabelFrame):
    def __init__(self, master, fes, tacton):
        tk.LabelFrame.__init__(
            self, master, text='Channel ' + str(tacton.channel))
        self.pack()
        self.fes = fes
        self.tacton = tacton
        self.is_playing = False

        self.button_play = tk.Button(self, text='Play', command=self.play)
        self.button_stop = tk.Button(self, text='Stop', command=self.stop)
        self.update_buttons()
        self.button_play.grid(row=0, column=0)
        self.button_stop.grid(row=1, column=0)

        row = 0
        column = 1
        tk.Label(self, text='Amplitude').grid(row=row, column=column)
        self.sb_amplitude = tk.Spinbox(self, from_=1, to=20, width=5,
                                       command=self.update_amplitude)
        self.sb_set_default(self.sb_amplitude, self.tacton.amplitude)
        self.sb_amplitude.grid(row=row, column=column + 1)

        column += 2
        tk.Label(self, text='Pulse width').grid(row=row, column=column)
        self.sb_pulse_width = tk.Spinbox(self, from_=0, to=500, width=5,
                                         command=self.update_pulse_width)
        self.sb_set_default(self.sb_pulse_width, self.tacton.pulse_width)
        self.sb_pulse_width.grid(row=row, column=column + 1)

        column += 2
        tk.Label(self, text='Length [s]').grid(row=row, column=column)
        self.sb_duration = tk.Spinbox(self, from_=-1, to=60, width=5,
                                      command=self.update_duration)
        self.sb_set_default(self.sb_duration, self.tacton.duration)
        self.sb_duration.grid(row=row, column=column + 1)

        row = 1
        column = 1
        tk.Label(self, text='Frequency').grid(row=row, column=column)
        self.scale_frequency = tk.Scale(self, from_=1, to=255, length=400,
                                        orient=tk.HORIZONTAL, command=self.update_frequency)
        self.scale_frequency.set(self.tacton.frequency)
        self.scale_frequency.grid(row=row, column=column + 1, columnspan=6)

    def play(self):
        self.is_playing = True
        self.update_fes()
        self.update_buttons()

    def update_buttons(self):
        if self.is_playing:
            self.button_stop.config(state=tk.NORMAL)
            self.button_play.config(state=tk.DISABLED)
        else:
            self.button_stop.config(state=tk.DISABLED)
            self.button_play.config(state=tk.NORMAL)

    def sb_set_default(self, sb, value):
        sb.delete(0, 'end')
        sb.insert(0, value)

    def stop(self):
        if self.is_playing:
            self.fes.stop(self.tacton)
            self.is_playing = False
            self.update_buttons()

    def update_fes(self):
        if self.is_playing:
            self.is_playing = self.fes.stimulate(self.tacton)

    def update_amplitude(self):
        self.tacton.amplitude = int(self.sb_amplitude.get())
        self.update_fes()

    def update_pulse_width(self):
        self.tacton.pulse_width = int(self.sb_pulse_width.get())
        self.update_fes()

    def update_frequency(self, value):
        self.tacton.frequency = int(value)
        self.update_fes()

    def update_duration(self):
        self.tacton.duration = int(self.sb_duration.get())
        self.update_fes()


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

    root = tk.Tk()
    for c in range(1, 9):
        tacton = Tacton(channel=c, frequency=1, amplitude=7,
                        duration=-1, pulse_width=310)
        UIChannelControl(root, fes, tacton)
    root.mainloop()
    fes.stop()
    fes.disconnect()
