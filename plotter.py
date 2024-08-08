import plotly.graph_objects as go
import numpy as np
import sympy as sp

class Plotter:
    def __init__(self):
        self.current_plot = None

    def parse_function(self, func_str):
        x, y, t = sp.symbols('x y t')
        func = sp.sympify(func_str)
        return func

    def evaluate_function(self, func, x_vals, y_vals=None):
        x, y, t = sp.symbols('x y t')
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

    def plot_parametric(self, x_func_str, y_func_str, t_range, num_points):
        x_func = self.parse_function(x_func_str)
        y_func = self.parse_function(y_func_str)
        t_vals = np.linspace(t_range[0], t_range[1], num_points)
        x_vals = self.evaluate_function(x_func, t_vals)
        y_vals = self.evaluate_function(y_func, t_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'{x_func_str}, {y_func_str}'))
        fig.update_layout(title=f'Parametric Plot', xaxis_title='x(t)', yaxis_title='y(t)')
        fig.show()
        self.current_plot = fig

    def plot_polar(self, func_str, theta_range, num_points):
        func = self.parse_function(func_str)
        theta_vals = np.linspace(theta_range[0], theta_range[1], num_points)
        r_vals = self.evaluate_function(func, theta_vals)

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=r_vals, theta=theta_vals * 180/np.pi, mode='lines', name=func_str))
        fig.update_layout(title=f'Polar Plot of {func_str}', polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(visible=True)
        ))
        fig.show()
        self.current_plot = fig

    def plot_multiplot(self, func_str_list, x_range, num_points, rows, cols):
        fig = sp.make_subplots(rows=rows, cols=cols, subplot_titles=func_str_list)

        for i, func_str in enumerate(func_str_list):
            func = self.parse_function(func_str)
            x_vals = np.linspace(x_range[0], x_range[1], num_points)
            y_vals = self.evaluate_function(func, x_vals)
            row = i // cols + 1
            col = i % cols + 1
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=func_str), row=row, col=col)

        fig.update_layout(title='Multiplot Layout')
        fig.show()
        self.current_plot = fig