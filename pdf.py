from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from main1 import CsvAnalyzer
import pandas as pd
import graph
import os


# Function to compute statistics for given columns in a DataFrame
def compute_statistics(columns,df):
    """
    Compute statistics for given columns in a DataFrame.

    Parameters:
        columns (list of str): List of column names.
        df (DataFrame): Input DataFrame.

    Returns:
        list of lists: Statistics table.
    """

    count = ['count']
    mean = ['mean']
    median = ['median']
    std = ['std']
    min = ['min']
    max = ['max']
    range = ['range']
    quartile_25_percent = ['25%']
    quartile_50_percent = ['50%']
    quartile_75_percent = ['75%']

    filtered_columns = ['']
    allowed_dtypes = ['int32', 'int64', 'float32', 'float64']

    for col in columns:
        if df[col].dtype in allowed_dtypes:
            filtered_columns.append(col)
            count.append(df[col].count())
            mean.append(round(df[col].mean(), 2))
            median.append(round(df[col].median(), 2))
            std.append(round(df[col].std(), 2))
            min.append(round(df[col].min(), 2))
            max.append(round(df[col].max(), 2))
            range.append(round(df[col].max() - df[col].min(), 2))
            quartile_25_percent.append(round(df[col].quantile(0.25), 2))
            quartile_50_percent.append(round(df[col].quantile(0.50), 2))
            quartile_75_percent.append(round(df[col].quantile(0.75), 2))
    
    table = [filtered_columns, count, mean, median, std, min, max, range, quartile_25_percent, quartile_50_percent, quartile_75_percent]
    
    count = ['count']
    mean = ['mean']
    median = ['median']
    std = ['std']
    min = ['min']
    max = ['max']
    range = ['range']
    quartile_25_percent = ['25%']
    quartile_50_percent = ['50%']
    quartile_75_percent = ['75%']

    return table

# Function to generate statistics for a DataFrame
def generate_statistics(df):
    
    columns = list(df.columns)
    if len(columns) >= 8:
        final_table=[]
        split_length = len(columns) // 2
        columns = [columns[:split_length], columns[split_length:]]

        for column in columns:
            final_table.append(compute_statistics(column, df))
            
    else:
        final_table = compute_statistics(columns, df)

    return final_table
            
# Function to validate if a table is properly formatted
def validate_table(table):
    """
    Validate if a table is properly formatted.

    Parameters:
        table (list of lists): Input table.

    Returns:
        bool: True if table is properly formatted, False otherwise.
    """
    for element in table:
        if isinstance(element, list):
            if all(isinstance(sub_ele, list) for sub_ele in element):
                return True
            else:
                return False
                

# Function to generate a PDF report
def generate_pdf(file, graph_parameters):
    """
    Generate a PDF report.

    Parameters:
        file (str): Path to the CSV file.
        graph_parameters (dict): Parameters for generating graph.

    Returns:
        str: Path to the generated PDF report.
    """

    dataframe = pd.read_csv(file)
    tables = generate_statistics(dataframe)
    
    # Instructions and queries for generating report
    instructuions = """
        - Do not mention 'The provided data or The provided data is in the form of a table', just give me straight response
        - Do not mention 'df' in the explanation, use table either.
        - Like the table contatins,...
    """
    queries = [
        f'Give me a brief explanation about the data provided, the explanation should at least contain 3 lines.follow these instructions: {instructuions}',
        f'Explain this statistics table: {tables}, of the provided data.follow these instructions: {instructuions}'
    ]

    responses={}
    llm = CsvAnalyzer()
    # Invoking the llm to generate response for the queries
    for index, query in enumerate (queries):
        response = llm.csv_model(file, query)
        responses[index] = response


    # Create folder and file path for saving report
    file_name = os.path.basename(file).split('.')
    folder_path = os.path.join(os.getcwd(), 'reports')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    report_path = os.path.join(folder_path, f'{file_name[0]}.pdf')

    # Set up PDF document
    pdf = SimpleDocTemplate(report_path, )
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    paragraph_style = styles['BodyText']

    justified_paragraph_style = ParagraphStyle(
        paragraph_style.name,
        parent=paragraph_style,
        alignment=TA_JUSTIFY,
        fontName="Times-Roman",
        leading= 2 * paragraph_style.fontSize
    )

    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=16,
        spaceAfter=10,
        spaceBefore=10
    )

    table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    title_space = Spacer(1, 12)
    sub_space = Spacer(1,6)
    
    # Add content to PDF
    title = Paragraph("Report", title_style)
    sub_heading1= Paragraph("Summary: ", subheading_style)
    sub_heading2= Paragraph("Statistics: ", subheading_style)
    sub_heading3= Paragraph("Explanation:", subheading_style)
    sub_heading4= Paragraph("Graph",subheading_style)

    summary= Paragraph(responses[0], justified_paragraph_style)
    content = [title, title_space, sub_heading1, sub_space, summary, sub_space, sub_heading2, sub_space]

    page_width = letter[0]
    left_margin = 0.5 * inch
    right_margin = 0.5 * inch
    available_width = page_width - left_margin - right_margin

    if validate_table(tables):
        for table in tables:
            num_columns = len(table[0])
            column_width = available_width / num_columns
            col_widths = [column_width] * num_columns

            data = Table(table, colWidths=col_widths)
            data.setStyle(table_style)
            
            
            content.append(data)
            content.append(Spacer(1, 20))

    else:
        num_columns = len(tables)
        column_width = available_width / num_columns
        col_widths = [column_width] * num_columns

        data = Table(tables, colWidths=col_widths)
        data.setStyle(table_style)
        content.append(data)
        content.append(Spacer(1,20))



    # content.append(sub_space)
    content.append(sub_heading3)
    content.append(sub_space)
    content.append(Paragraph(responses[1],justified_paragraph_style))

    # Generate and add graph to PDF if parameters are provided
    if graph_parameters:
        if graph_parameters['plot_type']=='Pie Chart':
            image = graph.pie_chart(dataframe, graph_parameters['value'], graph_parameters['label'])
        elif graph_parameters['plot_type']=='Bar Graph':
            image= graph.bar_graph(
                                    dataframe, 
                                    graph_parameters['x_column'], 
                                    graph_parameters['y_columns'],
                                    graph_parameters['x_label'],
                                    graph_parameters['y_label']
                                    )
        else:
            image= graph.line_grapg(
                                    dataframe, 
                                    graph_parameters['x_column'], 
                                    graph_parameters['y_columns'],
                                    graph_parameters['x_label'],
                                    graph_parameters['y_label']
                                    )
            
        print (image)
        content.append(PageBreak())
        content.append(sub_heading4)
        content.append(sub_space)
        resized_image = Image(image, width=300, height=200)
        content.append(resized_image)
        content.append(sub_space)
        graph_summary= llm.process_graph(image, dataframe)
        content.append(Paragraph(graph_summary, justified_paragraph_style))


    # Build PDF document
    pdf.build(content)

    return report_path

