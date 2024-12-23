
# 📊 AI-Driven Dynamic Data Visualizer 📊

This project is a **web-based dynamic data visualization tool** powered by **Dash** and **Hugging Face API**. It enables users to upload datasets (CSV), analyze them, and generate interactive visualizations with intelligent insights using AI.

---

## Features

- **File Upload**: Supports CSV uploads.
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
```

### Step 2: Set Up the Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

### Step 3: Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Set Environment Variables
Place your huggingface API key in the placeholder in app.py on line 21:
```
API_KEY="your_hugging_face_api_key"
```

### Step 5: Run the Application
Run the Dash app on a local server:
```bash
python app.py
```
The app will be available at [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## Usage

1. **Upload a Dataset**: Drag and drop a CSV or Excel file.
2. **Enter a Query**: Use natural language to ask questions about the dataset.
3. **Select Graph Type**: Choose a graph type from the dropdown.
4. **Generate Visualization**: Click the button to generate interactive visualizations.

---

## Project Structure

```plaintext
.
├── app.py                # Main application file
├── requirements.txt      # List of required dependencies
├── assets/
│   └── style.css         # Custom CSS for styling
├── media/                # Folder for uploaded files (auto-created)
├── .env                  # Environment variables (not included in repo)
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

---

## Technologies Used

- **Dash**: For building the web application.
- **Plotly**: For interactive visualizations.
- **Pandas**: For data manipulation and analysis.
- **Hugging Face API**: For AI-driven insights.
- **Python**: Backend programming language.

---

## Contributions

Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit pull requests.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- [Dash](https://dash.plotly.com/)
- [Plotly](https://plotly.com/)
- [Hugging Face](https://huggingface.co/)

---

### Screenshots
![Screenshot (193)](https://github.com/user-attachments/assets/7c707d0b-6e01-4ebf-862c-1b3b8f601610)

![Screenshot (189)](https://github.com/user-attachments/assets/5aeaa617-1bc5-407f-9176-3d9bd369ba0a)

![Screenshot (192)](https://github.com/user-attachments/assets/5f3fbe49-a6fe-4e6d-8a3b-c83dd282e307)

![Screenshot (190)](https://github.com/user-attachments/assets/def1f3bf-4180-4031-83be-a348661b82ae)



