import streamlit as st
import os
import pandas as pd
from main1 import CsvAnalyzer
from pdf import generate_pdf
import base64
import graph

st.title("CSV ANALYZER")

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to", ["Home", "Chat","Visualize", "Report"])

# Function to save uploaded files to a folder
def save_uploaded_file(uploadedfile):
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")
    with open(os.path.join("uploaded_files", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

# If uploaded_file is not in session state, initialize it as None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Function to generate pie chart UI
def pie_chart_ui(df):

    columns = list(df.columns)
    label = st.selectbox("Select a label", options=columns)
    columns.remove(label)
    value = st.selectbox("Select a value", options= columns)

    return (value, label)


# Function to generate common UI for bar chart and line graph
def common_ui(df):
    columns = list(df.columns)
    x_axis= st.selectbox("select column for x axis", options=columns)
    columns.remove(x_axis)
    y_values = st.multiselect("select column for y axis", options=columns)

    x_label= st.text_input("sepicify label for x-axis",)
    y_label= st.text_input("sepicify label for y-axis",)

    return (x_axis, y_values, x_label, y_label)


# Different sections of the Streamlit app
if selection == "Home":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        st.session_state.uploaded_file = uploaded_file
        df = pd.read_csv(uploaded_file)
        st.write(df)

elif selection == "Chat":
    # Chat section to interact with the uploaded CSV file using a language model
    if st.session_state.uploaded_file is not None:
        input_text = st.text_input("Enter your query here")
        button =st.button('submit')
        
        if input_text and button:

            
            file = os.path.join("uploaded_files", st.session_state.uploaded_file.name)
            model = CsvAnalyzer()
            response = model.csv_model(file,input_text)
            # st.write(input_text)
            html_code = f"""
            <div style="background-color: gray; color: white; padding: 10px; border-radius: 5px;">
                {input_text}
            </div>
            </br>
            """
            answer_html = f"""
            <div style="background-color: white; color: black; padding: 10px; border-radius: 5px; border: 1px solid #ccc; margin-bottom: 10px;">
                {response}
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)
            st.markdown(answer_html,unsafe_allow_html=True)
            
    else:
        st.write("Please upload a CSV file first in the Home section.")


elif selection=='Visualize':
     # Visualization section to generate plots from the uploaded CSV file
    file= os.path.join("uploaded_files", st.session_state.uploaded_file.name)
    dataframe= pd.read_csv(file)

    plot_type= st.radio(
        "select a plot type:",
        ("Bar Graph", "Line Graph","Pie Chart"),
        horizontal=True
    )

    if plot_type=='Pie Chart':
        value, label = pie_chart_ui(dataframe)
        button = st.button('Next')
        
        if button:
            image = graph.pie_chart(dataframe, value, label)
            image= open(image,'rb').read()

            st.image(image, caption=plot_type, use_column_width=True)
            st.download_button(
                label='Download Graph',
                data=image,
                file_name=f'{plot_type}.jpeg',
                mime='image/jpeg'
            )
        
    else:
        x_column, y_columns, x_label, y_label = common_ui(dataframe)

        if plot_type=='Bar Graph':
            image = graph.bar_graph(dataframe, x_column, y_columns, x_label, y_label)
        else:
            image = graph.line_grapg(dataframe,x_column, y_columns, x_label, y_label)

        image = open(image, 'rb').read()
        button= st.button("Next")
        if button:
            st.image(image, caption=plot_type, use_column_width=True)
            st.download_button(
                label="Download Image",
                data=image,
                file_name=f'{plot_type}.jpeg',
                mime='image/jpeg'
            )
   

elif selection == 'Report':
    # Generate a report based on user-selected plots
    plot_type= st.radio(
        "select a plot type:",
        (None,"Bar Graph", "Line Graph","Pie Chart"),
        horizontal=True
        )
    file = os.path.join("uploaded_files", st.session_state.uploaded_file.name)
    dataframe= pd.read_csv(file)

    plot_dict = {}
    if plot_type:
        if plot_type=='Pie Chart':
            value, label = pie_chart_ui(dataframe)
            plot_dict['plot_type']=plot_type
            plot_dict['value']=value
            plot_dict['label']=label

        else:
            x_column, y_columns, x_label, y_label = common_ui(dataframe)
            plot_dict['plot_type']=plot_type
            plot_dict['x_column']=x_column
            plot_dict['y_columns']=y_columns
            plot_dict['x_label']=x_label
            plot_dict['y_label']=y_label

    if st.button('Generate'):

        report = generate_pdf(file, plot_dict)

        with open (report,'rb') as pdf:
            pdf_report = pdf.read()

        base64_pdf = base64.b64encode(pdf_report).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button(
            label="Download PDF",
            data=pdf_report,
            file_name=os.path.basename(report),
            mime="application/pdf"
        )
