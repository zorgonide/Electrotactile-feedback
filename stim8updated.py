import serial
import struct
import sys
import time
import threading
# stub serial connection for debugging purposes


class SerialStub(object):
    in_waiting = 0

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.response = None

    def write(self, msg):
        print("SerialStub[{},{}]: {}".format(self.port, self.baudrate, msg))

    def read(self, num_bytes):
        if not isinstance(self.response, list):
            return None
        # return everything in buffer if buffer smaller or equal to num_bytes
        if len(self.response) <= num_bytes:
            response = self.response
            self.response = None
            self.in_waiting = 0
        # pop first num_bytes elements from buffer, leaving at least one
        else:
            response = self.response[0:num_bytes]
            self.response = self.response[num_bytes:]
            self.in_waiting = len(self.response)
        # avoid returning single element lists
        return response if len(response) is not 1 else response[0]

    def isOpen(self):
        return True

    def close(self):
        pass

    def set_response(self, response):
        self.response = None
        self.in_waiting = 0
        if isinstance(response, list):
            self.response = response
            self.in_waiting = len(self.response)
            return True
        else:
            print(
                "WARNING: response must be an instance of list - setting response to None instead.")
            return False


""" wrapper for channel properties """


class Tacton:
    def __init__(self, channel, amplitude, pulse_width=310, frequency=-1, duration=-1):
        self.channel = channel
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration  # controller stops after n seconds if duration > 0
        self.pulse_width = pulse_width


class FESDriver:
    def __init__(self, port, baudrate, debug=False):
        self.port = port
        self.baudrate = baudrate
        self.debug = debug
        self.is_connected = False
        self.serial = None

    def connect(self):
        if self.is_connected:
            self.disconnect()
        print('Opening serial connection to FES stimulator on port {} with baudrate {}'.format(
            self.port, self.baudrate))
        if self.debug:
            self.serial = SerialStub(self.port, self.baudrate)
        else:
            try:
                self.serial = serial.Serial(
                    self.port, self.baudrate, timeout=5)
            except serial.SerialException as err:
                print("SerialException: {0}".format(err))
                print("Unexpected error:", sys.exc_info()[0])
                return False
        if self.serial.isOpen():  # type: ignore
            self.is_connected = True
            return True
        else:
            # This should not be happening
            print('WARNING: Serial port not open despite successful initialization!')
            return False

    # Close the serial port if connected
    def disconnect(self):
        if not self.is_connected:
            return
        self.serial.close()  # type: ignore
        self.is_connected = False
        self.serial = None

    # Send command over serial and wait for response bytes with timeout
    def _send(self, message, min_bytes=4):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return
        self._clear_input_buffer()
        self.serial.write(message)  # type: ignore
        time.sleep(0.005)
        return self._wait_response(min_bytes=min_bytes)

    # Wait for response from serial of length min_bytes
    def _wait_response(self, min_bytes=4, timeout=3):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return
        tic = time.time()
        num_bytes = 0
        data = []
        while num_bytes < min_bytes:
            toc = time.time()
            if toc - tic > timeout:
                msg = self._clear_input_buffer()
                print("FES:inputError - Incomplete message from FES")
                print(msg)
                break
            if num_bytes < self.serial.in_waiting:  # type: ignore
                num_bytes = self.serial.in_waiting  # type: ignore
                tic = time.time()
        if num_bytes >= min_bytes:
            data = self._clear_input_buffer()
        return data

    # Pop and return all data from the serial input buffer
    def _clear_input_buffer(self):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return
        data = []
        for _ in range(self.serial.in_waiting):  # type: ignore
            data.append(self.serial.read(1))  # type: ignore
        return data

    def set_channel_amplitude(self, channel, amplitude):
        if not self._check_channel(channel) or not self._check_amplitude(amplitude):
            return
        byte_no, command, response_bytes = 2, 26, 4
        data = [byte_no, command, channel, amplitude]
        checksum = sum(data) % 256
        data = self._send(data + [checksum], min_bytes=response_bytes)
        return data

    def set_channel_frequency(self, channel, frequency):
        if not self._check_channel(channel) or not self._check_frequency(frequency):
            return
        byte_no, command, response_bytes = 3, 3, 4
        fq1, fq2 = divmod(frequency, 256)
        data = [byte_no, command, channel, fq1, fq2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_channel_pulsewidth(self, channel, pulsewidth):
        if not self._check_channel(channel) or not self._check_pulsewidth(pulsewidth):
            return
        byte_no, command, response_bytes = 3, 7, 4
        pw1, pw2 = divmod(pulsewidth, 256)
        data = [byte_no, command, channel, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # Update amplitude and pulsewidth of a single channel
    def set_channel_amplitude_pulsewidth(self, channel, amplitude, pulsewidth):
        if not self._check_channel(channel) or \
                not self._check_amplitude(amplitude) or \
                not self._check_pulsewidth(pulsewidth):
            return
        bytes_no, command, response_bytes = 4, 1, 4
        pw1, pw2 = divmod(pulsewidth, 256)
        data = [bytes_no, command, channel, amplitude, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_global_amplitude(self, amplitude):
        if not self._check_amplitude(amplitude):
            return
        byte_no, command, response_bytes = 1, 28, 4
        data = [byte_no, command, amplitude]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_global_frequency(self, frequency):
        if not self._check_frequency(frequency):
            return
        byte_no, command, response_bytes = 1, 2, 4
        data = [byte_no, command, frequency]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # Update pulsewidth for all channels
    def set_global_pulsewidth(self, pulsewidth):
        if not self._check_pulsewidth(pulsewidth):
            return
        byte_no, command, response_bytes = 2, 4, 4
        pw1, pw2 = divmod(pulsewidth, 256)
        data = [byte_no, command, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # Reset all parameters to startup configuration
    def reset(self):
        byte_no, command, checksum, response_bytes = 0, 32, 32, 2
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # Manually refresh LCD to display the latest channel settings
    def refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 23, 23, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # By default, the LCD screen does not refresh automatically after each
    # change of parameters to preserve battery. Updates to the LCD screen can
    # be performed manually (see refresh_lcd), or you can activate this globally
    # using enable_refresh_lcd
    def enable_refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 24, 24, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # Disables refreshing the screen after parameter updates by default.
    def disable_refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 25, 25, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # Get device firmware version
    def read_version(self):
        byte_no, command, checksum, response_bytes = 0, 8, 8, 7
        return self._send([byte_no, command, checksum], min_bytes=2)

    def stimulate(self, tacton):
        print('Stimulating {}'.format(vars(tacton)))
        start = time.time()
        self.set_channel_amplitude_pulsewidth(
            tacton.channel, tacton.amplitude, tacton.pulse_width)
        self.set_channel_frequency(tacton.channel, tacton.frequency)
        if tacton.duration > 0:
            time.sleep(tacton.duration - (time.time() - start))
            self.stop(tacton)
            return False
        else:
            return True

    def stimulate_channels(self, tactons):
        threads = []
        for tacton in tactons:
            thread = threading.Thread(target=self.stimulate, args=(tacton,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def stop(self, tacton=None):
        if tacton is None:
            print("Stopping stimulation on all channels.")
            self.reset()
        else:
            print('Stopping stimulation on channel {}'.format(tacton.channel))
            self.set_channel_amplitude_pulsewidth(
                tacton.channel, tacton.amplitude, 0)

    @staticmethod
    def _check_channel(channel):
        if channel < 1 or channel > 8:
            print("WARNING: channel {} out of range [1, 8].".format(channel))
            return False
        return True

    @staticmethod
    def _check_amplitude(amplitude):
        if amplitude < -1 or amplitude > 50:
            print(
                "WARNING: amplitude {} out of range [-1, 50].".format(amplitude))
            return False
        return True

    @staticmethod
    def _check_pulsewidth(pulsewidth):
        if pulsewidth < 0 or pulsewidth > 500:
            print(
                "WARNING: pulsewidth {} out of range [0, 500]".format(pulsewidth))
            return False
        return True

    @staticmethod
    def _check_frequency(frequency):
        if frequency < 0 or frequency > 100:
            print(
                "WARNING: frequency {} out of range [1, 99]".format(frequency))
            return False
        return True


if __name__ == "__main__":
    port = 'COM3'
    baudrate = 38400
    if len(sys.argv) > 1:
        port = sys.argv[1]
    dev = FESDriver(port, baudrate)
    dev.connect()
    # by default, the device does not update the display to preserve battery.
    #print("Enabling LCD")
    # dev.enable_refresh_lcd()
    print("Setting channel amplitude")
    dev.set_channel_amplitude(2, 7)
    print("Setting channel amplitude and pulsewidth")
    dev.set_channel_amplitude_pulsewidth(2, 8, 300)
    print("Setting pulsewidth of all channels.")
    dev.set_global_pulsewidth(310)
    print("Setting frequency of all channels.")
    dev.set_global_frequency(17)
    print("Setting amplitude of all channels.")
    dev.set_global_amplitude(4)
    print("Setting channel pulsewidth")
    dev.set_channel_pulsewidth(2, 110)
    print("Setting channel frequency")
    dev.set_channel_frequency(3, 33)
    print("Resetting device")
    dev.reset()
    dev.disconnect()
