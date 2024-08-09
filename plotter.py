import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sympy as sp
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

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

    def plot_csv(self, csv_file, increment, forecast_steps=0):
        data = pd.read_csv(csv_file, header=None, names=['value'])
        data['time'] = range(len(data))
        
        def create_features(df, lags):
            for lag in lags:
                df[f'lag_{lag}'] = df['value'].shift(lag)
            return df.dropna()

        lags = [1, 2, 3, 4, 5]
        data_featured = create_features(data, lags)

        X = data_featured.drop(['value', 'time'], axis=1)
        y = data_featured['value']

        if len(X) <= forecast_steps:
            print(f"Warning: Not enough data points for forecasting. Reducing forecast to {len(X) - 1} points.")
            forecast_steps = len(X) - 1

        train_size = max(len(X) - forecast_steps, 1)  # at least one training point
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # train
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        def forecast(model, steps, last_known_values):
            predictions = []
            current_input = last_known_values.copy()
            
            for _ in range(steps):
                pred = model.predict(scaler.transform([current_input]))[0]
                predictions.append(pred)
                current_input = np.roll(current_input, 1)
                current_input[0] = pred
            
            return predictions
        
        last_known = X.iloc[-1].values
        y_pred = forecast(model, forecast_steps, last_known)

        fig = go.Figure()

        # plot original
        fig.add_trace(go.Scatter(x=data['time'].tolist(), y=data['value'].tolist(), mode='lines', name='Original Data'))

        # plot forecast
        forecast_start = len(data)
        forecast_x = list(range(forecast_start, forecast_start + len(y_pred)))
        fig.add_trace(go.Scatter(x=forecast_x, y=y_pred, mode='lines', name='Forecast', line=dict(dash='dash')))

        fig.update_layout(title='CSV Data with Random Forest Forecast', 
                        xaxis_title='Time', 
                        yaxis_title='Value',
                        hovermode='x unified')
        
        self.current_plot = fig