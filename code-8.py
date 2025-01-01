import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


csv_file_path = "YTU_General_Data.csv"

df = pd.read_csv(csv_file_path)

# ---------------------------------------------------------------------------------------------------------------- #
# 10.2.1. Success Order Analysis: function for: Question 2, 4, 6, 8
# 10.2.2. Base Point Analysis: function for: Question 1, 2, 3, 4


def plot_department_analysis_with_highest_subjects(data, department_type, analysis_type, subjects=None, year=None):
    """
    Plots analysis for departments based on the given type, analysis category, and year(s),
    and prints the department with the highest score for each subject.

    Parameters:
        data (DataFrame): The dataset containing department data.
        department_type (str): The type of department (e.g., 'SAY', 'EA', 'DİL').
        analysis_type (str): The type of analysis ('scores', 'base_points', 'success_order').
        subjects (list, optional): List of subjects to compare (used for 'scores' analysis).
        year (int, optional): Specific year to filter data; if None, plots yearly data as grouped bars.

    Returns:
        None
    """
    # Filter data based on department type
    filtered_data = data[data['Department Type'] == department_type]

    if year:
        # Filter by the specified year
        filtered_data = filtered_data[filtered_data['Year'] == year]

    if analysis_type == 'scores' and subjects:
        # Group by department and calculate mean scores for specified subjects
        score_data = filtered_data.groupby('Department Name')[subjects].mean()
        score_data.plot(kind='bar', figsize=(10, 6))
        title_year = f"for {year}" if year else "over all years"
        plt.title(f"{department_type} Departments: Comparison of {', '.join(subjects)} Scores {title_year}")
        plt.ylabel("Average Score")
        plt.xlabel("Department Name")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Subject")
        plt.tight_layout()
        plt.show()

        # Identify the department with the highest score for each subject
        for subject in subjects:
            highest_department = score_data[subject].idxmax()
            highest_score = score_data[subject].max()
            print(f"{highest_department} department has the highest score at {subject} ({highest_score:.2f}).")

    elif analysis_type in ['base_points', 'success_order']:
        metric = 'Base Point' if analysis_type == 'base_points' else 'Success Order'

        if year:
            # Calculate and plot data for a single year
            metric_data = filtered_data.groupby('Department Name')[metric].mean()
            metric_data.sort_values().plot(kind='bar', figsize=(10, 6))
            plt.title(f"{department_type} Departments: Comparison of {metric} for {year}")
            plt.ylabel(f"Average {metric}")
            plt.xlabel("Department Name")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        else:
            # Plot yearly data as grouped bars for each department
            yearly_data = filtered_data.pivot_table(index='Department Name', columns='Year', values=metric)
            yearly_data.plot(kind='bar', figsize=(12, 6))
            plt.title(f"{department_type} Departments: Yearly Comparison of {metric}")
            plt.ylabel(f"Average {metric}")
            plt.xlabel("Department Name")
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Year")
            plt.tight_layout()
            plt.show()

    else:
        print("Invalid analysis type or missing parameters for the selected analysis.")


plot_department_analysis_with_highest_subjects(df, 'SAY', 'success_order')
plot_department_analysis_with_highest_subjects(df, 'EA', 'success_order')
plot_department_analysis_with_highest_subjects(df, 'SÖZ', 'success_order')
plot_department_analysis_with_highest_subjects(df, 'DİL', 'success_order')

plot_department_analysis_with_highest_subjects(df, 'SAY', 'base_points')
plot_department_analysis_with_highest_subjects(df, 'EA', 'base_points')
plot_department_analysis_with_highest_subjects(df, 'SÖZ', 'base_points')
plot_department_analysis_with_highest_subjects(df, 'DİL', 'base_points')
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.1. Success Order Analysis: function for: Question 12

def plot_success_order_distribution(data):
    """
    Create a distribution chart for success order.

    Parameters:
        data (str): Path to the CSV file containing the data.

    Returns:
        None
    """
    try:

        # Define the column name for success order
        column_name = "Success Order"

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the data.")

        # Drop any missing or invalid values in the column
        success_order = df[column_name].dropna()

        # Plot the histogram
        plt.figure(figsize=(10, 6))
        plt.hist(success_order, bins=20, edgecolor='black', alpha=0.7)
        plt.title("Success Order Distribution", fontsize=14)
        plt.xlabel("Success Order", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


plot_success_order_distribution(df)
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.3. Correct Answer Analysis: function for: Question 1, 2, 3, 4


def calculate_and_display_changes(group_type, subjects, title):
    # Filter data for the specific group
    group_data = df[df['Department Type'] == group_type]

    # Calculate year-over-year changes for the subjects
    yearly_changes = group_data.groupby(['Department Name', 'Year'])[subjects].mean().reset_index()
    yearly_changes['Department Name'] = yearly_changes['Department Name']  # Retain Department Name for alignment
    yearly_changes_diff = yearly_changes.groupby('Department Name')[subjects].diff()
    yearly_changes_diff['Department Name'] = yearly_changes['Department Name']  # Reattach Department Names

    # Calculate the average yearly change for each department and subject
    average_yearly_changes = yearly_changes_diff.groupby('Department Name').mean()

    # Plot the changes with department names as x-axis labels
    plt.figure(figsize=(20, 10))
    for subject in subjects:
        plt.bar(
            x=average_yearly_changes.index,
            height=average_yearly_changes[subject],
            label=subject,
            alpha=0.7
        )

    # Customize the chart
    plt.title(title)
    plt.ylabel("Average Yearly Score Change")
    plt.xlabel("Departments")
    plt.xticks(rotation=90, ha="right", fontsize=8)  # Rotate x-axis labels for visibility
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title="Subjects")
    plt.tight_layout()
    plt.show()


calculate_and_display_changes(
    "SAY",
    ['AYT Biology', 'AYT Physics', 'AYT Chemistry'],
    "Average Yearly Score Changes for SAY Departments"
)

calculate_and_display_changes(
    "EA",
    ['AYT Literature', 'AYT History1', 'AYT Geography1'],
    "Average Yearly Score Changes for EA Departments"
)

calculate_and_display_changes(
    "SÖZ",
    ['AYT Literature', 'AYT Geography1', 'AYT Geography2', 'AYT Religion', 'AYT Philosophy', 'AYT History1',
     'AYT History2'],
    "Average Yearly Score Changes for SÖZ Departments"
)

calculate_and_display_changes(
    "DİL",
    ['YDT Foreign Language'],
    "Average Yearly Score Changes for DİL Departments"
)
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.4. Gender Analysis: function for: Question 1

def analyze_and_visualize_performance(data, column='TYT Math', top_n=5, department_type=None):
    """
    Analyzes and visualizes gender representation in the specified column.

    Parameters:
        data (DataFrame): The dataset containing gender and performance columns.
        column (str): The column name for the performance metric to analyze.
        top_n (int): Number of top departments to analyze.
        department_type (str): Filter for department type (e.g., 'SAY', 'EA', 'SÖZ').

    Returns:
        None: Displays a bar chart of male and female percentages for the top departments.
    """
    if column not in data.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataset.")

    # Filter by department type if specified
    if department_type:
        data = data[data['Department Type'] == department_type]
        if data.empty:
            raise ValueError(f"No data available for department type '{department_type}'.")

    # Calculate average scores for each department
    department_avg = data.groupby('Department Name').agg(
        avg_score=(column, 'mean'),
        total_male=('Male', 'sum'),
        total_female=('Female', 'sum')
    ).reset_index()

    # Calculate percentages for males and females
    department_avg['total_students'] = department_avg['total_male'] + department_avg['total_female']
    department_avg['male_percentage'] = department_avg['total_male'] / department_avg['total_students'] * 100
    department_avg['female_percentage'] = department_avg['total_female'] / department_avg['total_students'] * 100

    # Sort departments by average score and select top N
    top_departments = department_avg.sort_values(by='avg_score', ascending=False).head(top_n)

    # Append average score to department names for labeling
    top_departments['department_label'] = top_departments.apply(
        lambda row: f"{row['Department Name']} ({row['avg_score']:.2f})", axis=1
    )

    # Replace underscores with spaces in the column name for the title
    column_title = column.replace('_', ' ')

    # Plotting the results
    x = np.arange(len(top_departments['department_label']))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_male = ax.bar(x - width / 2, top_departments['male_percentage'], width, label='Male %')
    bars_female = ax.bar(x + width / 2, top_departments['female_percentage'], width, label='Female %')

    # Adding labels and title
    ax.set_xlabel('Department')
    ax.set_ylabel('Percentage')
    ax.set_title(f'Male vs Female Percentage in Top {top_n} Departments by {column_title.capitalize()}' +
                 (f" ({department_type})" if department_type else ""))
    ax.set_xticks(x)
    ax.set_xticklabels(top_departments['department_label'], rotation=45, ha='right')
    ax.legend()

    # Display percentages on the bars
    for bar in bars_male + bars_female:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


analyze_and_visualize_performance(df, column='Total Correct TYT', top_n=5)
analyze_and_visualize_performance(df, column='Total Correct AYT', top_n=5)
analyze_and_visualize_performance(df, column='Total Correct YDT', top_n=2)
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.7. Exchange Program Analysis: function for: Question 3

def plot_success_order_exchange_program(data):
    """
    Create a bar chart showing the average exchange program participation
    (Exchange to Abroad) by success category, with the data categorized by
    departments. The year 2024 is excluded from the analysis.

    Parameters:
        data (str): Path to the CSV file containing the data.

    Returns:
        None
    """
    try:

        # Define the column names
        success_order_col = "Success Order"
        exchange_abroad_col = "Exchange to Abroad"
        year_col = "Year"

        # Exclude the year 2024 from the analysis
        data = data[data[year_col] != 2024]

        # Check if necessary columns exist
        for col in [success_order_col, exchange_abroad_col]:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the data.")

        # Calculate success percentiles
        low_threshold = data[success_order_col].quantile(0.66)
        medium_threshold = data[success_order_col].quantile(0.33)

        # Categorize departments by success
        def categorize_success(order):
            if order <= medium_threshold:
                return "High Success"
            elif order <= low_threshold:
                return "Medium Success"
            else:
                return "Low Success"

        data["Success Category"] = data[success_order_col].apply(categorize_success)

        # Calculate average exchange participation per department by success category
        avg_exchange = data.groupby(["Success Category"])[exchange_abroad_col].mean()

        # Sort categories for proper display
        avg_exchange = avg_exchange.reindex(["High Success", "Medium Success", "Low Success"])

        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        avg_exchange.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.title("Exchange Program Participation by Success Category", fontsize=14)
        plt.xlabel("Success Category", fontsize=12)
        plt.ylabel("Average Exchange Program Participation", fontsize=12)
        plt.xticks(rotation=0)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


plot_success_order_exchange_program(df)
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.8. Regions and Cities Analysis: function for: Question 1

def analyze_and_plot_regional_distribution(data, region_columns, year_column='Year'):
    """
    Analyzes regional student representation and plots all years on a single grouped bar chart.

    Args:
        data (pd.DataFrame): Data containing regional enrollment numbers.
        region_columns (list): Columns representing student counts by region.
        year_column (str): Column representing the year.

    Returns:
        pd.DataFrame: A DataFrame showing the total number of students from each region for each year.
    """
    # Replace underscores in region column names with spaces for better readability
    region_columns_cleaned = [region.replace('_', ' ') for region in region_columns]

    # Group data by year and sum the regional columns
    yearly_regional_totals = data.groupby(year_column)[region_columns].sum().reset_index()

    # Plot grouped bar chart
    plt.figure(figsize=(12, 8))
    bar_width = 0.15
    x = range(len(region_columns_cleaned))  # Base x positions for the regions

    for i, year in enumerate(yearly_regional_totals[year_column]):
        values = yearly_regional_totals.loc[i, region_columns]
        plt.bar([pos + bar_width * i for pos in x], values, bar_width, label=f'{int(year)}')

    # Add plot details
    plt.title('Regional Student Distribution Over the Years', fontsize=16)
    plt.xlabel('Regions', fontsize=14)
    plt.ylabel('Number of Students', fontsize=14)
    plt.xticks([pos + bar_width * (len(yearly_regional_totals[year_column]) / 2) for pos in x],
               region_columns_cleaned, rotation=45, fontsize=12)
    plt.legend(title='Year', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Return the yearly regional totals
    return yearly_regional_totals


analyze_and_plot_regional_distribution(df, region_columns=['Marmara','Aegean', 'Mediterranean', 'Black Sea',
                                                           'Central Anatolia', 'Eastern Anatolia',
                                                           'Southeastern Anatolia'])
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.9. General Analysis: function for: Question 1

def total_student_number_analysis_with_plot(dataframe, group_col):
    """
    Analyze total student numbers over years and generate a comparative bar chart.

    Args:
        dataframe (pd.DataFrame): Dataframe to analyze.
        group_col (str): Column for grouping (e.g., 'faculty_name' or 'department_name').

    Returns:
        pd.DataFrame: Sorted table of total student numbers and changes by group and year.
    """
    # Calculate yearly total student numbers
    year_col = "Year"

    # Exclude the year 2024 from the analysis
    dataframe = dataframe[dataframe[year_col] != 2024]

    yearly_totals = dataframe.groupby([group_col, 'Year'])['Total Student Number'].sum().reset_index()

    # Calculate changes in total student numbers
    yearly_totals['Student Number Change'] = yearly_totals.groupby(group_col)['Total Student Number'].diff().fillna(0)
    yearly_totals['Percentage Change'] = yearly_totals.groupby(group_col)['Total Student Number'].pct_change().fillna(0) * 100

    # Create a sorted table
    sorted_table = yearly_totals.sort_values(by=[group_col, 'Year']).reset_index(drop=True)

    # Generate a bar chart for total student numbers by faculty for 2021-2023
    pivot_data = yearly_totals.pivot(index=group_col, columns='Year', values='Total Student Number')

    # Plot total student numbers comparison
    pivot_data.plot(kind='bar', figsize=(12, 8), width=0.8, color=['orange', 'red', 'pink'])
    plt.title('Total Student Numbers by Faculty for 2021-2023')
    plt.ylabel('Total Student Number')
    plt.xlabel('Faculty Name')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Year', loc='upper right')
    plt.tight_layout()
    plt.show()

    return sorted_table


total_student_number_analysis_with_plot(df, group_col="Faculty Name")
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.9. General Analysis: function for: Question 2

def analyze_base_point_correlations(data):
    """
    Analyze the correlations between base points and influencing factors.

    Args:
        data (pd.DataFrame): The dataset containing base points and potential influencing factors.

    Returns:
        pd.DataFrame: Correlation matrix of factors influencing base points.
    """
    factors = ['Base Point', 'Success Order', 'Preferred number','Total Correct TYT','Total Correct AYT', 'Marmara',
               'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']
    correlation_matrix = data[factors].corr()
    print("Correlation Matrix for Base Points:")
    print(correlation_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Base Points and Influencing Factors')
    plt.show()

    return correlation_matrix


analyze_base_point_correlations(df)
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.9. General Analysis: function for: Question 3

def perform_regression_analysis(data_frame):
    """
    Performs regression analysis on the provided DataFrame to examine the relationship
    between Base Point and Preferred Number.

    Parameters:
    - data_frame: Pandas DataFrame containing the data to analyze.

    Returns:
    - Regression summary and displays a regression plot.
    """
    # Filter necessary columns for analysis
    relevant_columns = ["Department Name", "Year", "Base Point", "Preferred number"]
    analysis_data = data_frame[relevant_columns].dropna()

    # Ensure the data types are appropriate
    analysis_data["Base Point"] = pd.to_numeric(analysis_data["Base Point"], errors='coerce')
    analysis_data["Preferred number"] = pd.to_numeric(analysis_data["Preferred number"], errors='coerce')

    # Check for missing or invalid data
    analysis_data = analysis_data.dropna()

    # Perform regression analysis
    X = analysis_data["Base Point"]
    y = analysis_data["Preferred number"]
    X = sm.add_constant(X)  # Add a constant for the regression

    # Fit the regression model
    model = sm.OLS(y, X).fit()
    regression_summary = model.summary()

    # Visualize the regression
    plt.figure(figsize=(10, 6))
    sns.regplot(x="Base Point", y="Preferred number", data=analysis_data, line_kws={"color": "red"})
    plt.title("Regression Analysis: Base Point vs. Preferred Number")
    plt.xlabel("Base Point")
    plt.ylabel("Preferred Number")
    plt.grid()
    plt.tight_layout()
    plt.show()

    return regression_summary


perform_regression_analysis(df)
# ----------------------------------------------------------------------------------------------------------------- #
