import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sympy as sp
import csv

class Plotter:
    def __init__(self):
        self.current_plot = None

    def parse_function(self, func_str):
        x, y, t = sp.symbols('x y t')
        func = sp.sympify(func_str, locals={'cos': sp.cos, 'sin': sp.sin})
        return func

    def evaluate_function(self, func, x_vals, y_vals=None):
        x, y, t = sp.symbols('x y t')
        if y_vals is not None:
            f = sp.lambdify((x, y), func, modules=['numpy'])
            return f(x_vals, y_vals)
        elif 't' in str(func):
            f = sp.lambdify(t, func, modules=['numpy'])
            return np.array(f(x_vals), dtype=float)
        else:
            f = sp.lambdify(x, func, modules=['numpy'])
            return np.array(f(x_vals), dtype=float)

    def plot_2d(self, func_str, x_range, num_points):
        func = self.parse_function(func_str)
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.evaluate_function(func, x_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=func_str))
        fig.update_layout(title=f'Plot of {func_str}', xaxis_title='x', yaxis_title='f(x)', hovermode='x unified')
        self.current_plot = fig

    def plot_3d(self, func_str, x_range, y_range, num_points):
        func = self.parse_function(func_str)
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = np.linspace(y_range[0], y_range[1], num_points)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = self.evaluate_function(func, X, Y)

        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        fig.update_layout(title=f'3D Plot of {func_str}', scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='f(x, y)'), hovermode='closest')
        self.current_plot = fig

    def plot_parametric(self, x_func_str, y_func_str, t_range, num_points):
        t = sp.symbols('t')
        x_func = sp.sympify(x_func_str, locals={'cos': sp.cos, 'sin': sp.sin})
        y_func = sp.sympify(y_func_str, locals={'cos': sp.cos, 'sin': sp.sin})
        t_vals = np.linspace(t_range[0], t_range[1], num_points)
        x_vals = self.evaluate_function(x_func, t_vals)
        y_vals = self.evaluate_function(y_func, t_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'{x_func_str}, {y_func_str}'))
        fig.update_layout(title=f'Parametric Plot', xaxis_title='x(t)', yaxis_title='y(t)', hovermode='x unified')
        self.current_plot = fig

    def plot_polar(self, func_str, theta_range, num_points):
        theta = sp.symbols('theta')
        func = sp.sympify(func_str, locals={'cos': sp.cos, 'sin': sp.sin})
        theta_vals = np.linspace(theta_range[0], theta_range[1], num_points)
        r_vals = self.evaluate_function(func, theta_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=r_vals, theta=theta_vals * 180/np.pi, mode='lines', name=func_str))
        fig.update_layout(title=f'Polar Plot of {func_str}', polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(visible=True)), hovermode='closest')
        self.current_plot = fig

    def plot_multiplot(self, func_str_list, x_range, num_points, rows, cols):
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=func_str_list)

        for i, func_str in enumerate(func_str_list):
            func = self.parse_function(func_str)
            x_vals = np.linspace(x_range[0], x_range[1], num_points)
            y_vals = self.evaluate_function(func, x_vals)
            row = i // cols + 1
            col = i % cols + 1
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=func_str), row=row, col=col)

        fig.update_layout(title='Multiplot Layout', hovermode='x unified')
        self.current_plot = fig

    def plot_csv(self, csv_file, increment):
        x_vals = []
        y_vals = []
        
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                x_vals.append(i * increment)
                y_vals.append(float(row[0]))  # Assuming the CSV has one column of data points

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', name='CSV Data'))
        fig.update_layout(title='Plot of CSV Data', xaxis_title='Index', yaxis_title='Value')
        self.current_plot = fig