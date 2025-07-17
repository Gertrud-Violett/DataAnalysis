# Manufacturing Data Analysis Tool

This Python code provides a comprehensive set of tools for analyzing manufacturing data using statistical process control (SPC) techniques and advanced statistical methods. It is designed for engineers with entry level statistical analysis knowledge. The input and output parameters are similar to Minitab software. 

## Features

- Data loading and preprocessing
- Process capability analysis (Cp, Cpk, Cpu, Cpl, Pp, Ppk, Cpm, Cpkm)
- Tolerance interval calculation
- Distribution fitting (normal and Weibull)
- Correlation plotting
- Multivariate analysis (Principal Component Analysis)
- Statistical tests (Mann-Whitney U test)
- Visualization (multi-vari charts, box plots)
- Normal Probability Plotting

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn

Install the required libraries using pip:

```python
pip install pandas numpy matplotlib seaborn scipy scikit-learn controlchart
```

## Usage (Sample)
1.  Prepare your manufacturing data in a CSV file format. Refer to sample csv file for format.

2. Load the data from the CSV file:

```python
pc = read_csv_data('sample_manufacturing_data.csv', 'Temperature')
```
3. Set specification limits

```python
pc.set_specification_limits(usl=26.0, lsl=24.0, target=25.0)
```

4.  Perform capability analysis and show tolerance intervals:
```python
pc.set_active_column('Temperature')
capability_results = pc.calculate_capability()
print("\nProcess Capability Analysis Results for Temperature:")
print(f"Cp: {capability_results['Cp']:.3f}")
print(f"Cpk: {capability_results['Cpk']:.3f}")
print(f"Cpm: {capability_results['Cpm']:.3f}")
print(f"Cpkm: {capability_results['Cpkm']:.3f}")
lower, upper = pc.tolerance_interval(alpha=0.05, p=0.95, distribution='normal')
```


5. Fit and Compare distributions:
```python
normal_fit = pc.fit_distribution('normal')
weibull_fit = pc.fit_distribution('weibull')
print("\nDistribution Fit Results for Temperature:")
print("\nNormal Distribution:")
params = normal_fit['parameters'] #normal, weibull, lognormal can be selected
print(f"Parameters: ({params[0]:.4f}, {params[1]:.4f})")
print(f"KS-statistic: {normal_fit['ks_stat']:.3f}")
print(f"KS-p-value: {normal_fit['ks_p']:.3f}")
pc.plot_distribution(normal_fit) #normal, weibull, lognormal can be selected
pc.plot_capability()
```


6. Perform multivariate analysis:

```python
mv_analysis = MultivariateAnalysis(pc.data)
principal_components, explained_variance = mv_analysis.principal_component_analysis(n_components=2)
print("\nPrincipal Component Analysis Results:")
print(f"Explained Variance Ratio: {explained_variance}")
```

8. Perform statistical tests:

```python
stats_tests = StatisticalTests(pc.data)
group1 = pc.data['Temperature'][:50]
group2 = pc.data['Temperature'][50:]
u_stat, p_value = stats_tests.mann_whitney_u_test(group1, group2)
print("\nMann-Whitney U Test Results:")
print(f"U-statistic: {u_stat}")
print(f"p-value: {p_value:.3f}")
```

8. Create Additional visualizations:

```python
viz = Visualization(pc.data)
viz.multi_vari_chart('Test_Bench', 'Flow_Rate')
viz.box_plot('Flow_Rate')
```


9. Perform Correlation Analysis

```python
corr, p_value = pc.calculate_correlation('Temperature', 'Flow_Rate')
print(f"\nCorrelation between Temperature and Pressure:")  
print(f"Correlation coefficient: {corr:.4f}")
print(f"p-value: {p_value:.4e}")
pc.plot_correlation('Temperature', 'Flow_Rate')
```

10. Analyze Correlation between different columns
```python
columns_of_interest = ['Temperature', 'Pressure', 'Flow_Rate']
available_columns = [col for col in columns_of_interest if col in pc.data.columns]
print(f"\nAnalyzing correlations between: {available_columns}")
pc.plot_correlation_matrix(available_columns)
```

11. Create normal probability plots
```python
pc.plot_normal_probability('Temperature')
pc.plot_normal_probability('Pressure') 
pc.plot_normal_probability('Flow_Rate')
```