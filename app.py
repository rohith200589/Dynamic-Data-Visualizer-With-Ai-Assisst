
import os
import base64
import io
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State
import dash
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

import requests

# Hugging Face API endpoint and key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = ""  # Replace with your actual key
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def query_huggingface_api(prompt):
    
    
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        return response.json()[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        return f"Error querying Hugging Face API: {str(e)}"


#

# Default dataset
default_data = {
    "Player": ["Player A", "Player B", "Player C", "Player D", "Player E"],
    "Runs": [450, 400, 380, 350, 340],
    "Matches": [10, 10, 10, 10, 10],
    "Strike Rate": [140, 135, 130, 125, 120]
}
default_df = pd.DataFrame(default_data)

# Helper function to parse uploaded CSV or Excel file
def parse_uploaded_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, "Unsupported file type. Please upload a CSV or Excel file."
    except Exception as e:
        return None, f"Error processing file: {str(e)}"
    return df, None

# Function to analyze dataset
def analyze_dataset(df):
    column_types = {"numeric": [], "categorical": [], "datetime": []}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            column_types["numeric"].append(column)
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            column_types["datetime"].append(column)
        else:
            column_types["categorical"].append(column)
    return column_types

# Function to process natural language queries
# Function to process natural language queries and perform statistical analysis
def process_query(query, df):
    """
    Processes a user query and returns the response using LLM-generated insights.
    """
    query = query.lower()
    response_message = ""
    insights = []
    
    # Prepare a summary of the dataset for LLM
    dataset_summary = df.describe().to_string()

    # Formulate the prompt for the LLM
    prompt = f"Here is a dataset:\n{dataset_summary}\nUser query: {query}\n\n Provide a detailed interpretation and insights."

    try:
        # Query the LLM (Hugging Face API)
        llm_response = query_huggingface_api(prompt)
        
        if llm_response:
            response_message = f"LLM Analysis: {llm_response}"
            
        else:
            response_message = "The query couldn't be processed by the AI."
            insights.append("No insights generated.")

    except Exception as e:
        response_message = f"Error processing query: {str(e)}"
        insights.append(f"Error: {str(e)}")

    return df, response_message, " ".join(insights)


# Function to auto-select axes based on query
def auto_select_axes(df, query, column_types):
    if "trend" in query.lower() or "time" in query.lower():
        x_col = column_types["datetime"][0] if column_types["datetime"] else column_types["categorical"][0]
        y_col = column_types["numeric"][0] if column_types["numeric"] else None
    elif "compare" in query.lower() or "categories" in query.lower():
        x_col = column_types["categorical"][0] if column_types["categorical"] else None
        y_col = column_types["numeric"][0] if column_types["numeric"] else None
    else:
        x_col = column_types["categorical"][0] if column_types["categorical"] else None
        y_col = column_types["numeric"][0] if column_types["numeric"] else None
    return x_col, y_col

# App layout
app.layout = html.Div([
    # Page Title
    html.H1(
        "📊AI-Driven Dynamic Data Visualizer📊",
        style={
            'textAlign': 'center',
            'color': '#000',
            'marginBottom': '40px',
            'fontSize': '2.5em',
            'fontWeight': 'bold',
            'fontFamily': 'Arial, sans-serif'
        }
    ),

    # Main Container
    html.Div([
        # Left Section (Inputs)
        html.Div([
            # File Upload Section
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Span('Drag and Drop or ', style={'fontWeight': 'bold'}),
                    html.A('Select a CSV or Excel File', style={'color': '#1f77b4', 'textDecoration': 'underline'})
                ]),
                style={
                    'width': '100%',
                    'height': '80px',
                    'lineHeight': '80px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '20px 0',
                    'backgroundColor': 'rgba(255, 255, 255, 0.8)',
                    'color': '#555',
                    'fontSize': '1.2em',
                    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
                    'transition': 'background-color 0.3s ease'
                },
                accept=".csv,.xlsx",
                multiple=False
            ),
            html.Div(
                id="upload-feedback",
                style={
                    'color': '#28a745',
                    'margin': '10px 0',
                    'fontWeight': 'bold',
                    'fontSize': '1.1em',
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif'
                }
            ),

            # User Query Input
            dcc.Input(
                id="user-input",
                type="text",
                placeholder="Enter your query (e.g., 'Give top 5 run scorers')",
                style={
                    'width': '100%',
                    'padding': '11px',
                    'margin': '10px auto',
                    'border': '2px solid #ddd',
                    'borderRadius': '8px',
                    'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)',
                    'fontSize': '1.2em',
                    'color': '#333',
                    'backgroundColor': '#ffffff'
                }
            ),

            # Graph Type Dropdown
            dcc.Dropdown(
                id="graph-type-dropdown",
                options=[
                    {'label': 'Line Graph', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Pie Chart', 'value': 'pie'}
                ],
                placeholder="Select graph type...",
                style={
                    'width': '100%',
                    'margin': '10px auto',
                    'padding': '10px',
                    'border': '2px solid #ddd',
                    'borderRadius': '8px',
                    'fontSize': '1.2em',
                    'backgroundColor': '#ffffff',
                    'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)'
                }
            ),

            # Axes Selection
            html.Div([
                html.Div([
                    html.Label("X-axis:", style={'marginRight': '10px', 'fontWeight': 'bold', 'fontSize': '1.2em'}),
                    dcc.Dropdown(
                        id="x-axis-dropdown",
                        style={
                            'width': '100%',
                            'padding': '10px',
                            'border': '2px solid #ddd',
                            'borderRadius': '8px',
                            'fontSize': '1.1em',
                            'backgroundColor': '#ffffff',
                            'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)'
                        }
                    )
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Label("Y-axis:", style={'marginRight': '10px', 'fontWeight': 'bold', 'fontSize': '1.2em'}),
                    dcc.Dropdown(
                        id="y-axis-dropdown",
                        style={
                            'width': '100%',
                            'padding': '10px',
                            'border': '2px solid #ddd',
                            'borderRadius': '8px',
                            'fontSize': '1.1em',
                            'backgroundColor': '#ffffff',
                            'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.1)'
                        }
                    )
                ])
            ]),

            # Generate Visualization Button
            html.Button(
                "Generate Visualization",
                id="generate-button",
                style={
                    'padding': '15px 30px',
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'fontSize': '1.2em',
                    'fontWeight': 'bold',
                    'fontFamily': 'Arial, sans-serif',
                    'cursor': 'pointer',
                    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
                    'transition': 'background-color 0.3s ease',
                    'display': 'block',
                    'margin': '20px auto'
                }
            )
        ], style={
            'width': '45%',
            'padding': '34px',
            'backgroundColor': 'rgba(255, 255, 255, 0.9)',
            'borderRadius': '10px',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
        }),

        # Right Section (Outputs)
        html.Div([
            dcc.Loading(
                id="loading-spinner",
                type="circle",
                children=html.Div([

                    dcc.Graph(id="graph-output", style={
                        'margin': '20px auto',
                        'padding': '20px',
                        'border': '2px solid #ddd',
                        'borderRadius': '10px',
                        'backgroundColor':'#f9f9f9',
                        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
                    }),
                    html.Div(id="response-output-query",
                        style={
                        'margin': '20px 10px',
                        'padding': '15px',
                        'color': '#333',
                        'fontSize': '1.2em',
                        'lineHeight': '1.6em',
                        'textAlign': 'left',
                        'backgroundColor': '#f9f9f9',
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'fontFamily': 'Arial, sans-serif',
                        'whiteSpace': 'pre-wrap',  # Ensures newlines are respected
                        'overflowY': 'auto',      # Adds a scroll bar if content overflows
                        'maxHeight': '300px'      # Limits height for large content
                    

                    }),
                    html.Div(id="insights-output", style={
                        'margin': '20px 10px',
                        'color': '#28a745',
                        'fontSize': '1.1em',
                        'lineHeight': '1.6em',
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'backgorundColor': '#f9f9f9'
                    })
                    
                ])
            )
        ], style={
            'width': '45%',
            'padding': '20px',
            'padding-down':'20px',
            'backgroundColor': 'rgba(255, 255, 255, 0.9)',
            'borderRadius': '10px',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
        })
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'flex-start'
    })
], style={
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px',
    'backgroundImage': 'linear-gradient(103deg, #39e21c, #74eb04)',
'backgroundSize': 'cover',  # Ensures the gradient covers the container
'backgroundAttachment': 'fixed'  # Keeps the gradient fixed during scrolling

    
})



@app.callback(
    Output("upload-feedback", "children"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename")]
)
def show_upload_feedback(contents, filename):
    if contents and filename:
        return f"File '{filename}' uploaded successfully."
    return "No file uploaded yet."

@app.callback(
    [Output("x-axis-dropdown", "options"),
     Output("y-axis-dropdown", "options"),
     Output("x-axis-dropdown", "value"),
     Output("y-axis-dropdown", "value")],
    [Input("upload-data", "contents"),
     Input("upload-data", "filename"),
     Input("user-input", "value")]
)

def update_column_dropdowns(contents, filename, query):
    if contents:
        df, error_message = parse_uploaded_file(contents, filename)
        if error_message:
            return [], [], None, None
    else:
        df = default_df

    column_types = analyze_dataset(df)
    options = [{"label": col, "value": col} for col in df.columns]
    
    if query:
        x_auto, y_auto = auto_select_axes(df, query, column_types)
    else:
        x_auto, y_auto = None, None

    return options, options, x_auto, y_auto

@app.callback(
    [Output("response-output-query", "children"),
     Output("graph-output", "figure"),
     Output("insights-output", "children")],
    [Input("generate-button", "n_clicks")],
    [State("user-input", "value"),
     State("x-axis-dropdown", "value"),
     State("y-axis-dropdown", "value"),
     State("graph-type-dropdown", "value"),
     State("upload-data", "contents"),
     State("upload-data", "filename")]
)
def generate_visualization(n_clicks, query, x_col, y_col, graph_type, contents, filename):
    if n_clicks is None:
        return "", {}, ""

    # Display the loading message initially
    loading_message = "Generating Please Wait For 2-4 Seconds"
    loading_spinner = {"color": "orange"}  # You can customize the spinner color

    if contents:
        df, error_message = parse_uploaded_file(contents, filename)
        if error_message:
            return error_message, {}, ""
    else:
        df = default_df

    try:
        df, response_message, insights = process_query(query, df)

        # Generate the graph
        if graph_type == "line":
            fig = px.line(df, x=x_col, y=y_col, title=f"Line Graph: {y_col} vs {x_col}")
        elif graph_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart: {y_col} vs {x_col}")
        elif graph_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {y_col} vs {x_col}")
        elif graph_type == "pie":
            fig = px.pie(df, names=x_col, values=y_col, title=f"Pie Chart: {y_col} distribution")
        else:
            fig = {}

        # Hide loading state and show result
        loading_message = ""  # Remove loading message once result is ready
        return response_message, fig, insights

    except Exception as e:
        return f"Error generating visualization: {str(e)}", {}, ""


if __name__ == "__main__":
    app.run_server(debug=True) 
