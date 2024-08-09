import plotly.graph_objects as go
import sympy as sp
import numpy as np

class Annotations:
    def add_annotations(self, func_str, fig, x_range, num_points, annotate_on_condition=None):
        x = sp.symbols('x')
        func = sp.sympify(func_str, locals={'cos': sp.cos, 'sin': sp.sin})

        # Generate x and y values
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = np.array([func.subs(x, val).evalf() for val in x_vals], dtype=float)

        # Check the condition
        if annotate_on_condition:
            condition_met = False
            segment_start = None

            for i, (x_val, y_val) in enumerate(zip(x_vals, y_vals)):
                if annotate_on_condition(x_val, y_val):
                    if not condition_met:
                        # Annotate the first point that meets the condition
                        fig.add_annotation(x=x_val, y=y_val,
                                           text=f'({x_val:.2f}, {y_val:.2f})',
                                           showarrow=True, arrowhead=2)
                        segment_start = (x_val, y_val)
                        condition_met = True
                    else:
                        # Color the curve where the condition is met
                        if i < len(x_vals) - 1:
                            fig.add_trace(go.Scatter(
                                x=[segment_start[0], x_val],
                                y=[segment_start[1], y_val],
                                mode='lines',
                                line=dict(color='red', width=3),
                                hoverinfo='skip',  # Suppress hover information
                                showlegend=False
                            ))
                            segment_start = (x_val, y_val)
                else:
                    condition_met = False
                    segment_start = None