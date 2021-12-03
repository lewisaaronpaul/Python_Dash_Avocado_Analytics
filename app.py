# Favicon: https://twemoji.twitter.com/
# Import the libraries
from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

# Read the data
data =pd.read_csv("avocado.csv")
#data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format = "%Y-%m-%d")
data.sort_values("Date", inplace = True)

# Link to the CSS stylesheet
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# Initialize the application
app = Dash(__name__, external_stylesheets=external_stylesheets)
# Add this for deployment to Heroku
server = app.server

app.title = "Avocado Analytics: Understand Your Avocados!"

# Define the layout of the application
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(
                    children="🥑",
                    className="header-emoji"),
        
                html.H1(
                    children="Avacado Analytics",
                    className="header-title",
                ),
                html.P(
                    children="Analyze the behavior of avocado prices "
                             "and the number of avocados sold in the US "
                             "between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # The dropdown menu
        html.Div(
            children=[
                html.Div(
                    children=[
                        # Label
                        html.Div(
                            children="Region", 
                            className="menu-title"
                        ),
                        # End label
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Houston",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        # Label for Avocado Type
                        html.Div(
                            children="Type", 
                            className="menu-title"
                        ),
                        # End label for Avocado Type
                        # Dropdown for Avocado Type
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, 
                                 "value": avocado_type}
                                for avocado_type in np.sort(data.type.unique())
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        # Label for Date Range
                        html.Div(
                            children="Date Range", 
                            className="menu-title"
                        ),
                        # End label for Date Range
                        # Dropdown for Date Range
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        # End dropdown menu
        # Graph component
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# Create Callback function for Interactivity

@app.callback(
    # Callback Output from the function
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    # Callback Input for the function
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", 
                      "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", 
                      "x": 0.05, 
                      "xanchor": "left"
                      },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure



if __name__ == '__main__':
    app.run_server(debug=True)
