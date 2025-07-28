"""
===-*- data deviation creation Tool -*-===
=====-*- General -*-=====
Copyright (c) makkiblog.com
MIT License 
coding: utf-8
type -h for help

===-*- VERSION -*-===
v0.0 Initial Release
vvvCODEvvv
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import sys

def read_data_from_file(filename):
    """
    Read numerical data from a text file.
    Handles various formats: space-separated, comma-separated, or one value per line.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read().strip()
        
        # Try different parsing methods
        data = []
        
        # First, try to split by whitespace and commas
        values = content.replace(',', ' ').split()
        
        for value in values:
            try:
                data.append(float(value))
            except ValueError:
                continue  # Skip non-numeric values
        
        if len(data) == 0:
            raise ValueError("No valid numerical data found in the file")
        
        return np.array(data)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {str(e)}")
        sys.exit(1)

def save_modified_data_to_file(filename, modified_data):
    """
    Save the modified data values to a single-column text file (CSV-compatible).
    One value per line for easy CSV reading.
    
    Args:
        filename: Output filename
        modified_data: Array of modified values
    """
    try:
        with open(filename, 'w') as file:
            for value in modified_data:
                file.write(f"{value:.6f}\n")
        
        print(f"Modified data saved to: {filename}")
        print(f"Format: Single column, one value per line (CSV-compatible)")
    
    except Exception as e:
        print(f"Error saving file '{filename}': {str(e)}")
        sys.exit(1)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description='Add random deviations to numerical data and output modified values in single column format.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py data.txt                    # Use default 0.5σ deviation
  python script.py data.txt -d 1.0             # Use 1.0σ deviation
  python script.py data.txt -d 0.25 --show-stats  # Use 0.25σ and show original stats
  python script.py data.txt -s 42              # Set seed for reproducible results

Output format:
  - Single column text file (.txt extension)
  - One value per line
  - CSV-compatible format
  - 6 decimal places precision
        """
    )
    
    parser.add_argument('input_file', 
                       help='Input text file containing numerical data')
    parser.add_argument('-d', '--deviation', 
                       type=float, 
                       default=0.5,
                       help='Deviation multiplier (multiple of sigma, default: 0.5)')
    parser.add_argument('--show-stats', 
                       action='store_true',
                       help='Display original dataset statistics')
    parser.add_argument('-s', '--seed', 
                       type=int, 
                       default=None,
                       help='Random seed for reproducible results')
    parser.add_argument('--no-plot', 
                       action='store_true',
                       help='Skip generating plots')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    if args.deviation <= 0:
        print("Error: Deviation multiplier must be positive.")
        sys.exit(1)
    
    # Set random seed if provided
    if args.seed is not None:
        np.random.seed(args.seed)
        print(f"Random seed set to: {args.seed}")
    
    # Read data from file
    print(f"Reading data from: {args.input_file}")
    data = read_data_from_file(args.input_file)
    print(f"Successfully loaded {len(data)} data points")
    
    # Calculate basic statistics
    mean_value = np.mean(data)
    std_dev = np.std(data, ddof=0)  # Population standard deviation
    variance = np.var(data, ddof=0)
    
    # Display original statistics if requested
    if args.show_stats:
        print("\n=== Original Dataset Statistics ===")
        print(f"Number of data points: {len(data)}")
        print(f"Mean: {mean_value:.6f}")
        print(f"Standard Deviation (σ): {std_dev:.6f}")
        print(f"Variance (σ²): {variance:.6f}")
        print(f"Min value: {np.min(data):.6f}")
        print(f"Max value: {np.max(data):.6f}")
    
    # Generate random deviations with the specified multiplier
    # The standard deviation of the random deviations will be deviation_multiplier * original_std_dev
    deviation_std = args.deviation * std_dev
    random_deviations = np.random.normal(0, deviation_std, len(data))
    
    # Add random deviations to original data
    modified_data = data + random_deviations
    
    print(f"\n=== Random Deviations Applied ===")
    print(f"Deviation multiplier: {args.deviation}σ")
    print(f"Original standard deviation: {std_dev:.6f}")
    print(f"Random deviation standard deviation: {deviation_std:.6f}")
    print(f"Theoretical range (±3σ): ±{3 * deviation_std:.6f}")
    print(f"Actual min deviation: {np.min(random_deviations):.6f}")
    print(f"Actual max deviation: {np.max(random_deviations):.6f}")
    
    print(f"\n=== Modified Dataset Statistics ===")
    print(f"New Mean: {np.mean(modified_data):.6f}")
    print(f"New Standard Deviation: {np.std(modified_data, ddof=0):.6f}")
    print(f"New Min value: {np.min(modified_data):.6f}")
    print(f"New Max value: {np.max(modified_data):.6f}")
    
    # Generate output filename
    base_name = os.path.splitext(args.input_file)[0]
    output_filename = f"{base_name}_deviation.txt"
    
    # Save the modified data to file (single column format)
    save_modified_data_to_file(output_filename, modified_data)
    
    # Display sample comparison
    print(f"\n=== Sample Comparison (First 10 values) ===")
    print("Original    | Random Dev  | Modified")
    print("-" * 40)
    for i in range(min(10, len(data))):
        print(f"{data[i]:10.6f} | {random_deviations[i]:10.6f} | {modified_data[i]:10.6f}")
    
    # Create visualization (unless disabled)
    if not args.no_plot:
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Original vs Modified Data
        plt.subplot(2, 2, 1)
        plt.plot(data, 'b-', label='Original Data', alpha=0.7, linewidth=1)
        plt.plot(modified_data, 'r-', label='Modified Data', alpha=0.7, linewidth=1)
        plt.title('Original vs Modified Data')
        plt.xlabel('Data Point Index')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Random Deviations
        plt.subplot(2, 2, 2)
        plt.plot(random_deviations, 'g-', alpha=0.7, linewidth=1)
        plt.axhline(y=3*deviation_std, color='r', linestyle='--', 
                   label=f'+3σ = {3*deviation_std:.4f}')
        plt.axhline(y=-3*deviation_std, color='r', linestyle='--', 
                   label=f'-3σ = {-3*deviation_std:.4f}')
        plt.axhline(y=deviation_std, color='orange', linestyle=':', 
                   label=f'+1σ = {deviation_std:.4f}')
        plt.axhline(y=-deviation_std, color='orange', linestyle=':', 
                   label=f'-1σ = {-deviation_std:.4f}')
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.title(f'Random Deviations Applied ({args.deviation}σ)')
        plt.xlabel('Data Point Index')
        plt.ylabel('Deviation Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Histogram of Original Data
        plt.subplot(2, 2, 3)
        plt.hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')
        plt.title('Distribution of Original Data')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Histogram of Modified Data
        plt.subplot(2, 2, 4)
        plt.hist(modified_data, bins=20, alpha=0.7, color='red', edgecolor='black')
        plt.title('Distribution of Modified Data')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.suptitle(f'Data Analysis: {args.input_file} ({args.deviation}σ deviation)', 
                    y=1.02, fontsize=14)
        plt.show()
    
    print(f"\n=== Process Complete ===")
    print(f"Input file: {args.input_file}")
    print(f"Output file: {output_filename}")
    print(f"Output format: Single column (.txt, CSV-compatible)")
    print(f"Deviation applied: {args.deviation}σ (std = {deviation_std:.6f})")
    print(f"Total values written: {len(modified_data)}")

if __name__ == "__main__":
    main()