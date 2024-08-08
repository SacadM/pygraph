import plotly.graph_objects as go
import numpy as np
import sympy as sp

class Plotter:
    def __init__(self):
        self.current_plot = None

    def parse_function(self, func_str):
        x, y = sp.symbols('x y')
        func = sp.sympify(func_str)
        return func

    def evaluate_function(self, func, x_vals, y_vals=None):
        x, y = sp.symbols('x y')
        if y_vals is not None:
            f = sp.lambdify((x, y), func, 'numpy')
            return f(x_vals, y_vals)
        else:
            f = sp.lambdify(x, func, 'numpy')
            return f(x_vals)

    def plot_2d(self, func_str, x_range, num_points):
        func = self.parse_function(func_str)
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.evaluate_function(func, x_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=func_str))
        fig.update_layout(title=f'Plot of {func_str}', xaxis_title='x', yaxis_title='f(x)')
        fig.show()
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
            zaxis_title='f(x, y)'))
        fig.show()
        self.current_plot = fig