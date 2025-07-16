"""
===-*- Vibration waterfall Tool -*-===
=====-*- General -*-=====
Copyright (c) makkiblog.com
MIT License 
coding: utf-8

===-*- VERSION -*-===
v0.0 Initial Release
vvvCODEvvv
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def select_file():
    # Create a simple tkinter window (it won't actually show)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    # Close the hidden window
    root.destroy()
    
    return file_path

def create_vibration_3d_plot(csv_file):
    # Read the CSV file, skipping the first 3 rows
    detected_encoding = detect_encoding(csv_file)
    df = pd.read_csv(csv_file, header=9, encoding=detected_encoding)
    
    # Get the x-axis range and values
    y_values = df.iloc[:, 0].values
    y_min, y_max = y_values.min(), y_values.max()
    
    # Scale y-values to match x-value range
    x_original = np.arange(len(df.columns) - 1)  # Original measurement indices
    print(x_original)
    #x_scaled = (x_original - x_original.min()) * (y_max - y_min) / (x_original.max() - x_original.min())
    x_scaled = (x_original - x_original.min()) * (300000 - 0) / (x_original.max() - x_original.min())
    print(x_scaled)
    
    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(
        z=df.iloc[:, 1:].values,
        x=x_scaled,
        y=y_values,
        colorscale='Viridis',
        opacity=0.8,
        showscale=False
    )])
    
    # Customize the plot appearance
    fig.update_layout(
        scene=dict(
            xaxis_title='Measurement rpm',
            yaxis_title='Speed rpm',
            zaxis_title='Magnitude',
            aspectratio=dict(
                x=1,
                y=1,
                z=1
            ),
            yaxis=dict(
                range=[y_min, y_max]  # Match x-axis range
            )
        ),
        width=1920,
        height=1200,
        title='3D Vibration Analysis Surface Plot'
    )
    return fig



def save_2d_visualization(csv_file):
    """Create and save a 2D heatmap visualization"""
    detected_encoding = detect_encoding(csv_file)
    df = pd.read_csv(csv_file, header=9, encoding=detected_encoding)
    
    # Get the x-axis range and values
    y_values = df.iloc[:, 0].values
    y_min, y_max = y_values.min(), y_values.max()
    
    # Scale x-values
    x_original = np.arange(len(df.columns) - 1)
    x_scaled = (x_original - x_original.min()) * (300000 - 0) / (x_original.max() - x_original.min())
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create the 2D heatmap
    z_data = df.iloc[:, 1:].values
    im = plt.pcolormesh(x_scaled, y_values, z_data, cmap='jet',vmin=0,vmax=3)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Magnitude')
    
    # Set labels and title
    plt.xlabel('Measurement rpm')
    plt.ylabel('Speed rpm')
    plt.title('2D Vibration Analysis Heatmap')
    
    # Save the figure
    plt.savefig(file_path+'_2d.png', dpi=300, bbox_inches='tight')
    plt.show()
    #plt.close()  # Clean up memory
    

# Main script
if __name__ == "__main__":
    # Get the file path from the dialog
    file_path = select_file()
    
    if file_path:
        # Create and show the plot
        fig = create_vibration_3d_plot(file_path)
        save_2d_visualization(file_path) 
        fig.show()