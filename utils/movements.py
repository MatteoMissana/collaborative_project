class Txtfile:
    def __init__(self, path):
        self.maxlines = 5
        self.path = path
    def save_line(self, line, line_number):
        """
        Saves the line to a specific line of the text file in the format:
        "speed,amplitude\n".
        line: the line to save
        line_number: the line index to save the line
        """
        # Open the file in read mode
        txt_file = open(self.path, 'r')
        # read the lines
        lines = txt_file.readlines()
        # Close the file
        txt_file.close()

        if lines[line_number] == '\n':
            # Write the string to the file
            lines[line_number] = line
            # write the new lines
            with open(self.path, 'w') as file:
                file.writelines(lines)
        else:
            print('The movement is already occupied, delete the movement or save it in another position')

    def delete_line(self, line_number):
        '''
        Deletes a specific line of the text file if it exists
        :param line_number: the line to delete
        '''
        # Open the file in read mode
        txt_file = open(self.path, 'r')
        # read the lines
        lines = txt_file.readlines()
        # Close the file
        txt_file.close()

        if lines[line_number] == '\n':
            print('There\'s no movement in the position you selected')
        else:
            # Write the string to the file
            lines[line_number] = '/n'
            # write the new lines
            with open(self.path, 'w') as file:
                file.writelines(lines)


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

    def save_settings(self, line_number):
        '''
        function that saves the current speed and amplitude to a text file in a certain line of the text file.
        :param line_number: the line to save the settings to.
        '''
        txtfile = Txtfile(self.txt_path)
        txtfile.save_line(f"Speed {self.speed}, Amplitude {self.amplitude}", line_number)

class Other_movement:
    def __init__(self):
        self.message = 'The current movement cannot be saved. Only repetitive movements can be saved'

    def save_settings(self, line_number):
        '''
        Questa è solo una funzione per rispondere al caso in cui chiamo save movement quando il movimento non è ripetitivo

        :param line_number: number of the line to save the settings to.
        :return:
        '''
        print(self.message)



