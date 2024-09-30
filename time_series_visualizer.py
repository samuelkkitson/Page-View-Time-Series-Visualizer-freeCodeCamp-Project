import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=['date'])

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    # Set up figure size (width=15, height=5)
    fig, ax = plt.subplots(figsize=(15, 5))  # Adjust these values to change width and height

    # Plot the data
    ax.plot(df.index, df['value'], "r")  # Make sure to specify the x and y data correctly
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()  
    df_bar['Year'] = df_bar.index.year  
    df_bar['Month'] = df_bar.index.month 

    # Group by Year and Month and calculate the average page views
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().reset_index()
    
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Step 6: Plot using Matplotlib
    # Create a pivot table to arrange data for plotting
    pivot_df = df_bar.pivot(index='Year', columns='Month', values='value')

    # Plot the bar chart
    pivot_df.plot(kind='bar', ax=ax, color=plt.cm.Set1.colors)

    # Customize the plot
    ax.set_title('Average Daily Page Views Per Month (Grouped by Year)')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Customize the legend to show month names
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    # Update legend labels to month names
    handles, labels = ax.get_legend_handles_labels()
    new_labels = [month_names[int(label)] for label in labels]  # Replace numbers with month names
    ax.legend(handles, new_labels, title='Months', loc='upper left', bbox_to_anchor=(1.0, 1.0))

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Create a figure with two subplots
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)
    
    # Yearly boxplot
    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Monthly boxplot
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
