import utils.general as utils  # Import utils file with the needed function
import numpy as np
import matplotlib.pyplot as plt
import pvporcupine
import seaborn as sns
import whisper
import os
import json

access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="

model = whisper.load_model("base")  # Load the Whisper transcription model

keyword_paths = [r'rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/robot-stop_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/save-movement_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/amplitude-change_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/velocity-change_en_windows_v3_0_0.ppn']  # Change them if you have a mac

handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)

commands_to_test = ["up fast", "up slow", "down fast", "down slow",
                    "repetitive", "movement 1",
                    "movement 2", "movement 3", "movement 4", "movement 5"]

thresholds = np.array([0.4, 0.5, 0.6])
n_repetitions = 10  # Number of repetitions to test for each command
accuracies = {command: [] for command in commands_to_test}
sample_rate = handle.sample_rate

# Initialization of a data structure needed to build the confusion matrix
confusion_matrices = {threshold: np.zeros((len(commands_to_test), len(commands_to_test)), dtype=int) for threshold in
                      thresholds}

# Testing for each command and each threshold
for command_index, command in enumerate(commands_to_test):
    print(f"ATTENTION!!! the next command to be tested will be: {command}")
    utils.beep()
    utils.beep()
    utils.beep()
    for threshold in thresholds:
        correct_count = 0

        for _ in range(n_repetitions):
            print(f"\nTestando il comando: '{command}'")
            # Record audio and trsìanscribe it with Whisper
            detection = utils.on_keyword_detected(0, sample_rate, model)
            if not detection.strip():
                continue  # Skip if the transcription is empty

            # Comparison
            index, match = utils.compare_with_commands(commands_to_test, detection, threshold)
            if match:
                confusion_matrices[threshold][command_index, index] += 1

            if commands_to_test[index] == command:
                correct_count += 1

            print(f"Detection: {detection}, Command: {commands_to_test[index]}")

        # Accuracy estimation
        total_tests = n_repetitions
        accuracy = (correct_count / total_tests) * 100
        accuracies[command].append(accuracy)
        print(f"Threshold {threshold:.1f} - Accuratezza: {accuracy:.2f}%")

# Visualization of the confuzion matrix
for threshold, matrix in confusion_matrices.items():
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=commands_to_test, yticklabels=commands_to_test)
    plt.title(f"Confusion Matrix at Threshold {threshold:.1f}")
    plt.xlabel("Recognized Commands")
    plt.ylabel("Actual Commands")
    plt.tight_layout()
    plt.show()

# Accuracy plot
plt.figure(figsize=(12, 6))
for command, acc in accuracies.items():
    plt.plot(thresholds, acc, label=f"Command: {command}")
plt.xlabel("Threshold")
plt.ylabel("Accuracy (%)")
plt.title("Performance Across Different Thresholds")
plt.legend(loc="best")
plt.grid()
plt.tight_layout()
plt.show()

# Trova un percorso incrementale per la directory dei risultati
base_output_dir = "test_results/exp"
output_dir = base_output_dir
counter = 1

while os.path.exists(output_dir):  # Incrementa il percorso finché non troviamo uno disponibile
    output_dir = f"{base_output_dir}{counter}"
    counter += 1

os.makedirs(output_dir)  # Crea la directory
print(f"Results will be saved in: {output_dir}")

# Salva le matrici di confusione
for threshold, matrix in confusion_matrices.items():
    matrix_filename = os.path.join(output_dir, f"confusion_matrix_threshold_{threshold:.1f}.csv")
    np.savetxt(matrix_filename, matrix, delimiter=",", fmt="%d",
               header=",".join(commands_to_test), comments="")
    print(f"Confusion matrix saved to {matrix_filename}")

# Salva le accuratezze
accuracies_filename = os.path.join(output_dir, "accuracies.json")
with open(accuracies_filename, "w") as f:
    json.dump(accuracies, f, indent=4)
print(f"Accuracies saved to {accuracies_filename}")