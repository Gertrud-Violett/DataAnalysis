# Manufacturing Data Analysis Tool

This Python code provides a comprehensive set of tools for analyzing manufacturing data using statistical process control (SPC) techniques and advanced statistical methods. It is designed for engineers with entry level statistical analysis knowledge. The input and output parameters are similar to Minitab software. 

## Features

- Data loading and preprocessing
- Process capability analysis (Cp, Cpk, Cpu, Cpl, Pp, Ppk, Cpm, Cpkm)
- Tolerance interval calculation
- Distribution fitting (normal and Weibull)
- Multivariate analysis (Principal Component Analysis)
- Statistical tests (Mann-Whitney U test)
- Visualization (multi-vari charts, box plots, Pareto charts, control chart dashboards)

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn
- spc

Install the required libraries using pip:

```python
pip install pandas numpy matplotlib seaborn scipy scikit-learn controlchart
```

## Usage 
1.  Prepare your manufacturing data in a CSV file format. 
2. Import the necessary classes and functions: Refer to sample code for usage

```python
from process_control import ProcessControl, MultivariateAnalysis, StatisticalTests, Visualization
```

3. Load the data from the CSV file:

```python
pc = read_csv_data('sample_manufacturing_data.csv', 'Temperature')
```
4. Set specification limits and perform capability analysis:

```python
pc.set_specification_limits(usl=26.0, lsl=24.0, target=25.0)
pc.set_active_column('Temperature')
capability_results = pc.calculate_capability()
additional_indices = pc.calculate_capability_indices()
```

5. Calculate tolerance intervals:

```python
lower, upper = pc.tolerance_interval(alpha=0.05, p=0.95, distribution='normal')
```

6. Fit and compare distributions:

```python
normal_fit = pc.fit_distribution('normal')
weibull_fit = pc.fit_distribution('weibull')
```

7. Perform multivariate analysis:

```python
mv_analysis = MultivariateAnalysis(pc.data)
principal_components, explained_variance = mv_analysis.principal_component_analysis(n_components=2)
```

8. Perform statistical tests:

```python
stats_tests = StatisticalTests(pc.data)
u_stat, p_value = stats_tests.mann_whitney_u_test(group1, group2)
```

9. Create visualizations:

```python
pc.plot_distribution(normal_fit)
pc.plot_distribution(weibull_fit)
pc.plot_capability()
```

viz = Visualization(pc.data)
viz.multi_vari_chart('Group', 'Temperature')
viz.box_plot('Temperature')
viz.pareto_chart('Defect_Type', 'Count')
viz.control_chart_dashboard(pc.data, chart_type='xbar_r')