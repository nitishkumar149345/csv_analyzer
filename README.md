# CSV File Analyzer

CSV File Analyzer is a powerful tool that allows users to interactively analyze CSV files. With this tool, users can chat with the CSV file, generate insightful graphs, and create comprehensive PDF reports.

## Features

- **Chat with CSV File**: Interactively query and explore your CSV data through a chat interface.
- **Generate Graphs**: Create various types of graphs to visualize data trends and patterns.
- **PDF Report Generation**: Compile analysis results into a professional PDF report.

## Installation

To get started with CSV File Analyzer, follow these steps:

1. **Clone the repository:**
   git clone https://github.com/nitishkumar149345/csv_analyzer.git

2. **Set up the environment:**
   python -m venv env
   source env/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt
   
5. **Set up environment variables:**
   create a `.env` file in the project root directory and add your openai api key as environment variable.  
   
## Usage
1. **Run the streamlit application:**
   streamlit run ui.py

2. **Upload a CSV file:**
   use the interface to upload your CSV file

3. **Chat with the CSV file:**
   interact with the CSV file through the chat interface to perform queries and get immediate responses.

4. **Generate Graphs:**
   use the provided options to create various types of graphs based on your csv data.

5. **Generate PDF Report:**
   Generate a pdf report with summary, statistics and graph along with their explanation.

## Chat with CSV
Example queries you can use:
* "Show me the summary statistics of the data."
* "What are the top 10 entries in the dataset?"
* "Find the average value of column X."

## Generate Graphs
Supported graph types include:
* Bar Graphs
* Line Charts
* Pie Charts

## Generate PDF Report
The PDF report will include:

* Summary of the CSV file
* Tabular reprasentation of statistical data, along with its explanation.
* Graph you selected, along with its explanation. 

## Acknowledgments
Thanks to OpenAI for the API support.
