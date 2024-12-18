import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import defaultdict
import pandas as pd

# Directory dei risultati salvati
results_dir = "test_results"


# Funzione per leggere e combinare le confusion matrices
def combine_confusion_matrices(results_dir):
    combined_matrices = defaultdict(lambda: None)

    for subdir, _, files in os.walk(results_dir):
        for file in files:
            if file.startswith("confusion_matrix_threshold_") and file.endswith(".csv"):
                threshold = float(file.split("_")[-1].replace(".csv", ""))
                filepath = os.path.join(subdir, file)

                # Legge la matrice
                matrix = np.loadtxt(filepath, delimiter=",", skiprows=1)
                header = open(filepath).readline().strip().split(",")

                # Somma le matrici
                if combined_matrices[threshold] is None:
                    combined_matrices[threshold] = matrix
                else:
                    combined_matrices[threshold] += matrix

    return combined_matrices, header


# Funzione per calcolare le accuratezze totali
def calculate_total_accuracies(combined_matrices, header):
    threshold_accuracies = defaultdict(dict)

    for threshold, matrix in combined_matrices.items():
        total_correct = np.trace(matrix)
        total_samples = matrix.sum()
        overall_accuracy = 100.0 * total_correct / total_samples if total_samples > 0 else 0.0

        # Calcola accuratezze per comando
        for i, command in enumerate(header):
            command_samples = matrix[i, :].sum()
            command_correct = matrix[i, i]
            accuracy = 100.0 * command_correct / command_samples if command_samples > 0 else 0.0
            threshold_accuracies[threshold][command] = accuracy

        threshold_accuracies[threshold]["Overall"] = overall_accuracy

    return threshold_accuracies


# Funzione per caricare accuracies.json
def load_json_accuracies(results_dir):
    all_accuracies = defaultdict(lambda: defaultdict(list))

    for subdir, _, files in os.walk(results_dir):
        for file in files:
            if file == "accuracies.json":
                filepath = os.path.join(subdir, file)
                with open(filepath, "r") as f:
                    accuracies = json.load(f)
                    for command, values in accuracies.items():
                        for i, value in enumerate(values):
                            all_accuracies[i][command].append(value)

    return all_accuracies


# Funzione per visualizzare confusion matrices
def plot_confusion_matrices(combined_matrices, header):
    for threshold, matrix in combined_matrices.items():
        plt.figure(figsize=(10, 8))
        sns.heatmap(matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=header, yticklabels=header)
        plt.title(f"Confusion Matrix at Threshold {threshold:.1f}")
        plt.xlabel("Recognized Commands")
        plt.ylabel("Actual Commands")
        plt.tight_layout()
        plt.show()


# Main
combined_matrices, header = combine_confusion_matrices(results_dir)
threshold_accuracies = calculate_total_accuracies(combined_matrices, header)
all_accuracies = load_json_accuracies(results_dir)

# Visualizzazione matrici di confusione
plot_confusion_matrices(combined_matrices, header)

# Stampa accuratezze
print("\nAccuratezze per soglia e comando:")
for threshold, accuracies in threshold_accuracies.items():
    print(f"\nThreshold {threshold:.1f}:")
    for command, accuracy in accuracies.items():
        print(f"  {command}: {accuracy:.2f}%")

# Accuratezza dal file JSON
print("\nAccuratezze aggregate da accuracies.json:")
for threshold, commands in all_accuracies.items():
    print(f"\nThreshold {threshold}:")
    for command, acc_list in commands.items():
        print(f"  {command}: {np.mean(acc_list):.2f}% (media), valori: {acc_list}")
