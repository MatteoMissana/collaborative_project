class Repetitive:
    def __init__(self, speed, amplitude, txt_path):
        self.speed = speed
        self.max_speed = 5
        self.amplitude = amplitude
        self.max_amplitude = 5
        self.txt_path = txt_path
    def speed_up(self):
        if self.speed <= self.max_speed:
            self.speed = self.speed + 1

    def speed_down(self):
        if self.speed >= 1:
            self.speed = self.speed - 1

    def amplitude_up(self):
        if self.amplitude <= self.max_amplitude:
            self.amplitude = self.amplitude + 1

    def amplitude_down(self):
        if self.amplitude >= 1:
            self.amplitude = self.amplitude - 1

    def save_on_txt(self):
        txt_file = open(self.txt_path, 'w')
        string = f"{self.speed},{self.amplitude}\n"
        txt_file.write(string)
        txt_file.close()

    def encode_numbers(self):
        offset = 65  # Base ASCII (usiamo 'A' come primo carattere)
        encoded_char = chr((self.speed - 1) * 5 + (self.amplitude - 1) + offset)
        return encoded_char



