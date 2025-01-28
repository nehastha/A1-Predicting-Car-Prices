import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pickle
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div(
    id='form-container',
    children=[
        html.H1('Car Price Prediction', style={
            'text-align': 'center',
            'color': '#000000',
            'margin-bottom': '30px'}),
        html.P('Instructions: Please enter the values for Year, Engine, Km_driven and Mileage in the respective fields. '
               'The prediction model will use these inputs to estimate the car price. To see the predicted value proceed by clicking the "Submit" button.'
               ' For the fields that are empty default values will be used to predict the car price',
               style={
                   'font-size': '14px',
                   'color': '#555',
                   'margin-bottom': '30px',
                   'line-height': '1.5'
               }),
        html.Label('Enter the values in the relative field', style={'font-weight': 'bold', 'font-size': '16px'}),
        html.Br(),
        html.Br(),
        html.Label('Engine:', style={'font-weight': 'bold', 'font-size': '14px'}),
        html.Br(),
        dcc.Input(id='engine', type='number', placeholder='Input the value of Engine', style={
            'width': '100%',
            'padding': '8px',
            'margin-top': '5px',
            'margin-bottom': '20px',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'box-sizing': 'border-box',
            'font-size': '14px'
        }),
        html.Br(),
        html.Label('Mileage:', style={'font-weight': 'bold', 'font-size': '14px'}),
        html.Br(),
        dcc.Input(id='mileage', type='number', placeholder='Input the value of Mileage', style={
            'width': '100%',
            'padding': '8px',
            'margin-top': '5px',
            'margin-bottom': '20px',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'box-sizing': 'border-box',
            'font-size': '14px'
        }),
        html.Br(),
        html.Label('Km_driven:', style={'font-weight': 'bold', 'font-size': '14px'}),
        html.Br(),
        dcc.Input(id='km_driven', type='number', placeholder='Input the value of Km_driven', style={
            'width': '100%',
            'padding': '8px',
            'margin-top': '5px',
            'margin-bottom': '20px',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'box-sizing': 'border-box',
            'font-size': '14px'
        }),
        html.Br(),
        html.Label('Year', style={'font-weight': 'bold', 'font-size': '14px'}),
        html.Br(),
        dcc.Input(id='year', type='number', placeholder='Input Year', style={
            'width': '100%',
            'padding': '8px',
            'margin-top': '5px',
            'margin-bottom': '20px',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'box-sizing': 'border-box',
            'font-size': '14px'
        }),
        html.Br(),
        html.Br(),
        html.Button('Submit', id='submit', n_clicks=0, style={
            'background-color': '#87B992',
            'color': 'white',
            'padding': '10px 15px',
            'border': 'none',
            'border-radius': '100px',
            'cursor': 'pointer',
            'font-size': '16px',
            'display': 'block',
            'margin': '0px 10px 0px 0px'
        }),
        html.Div(id='output-predict', style={
            'font-size': '16px',
            'margin-top': '20px',
            'color': '#333'
        })
    ],
    style={
        'margin': 'auto',
        'width': '50%',
        'padding': '20px',
        'border': '2px solid #f0f0f0',
        'border-radius': '10px',
        'background-color': '#f9f9f9',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }
)

def prediction(year: float, engine: float, km_driven: float , mileage: float,) -> float:
    try:
        model = pickle.load(open('model/car.model', 'rb'))
        data = np.array([[year, engine, km_driven, mileage]])
        prediction = np.exp(model.predict(data))
        return prediction[0]  # Accessing the first element
    except Exception as e:
        raise ValueError(f"Prediction error: {str(e)}")

def getDefaultValue():
    try:
        df = pd.read_csv("./data/Cars.csv")
        df['owner'] = df['owner'].map({
            "First Owner": 1,
            "Second Owner": 2,
            "Third Owner": 3,
            "Fourth & Above Owner": 4,
            "Test Drive Car": 5
        })
        df = df[(df['fuel'] != 'CNG') & (df['fuel'] != 'LPG')]
        df['mileage'] = df['mileage'].str.split().str[0].astype(float)
        df['engine'] = df['engine'].str.split().str[0].str.replace('CC', '').astype(float)
        df['max_power'] = df['max_power'].str.replace('bhp', '').str.extract('(\d+\.?\d*)').astype(float)
        df['name'] = df['name'].str.split().str[0]
        df = df.drop(columns=['torque'])
        df = df[df['owner'] != 5]

        median_engine = df['engine'].median()
        median_year = df['year'].median()
        mean_mileage = df['mileage'].mean()
        median_km_driven = df['km_driven'].median()
        return median_year, median_engine, mean_mileage, median_km_driven
    except Exception as e:
        raise ValueError(f"Error in processing data: {str(e)}")

@app.callback(
    Output('output-predict', 'children'),
    [Input('submit', 'n_clicks')],
    [State('engine', 'value'),
     State('mileage', 'value'),
     State('km_driven', 'value'),
     State('year', 'value')]
)

def update_output(click, entered_engine, entered_mileage,entered_km_driven, entered_year):
    try:
        if click > 0:
            default_year, default_engine, default_mileage , default_km_driven = getDefaultValue()
            
            entered_year = entered_year if entered_year else default_year
            entered_engine = entered_engine if entered_engine else default_engine
            entered_mileage = entered_mileage if entered_mileage else default_mileage
            entered_km_driven = entered_km_driven if entered_km_driven else default_km_driven
            
            prediction_val = prediction(float(entered_engine), float(entered_mileage),float(entered_km_driven), float(entered_year))
            return f" Predicted Price: {prediction_val:.2f}"
    except Exception as e:
        return f"Error in prediction: {str(e)}"
    
    return 'Click "Submit" to view the predicted price.'

if __name__ == '__main__':
    app.run(debug=True, port=8050)
