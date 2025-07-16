
"""
===-*- Polynominal Interpolation Tool -*-===
=====-*- General -*-=====
Copyright (c) makkiblog.com
MIT License 
coding: utf-8

===-*- VERSION -*-===
v0.0 Initial Release
vvvCODEvvv
"""

import numpy as np
import tkinter as tk
from tkinter import filedialog
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import csv

def open_csv_file():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_csv_file(file_path)

def process_csv_file(file_path):
    # Read CSV file
    psd_values = []
    cw_values = []
    tw_values = []
    
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Skip empty rows
            if not row:
                continue
                
            # Try to parse the row
            try:
                # Remove any extra whitespace and split if necessary
                row_data = [item.strip() for item in row]
                
                # If there's only one column, it might be space-separated
                if len(row_data) == 1 and ' ' in row_data[0]:
                    row_data = row_data[0].split()
                
                # Ensure we have exactly 3 values
                if len(row_data) >= 3:
                    psd_values.append(float(row_data[0]))
                    cw_values.append(float(row_data[1]))
                    tw_values.append(float(row_data[2]))
            except:
                # Skip rows that can't be converted to float
                continue
    
    # Perform polynomial regression
    psd = np.array(psd_values)
    cw = np.array(cw_values)
    tw = np.array(tw_values)
    
    # Combine CW and TW into a feature matrix
    X = np.column_stack((cw, tw))
    
    # Create a polynomial regression model of degree 2
    model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model.fit(X, psd)
    
    # Get the coefficients
    poly_features = model.named_steps['polynomialfeatures']
    linear_regression = model.named_steps['linearregression']
    coefficients = linear_regression.coef_
    intercept = linear_regression.intercept_
    
    # Get the feature names to understand the order of coefficients
    feature_names = poly_features.get_feature_names_out(['CW', 'TW'])
    
    # Create a dictionary mapping features to coefficients
    coef_dict = {feature: coef for feature, coef in zip(feature_names, coefficients)}
    coef_dict['intercept'] = intercept
    
    # Create the equation string
    equation = f"PSD = {coef_dict['intercept']:.6f}"
    for feature, coef in coef_dict.items():
        if feature != 'intercept':
            equation += f" + ({coef:.6f} * {feature})"
    
    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Data Points:\n")
    result_text.insert(tk.END, "PSD\tCW\tTW\n")
    for i in range(len(psd)):
        result_text.insert(tk.END, f"{psd[i]:.6f}\t{cw[i]:.6f}\t{tw[i]:.6f}\n")
    
    result_text.insert(tk.END, "\nPolynomial Regression Results:\n")
    result_text.insert(tk.END, f"{equation}\n\n")
    
    # Simplify the equation by removing terms with very small coefficients
    simplified_eq = f"PSD = {coef_dict['intercept']:.6f}"
    for feature, coef in coef_dict.items():
        if feature != 'intercept' and abs(coef) > 1e-10:
            simplified_eq += f" + ({coef:.6f} * {feature})"
    
    result_text.insert(tk.END, "Simplified Equation:\n")
    result_text.insert(tk.END, f"{simplified_eq}\n")
    
    # Enable export button
    export_button.config(state=tk.NORMAL)
    
    # Store results for export
    global results_to_export
    results_to_export = {
        'psd': psd,
        'cw': cw,
        'tw': tw,
        'equation': equation,
        'simplified_eq': simplified_eq
    }

def export_results():
    file_path = filedialog.asksaveasfilename(
        title="Save Results",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if file_path:
        with open(file_path, 'w') as f:
            # Write the data points
            f.write("Data Points:\n")
            f.write("PSD\tCW\tTW\n")
            for i in range(len(results_to_export['psd'])):
                f.write(f"{results_to_export['psd'][i]:.6f}\t{results_to_export['cw'][i]:.6f}\t{results_to_export['tw'][i]:.6f}\n")
            
            f.write("\nPolynomial Regression Results:\n")
            f.write(f"{results_to_export['equation']}\n\n")
            
            f.write("Simplified Equation:\n")
            f.write(f"{results_to_export['simplified_eq']}\n")

# Create the main window
root = tk.Tk()
root.title("Polynomial Regression Tool")
root.geometry("500x350")

# Global variable to store results
results_to_export = None

# Create UI elements
frame = tk.Frame(root)
frame.pack(pady=10)

open_button = tk.Button(frame, text="Select CSV File", command=open_csv_file)
open_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(frame, text="Export Results", command=export_results, state=tk.DISABLED)
export_button.pack(side=tk.LEFT, padx=5)

# Text widget to display results
result_text = tk.Text(root, height=15, width=60)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add a scrollbar
scrollbar = tk.Scrollbar(result_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

# Start the application
root.mainloop()