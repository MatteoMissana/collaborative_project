# Collaborative Project - Voice-Controlled Robotic Arm

## Overview

This project involves controlling a robotic arm using voice commands, evaluating system performance through accuracy and confusion matrices, and managing the robot's functionality via Arduino code. The code works on windows but can be easily adapted for other operating systems

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MatteoMissana/collaborative_project
   cd collaborative_project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. If you don't have FFMPEG installed, install it following this guide:

https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

---

## Project Structure

- **`main.py`**  
  The main script for implementing and managing voice commands.

- **`valutazione_accuracy.py`**  
  A script to evaluate system accuracy and generate confusion matrices.

- **`./arduino_robarm/`**  
  This folder contains the Arduino code for the robotic arm.

---

## Vocal Commands

The following voice commands are supported to interact with the robotic arm:

### **Robotic Arm Commands**
- **Down**:  
  - `DOWN SLOW`  
  - `DOWN FAST`  
- **Up**:  
  - `UP SLOW`  
  - `UP FAST`  
- **Repetitive Movements**:  
  - `MOVEMENT 1`, `MOVEMENT 2`, `MOVEMENT 3`, `MOVEMENT 4`, `MOVEMENT 5`

### **Velocity Control**
- `FASTER`  
- `SLOWER`

### **Amplitude Control**
- `LONGER`  
- `SHORTER`

### **Saving Movements**
- Save specific positions:  
  - `POSITION 1`, `POSITION 2`, `POSITION 3`, `POSITION 4`, `POSITION 5`

### **Stopping the Robot**
- `ROBOT STOP`

---

## General Usage Guidelines

1. Speak clearly for optimal recognition.  
2. Wait for the beep sound before issuing a command.  
3. Saved movements can be reviewed in the `movements.txt` file.  

For additional details or troubleshooting, refer to the project documentation or contact the contributors.

---

Feel free to reach out for further assistance or inquiries!