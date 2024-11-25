class Repetitive:
    """
    A class to represent a system with adjustable speed and amplitude,
    allowing for configuration, saving settings to a text file, and encoding values.

    Attributes:
    - speed (int): Current speed level (1-5).
    - max_speed (int): Maximum allowed speed level.
    - amplitude (int): Current amplitude level (1-5).
    - max_amplitude (int): Maximum allowed amplitude level.
    - txt_path (str): Path to the text file where settings are saved.
    """
    def __init__(self, speed, amplitude, txt_path):
        """
        Initializes the Repetitive object with speed, amplitude, and a text file path.

        Parameters:
        - speed (int): Initial speed level.
        - amplitude (int): Initial amplitude level.
        - txt_path (str): Path to the text file for saving settings.
        """
        self.speed = speed
        self.max_speed = 5  # Maximum speed level
        self.amplitude = amplitude
        self.max_amplitude = 5  # Maximum amplitude level
        self.txt_path = txt_path

    def speed_up(self):
        """
        Increases the speed by 1, if it is below the maximum allowed speed.
        """
        if self.speed <= self.max_speed:
            self.speed = self.speed + 1  # Increment speed

    def speed_down(self):
        """
        Decreases the speed by 1, if it is above the minimum allowed speed (1).
        """
        if self.speed >= 1:
            self.speed = self.speed - 1  # Decrement speed

    def amplitude_up(self):
        """
        Increases the amplitude by 1, if it is below the maximum allowed amplitude.
        """
        if self.amplitude <= self.max_amplitude:
            self.amplitude = self.amplitude + 1  # Increment amplitude

    def amplitude_down(self):
        """
        Decreases the amplitude by 1, if it is above the minimum allowed amplitude (1).
        """
        if self.amplitude >= 1:
            self.amplitude = self.amplitude - 1  # Decrement amplitude

    def save_on_txt(self):
        """
        Saves the current speed and amplitude values to a text file in the format:
        "speed,amplitude\n".
        """
        # Open the file in write mode
        txt_file = open(self.txt_path, 'w')
        # Create a string representation of the speed and amplitude
        string = f"{self.speed},{self.amplitude}\n"
        # Write the string to the file
        txt_file.write(string)
        # Close the file
        txt_file.close()

    def encode_numbers(self):
        """
        Encodes the current speed and amplitude as a single character based on the formula:
        ASCII character = ((speed - 1) * 5 + (amplitude - 1)) + 65.

        Returns:
        - A single character encoding the speed and amplitude.
        """
        offset = 65  # ASCII value of 'A'
        # Calculate the encoded character based on speed and amplitude
        encoded_char = chr((self.speed - 1) * 5 + (self.amplitude - 1) + offset)
        return encoded_char




