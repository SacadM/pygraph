import numpy as np
import sympy as sp
import plotly.graph_objects as go

class MathOps:
    def __init__(self):
        self.x, self.y = sp.symbols('x y')
        self.current_plot = None

    def parse_function(self, func_str):
        return sp.sympify(func_str, locals={'cos': sp.cos, 'sin': sp.sin})

    def evaluate_function(self, func, x_vals):
        f = sp.lambdify(self.x, func, modules=['numpy'])
        return np.array(f(x_vals), dtype=float)

    def plot_derivative(self, func_str, x_range, num_points, order=1):
        func = self.parse_function(func_str)
        derivative = sp.diff(func, self.x, order)
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.evaluate_function(derivative, x_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'{order} order derivative'))
        fig.update_layout(title=f'{order} Order Derivative of {func_str}', xaxis_title='x', yaxis_title=f'd^({order})f/dx^{order}')
        self.current_plot = fig

    def plot_integral(self, func_str, x_range, num_points, definite=False, a=None, b=None):
        func = self.parse_function(func_str)
        integral = sp.integrate(func, self.x)
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.evaluate_function(integral, x_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Integral'))
        fig.update_layout(title=f'Integral of {func_str}', xaxis_title='x', yaxis_title=f'∫f dx')
        self.current_plot = fig

    def plot_taylor_series(self, func_str, x_range, num_points, n=5):
        func = self.parse_function(func_str)
        taylor_series = sp.series(func, self.x, 0, n+1).removeO()
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.evaluate_function(taylor_series, x_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'Taylor Series (n={n})'))
        fig.update_layout(title=f'Taylor Series of {func_str}', xaxis_title='x', yaxis_title=f'Taylor Series Approximation')
        self.current_plot = fig