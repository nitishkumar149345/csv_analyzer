import matplotlib.pyplot as plt
import pandas as pd
import os

# Function to generate a line graph
def line_grapg(df, x_column, y_columns, xl, yl):
    """
    Generate a line graph from DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame.
        x_column (str): Column name for x-axis.
        y_columns (list of str): Column names for y-axis.
        x_label (str): Label for x-axis.
        y_label (str): Label for y-axis.

    Returns:
        str: Path to the generated line graph image.
    """
    for value in y_columns:
        plt.plot(df[x_column],df[value],label= value)

    plt.title("Line Graph")
    plt.xticks(rotation=90, ha='right')
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend()
    plt.tight_layout()

    # Save the plot to an image file
    path= os.path.join(os.getcwd(),'static','linegraph.jpeg')
    plt.savefig(path)
    plt.close()
    return path


# Function to generate a bar graph
def bar_graph(df, x_column, y_columns, x_label, y_label):
    """
    Generate a bar graph from DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame.
        x_column (str): Column name for x-axis.
        y_columns (list of str): Column names for y-axis.
        x_label (str): Label for x-axis.
        y_label (str): Label for y-axis.

    Returns:
        str: Path to the generated bar graph image.
    """
    names = df[x_column]
    x = range(len(names))
    width = 0.35  

    fig, ax = plt.subplots()
    for i, y_column in enumerate(y_columns):
        ax.bar([p + width * i for p in x], df[y_column], width, label=y_column)

    plt.xticks(rotation=90, ha='right')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title('Bar Graph')
    ax.set_xticks([p + width * (len(y_columns) - 1) / 2 for p in x])
    ax.set_xticklabels(names)
    ax.legend()
    plt.tight_layout()

    # Save the plot to an image file
    path = os.path.join(os.getcwd(), 'static', 'bar_graph.jpeg')
    plt.savefig(path)
    plt.close()
    return path

# Function to generate a pie chart
def pie_chart(df,value,names):
    """
    Generate a pie chart from DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame.
        value (str): Column name containing the values.
        names (str): Column name containing the labels.

    Returns:
        str: Path to the generated pie chart image.
    """

    df = df.dropna(subset=[value])
    values = pd.to_numeric(df[value], errors='coerce')
    label = df[names]
    
    plt.pie(values, labels=label,autopct='%1.1f%%')
    plt.title("Pie Chart")
    path = os.path.join(os.getcwd(),'static','pie_chart.jpeg')
    plt.savefig(path)
    return path
