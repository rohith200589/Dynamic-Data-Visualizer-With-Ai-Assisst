# AI-Driven Dynamic Data Visualizer 📊

This project is a **web-based dynamic data visualization tool** powered by **Dash** and **Hugging Face API**.
It enables users to upload datasets (CSV or Excel), analyze them, and generate interactive visualizations with intelligent insights using AI.

---

## Features

- **File Upload**: Supports CSV and Excel file uploads.
- **Dynamic Analysis**: Automatically analyzes datasets and suggests axes for graphs.
- **Natural Language Query**: Processes user queries to generate AI-driven insights.
- **Interactive Visualizations**: Provides options for line graphs, bar charts, scatter plots, and pie charts.
- **Built-in Dataset**: Includes a default dataset for demonstration purposes.

---

## Setup and Installation

### Prerequisites
1. Python 3.7+
2. Virtual Environment (optional but recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Step 2: Set Up the Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
Step 3: Install Dependencies
Install the required Python packages listed in requirements.txt:

bash
Copy code
pip install -r requirements.txt
Step 4: Add API Key
The source code includes a placeholder for the Hugging Face API key. Update it in the relevant file (app.py or configuration file):

python
Copy code
API_KEY = "your_hugging_face_api_key"
Replace "your_hugging_face_api_key" with your actual Hugging Face API key.

Step 5: Run the Application
Run the Dash app on a local server:

bash
Copy code
python app.py
The app will be available at http://127.0.0.1:8050.

Usage
Upload a Dataset: Drag and drop a CSV or Excel file.
Enter a Query: Use natural language to ask questions about the dataset.
Select Graph Type: Choose a graph type from the dropdown.
Generate Visualization: Click the button to generate interactive visualizations.
Project Structure
plaintext
Copy code
.
├── app.py                # Main application file
├── requirements.txt      # List of required dependencies
├── assets/
│   └── style.css         # Custom CSS for styling
├── media/                # Folder for uploaded files (auto-created)
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
└── LICENSE               # License file
Technologies Used
Dash: For building the web application.
Plotly: For interactive visualizations.
Pandas: For data manipulation and analysis.
Hugging Face API: For AI-driven insights.
Python: Backend programming language.
Contributions
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit pull requests.

License
This project is licensed under the MIT License.

Acknowledgements
Dash
Plotly
Hugging Face
Screenshots
