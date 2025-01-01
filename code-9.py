import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


csv_file_path = "YTU_General_Data.csv"
csv_file_path_dep = "ytu_department_yearly_per_change"
csv_file_path_fac = "yut_faculty_yearly_per_change.csv"
csv_file_path_ytu = "ytu_yearly_per_change.csv"


df = pd.read_csv(csv_file_path)
df_dep_change = pd.read_csv(csv_file_path_dep)
df_fac_change = pd.read_csv(csv_file_path_fac)
df_ytu_change = pd.read_csv(csv_file_path_ytu)

# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.1. Success Order Analysis: function for: Question 9
# 10.2.3. Correct Answer Analysis: function for: Question 5
# 10.2.4. Gender Analysis: function for: Question 3
# 10.2.5. Quota, Student Number and Preferred Number Analysis: function for: Question 12
# 10.2.7. Exchange Program Analysis: function for: Question 6


def compare_math_programs(data):
    # Filter data for "Mathematical Engineering" and "Mathematical Engineering (English)"
    math_depts = data[
        data["Department Name"].str.contains("Mathematical Engineering", case=False, na=False)
    ]

    # Separate the data for Turkish and English programs
    turkish_program = math_depts[math_depts["Department Name"] == "Mathematical Engineering"]
    english_program = math_depts[math_depts["Department Name"] == "Mathematical Engineering (English)"]

    # Convert year and percentage columns to numeric for analysis
    turkish_program["Year"] = turkish_program["Year"].astype(int)
    english_program["Year"] = english_program["Year"].astype(int)

    # New columns of interest (three groups of metrics)
    columns_group_1 = [
        "Year", "Total Male Number Change (%)", "Total Female Number Change (%)",
        "Total Student Number Change (%)", "Exchange to Abroad Change (%)"
    ]
    columns_group_2 = [
        "Professors Change (%)", "Assoc Prof Change (%)", "Phd Change (%)"
    ]
    columns_group_3 = [
        "Base Point Change (%)", "Success Order Change (%)",
        "Preferred number Change (%)", "Quota Change (%)",
        "Total Correct TYT Change (%)", "Total Correct AYT Change (%)"
    ]

    # Include Academician Change as combined Phd, Assoc Prof, and Professors Change
    turkish_program["Academician Change (%)"] = (
        turkish_program["Professors Change (%)"] +
        turkish_program["Assoc Prof Change (%)"] +
        turkish_program["Phd Change (%)"]
    )

    english_program["Academician Change (%)"] = (
        english_program["Professors Change (%)"] +
        english_program["Assoc Prof Change (%)"] +
        english_program["Phd Change (%)"]
    )/3

    # Create a function to plot a group of metrics without the legend
    def plot_group(columns, turkish_program, english_program):
        fig, axes = plt.subplots(len(columns) - 1, 1, figsize=(14, 15))
        plt.subplots_adjust(hspace=0.4)

        # Plot each metric separately
        for i, column in enumerate(columns[1:]):
            axes[i].plot(
                turkish_program["Year"],
                turkish_program[column],
                marker="o", linestyle='-', color="blue", alpha=0.7
            )
            axes[i].plot(
                english_program["Year"],
                english_program[column],
                marker="x", linestyle='--', color="green", alpha=0.7
            )

            # Add titles and labels for each subplot
            axes[i].set_title(f"{column} - Yearly Changes", fontsize=12)
            axes[i].set_xlabel("Year", fontsize=10)
            axes[i].set_ylabel("Percentage Change (%)", fontsize=10)
            axes[i].set_xticks([2022, 2023, 2024])  # Set X-axis ticks to be exact years
            axes[i].set_xticklabels(["2022", "2023", "2024"])

        # Show the plot without legend
        plt.show()

    # Plot each group of columns separately without the legend
    plot_group(columns_group_1, turkish_program, english_program)
    plot_group(columns_group_2, turkish_program, english_program)
    plot_group(columns_group_3, turkish_program, english_program)


compare_math_programs(df_dep_change)
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.4. Gender Analysis: function for: Question 4

def plot_top_5_gender_changes_by_year(data):
    # Filter out departments with "(TRNC Citizens)"
    filtered_data = data[~data["Department Name"].str.contains(r"\(TRNC Citizens\)", na=False)]

    # Unique years in the dataset
    years = filtered_data["Year"].unique()

    for year in sorted(years):
        # Filter data for the specific year
        year_data = filtered_data[filtered_data["Year"] == year]
        year_data = year_data.dropna(subset=["Male Change (%)", "Female Change (%)"])
        year_data["Male Change (%)"] = year_data["Male Change (%)"].astype(float)
        year_data["Female Change (%)"] = year_data["Female Change (%)"].astype(float)

        if year_data.empty:
            continue

        # Get the top 5 departments for each metric
        top_5_max_male = year_data.nlargest(5, "Male Change (%)")[["Department Name", "Male Change (%)"]]
        top_5_min_male = year_data.nsmallest(5, "Male Change (%)")[["Department Name", "Male Change (%)"]]
        top_5_max_female = year_data.nlargest(5, "Female Change (%)")[["Department Name", "Female Change (%)"]]
        top_5_min_female = year_data.nsmallest(5, "Female Change (%)")[["Department Name", "Female Change (%)"]]

        # Prepare data for plotting
        data_labels = ["Max Male Increase", "Min Male Decrease", "Max Female Increase", "Min Female Decrease"]
        top_5_values = [
            top_5_max_male["Male Change (%)"].tolist(),
            top_5_min_male["Male Change (%)"].tolist(),
            top_5_max_female["Female Change (%)"].tolist(),
            top_5_min_female["Female Change (%)"].tolist(),
        ]
        departments = [
            top_5_max_male["Department Name"].tolist(),
            top_5_min_male["Department Name"].tolist(),
            top_5_max_female["Department Name"].tolist(),
            top_5_min_female["Department Name"].tolist(),
        ]

        # Define colors for each category
        colors = [
            ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd"],  # Max Male Increase (blue shades)
            ["#aec7e8", "#98df8a", "#ffbb78", "#ff9896", "#c5b0d5"],  # Min Male Decrease (light blue shades)
            ["#17becf", "#bcbd22", "#e377c2", "#7f7f7f", "#8c564b"],  # Max Female Increase (teal shades)
            ["#9edae5", "#dbdb8d", "#f7b6d2", "#c7c7c7", "#c49c94"],  # Min Female Decrease (light teal shades)
        ]

        # Plot the data
        plt.figure(figsize=(12, 8))
        for idx, (label, values, dept_names, color) in enumerate(zip(data_labels, top_5_values, departments, colors)):
            plt.bar(
                [f"{label}\n{i + 1}" for i in range(len(values))],  # Position labels
                values, color=color, label=label
            )
            for i, (val, dept) in enumerate(zip(values, dept_names)):
                plt.text(idx * 5 + i, val, dept, ha="center", va="bottom", fontsize=8)

        # Styling
        plt.title(f"Top 5 Gender Ratio Changes ({year})", fontsize=14)
        plt.ylabel("Percentage Change (%)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Change Categories", fontsize=10)
        plt.tight_layout()
        plt.show()


plot_top_5_gender_changes_by_year(df_dep_change)
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.5. Quota, Student Number and Preferred Number Analysis: function for: Question 9

def plot_faculty_enrollment_change(exclude_years):

    # Filter out the excluded years
    filtered_data = df_fac_change[~df_fac_change['Year'].isin(exclude_years)]

    # Select relevant columns for the graph
    faculty_enrollment_data = filtered_data[['Year', 'Faculty Name', 'Total Student Number Change (%)']]

    # Pivot the data for better plotting
    pivot_data = faculty_enrollment_data.pivot(index='Faculty Name', columns='Year',
                                               values='Total Student Number Change (%)')

    # Plotting the data
    plt.figure(figsize=(10, 6))
    pivot_data.plot(kind='bar', figsize=(15, 8), width=0.8)

    plt.title('Total Student Enrollment Change by Faculty', fontsize=14)
    plt.xlabel('Faculty', fontsize=12)
    plt.ylabel('Change (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Year', fontsize=10)
    plt.tight_layout()

    # Show the plot
    plt.show()


# Call the function
plot_faculty_enrollment_change(exclude_years=[2021, 2024])
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.5. Quota, Student Number and Preferred Number Analysis: function for: Question 8

def plot_faculty_quota_change(exclude_years):

    # Filter out the excluded years
    filtered_data = df_fac_change[~df_fac_change['Year'].isin(exclude_years)]

    # Select relevant columns for the graph
    faculty_quota_data = filtered_data[['Year', 'Faculty Name', 'Quota Change (%)']]

    # Pivot the data for better plotting
    pivot_data = faculty_quota_data.pivot(index='Faculty Name', columns='Year', values='Quota Change (%)')

    # Plotting the data
    plt.figure(figsize=(10, 6))
    pivot_data.plot(kind='bar', figsize=(15, 8), width=0.8)

    plt.title('Quota Change by Faculty', fontsize=14)
    plt.xlabel('Faculty', fontsize=12)
    plt.ylabel('Change (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Year', fontsize=10)
    plt.tight_layout()

    # Show the plot
    plt.show()


plot_faculty_quota_change(exclude_years=[2021])
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.7. Exchange Program Analysis: function for: Question 10

def plot_ytu_yearly_changes_with_exchange(exclude_years):
    """
    Plot the total yearly student enrollment change and exchange from abroad for Yıldız Technical University,
    excluding specified years.

    Parameters:
    - data_path (str): Path to the CSV file containing the data.
    - exclude_years (list): List of years to exclude from the plot.

    Returns:
    - None
    """

    # Filter out the excluded years
    filtered_data = df_ytu_change[~df_ytu_change['Year'].isin(exclude_years)]

    # Group by year and calculate the mean change for relevant columns
    yearly_change_data = filtered_data.groupby('Year')[
        ['Exchange to Abroad Change (%)', 'Exchange from Abroad Change (%)']
    ].mean()

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_change_data.index, yearly_change_data['Exchange to Abroad Change (%)'], marker='o', label='Exchange to Abroad Change (%)', linewidth=2)
    plt.plot(yearly_change_data.index, yearly_change_data['Exchange from Abroad Change (%)'], marker='o', label='Exchange from Abroad Change (%)', linewidth=2)

    plt.title('Yearly Changes at YTU (Student Exchange)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Change (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(yearly_change_data.index.astype(int))  # Ensure x-axis shows integers
    plt.legend(fontsize=10)
    plt.tight_layout()

    # Show the plot
    plt.show()


# Call the function
plot_ytu_yearly_changes_with_exchange(exclude_years=[2021, 2024])

# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# 10.2.9. General Analysis: function for: Question 4

def plot_ytu_yearly_gender_student_change(exclude_years):
    """
    Plot the yearly changes in total male, female, and student enrollment for Yıldız Technical University,
    excluding specified years.

    Parameters:
    - data_path (str): Path to the CSV file containing the data.
    - exclude_years (list): List of years to exclude from the plot.

    Returns:
    - None
    """

    # Filter out the excluded years
    filtered_data = df_ytu_change[~df_ytu_change['Year'].isin(exclude_years)]

    # Group by year and calculate the mean change for relevant columns
    yearly_change_data = filtered_data.groupby('Year')[
        ['Total Male Number Change (%)', 'Total Female Number Change (%)', 'Total Student Number Change (%)']
    ].mean()

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_change_data.index, yearly_change_data['Total Male Number Change (%)'], marker='o', label='Male Change (%)', linewidth=2)
    plt.plot(yearly_change_data.index, yearly_change_data['Total Female Number Change (%)'], marker='o', label='Female Change (%)', linewidth=2)
    plt.plot(yearly_change_data.index, yearly_change_data['Total Student Number Change (%)'], marker='o', label='Total Student Change (%)', linewidth=2)

    plt.title('Yearly Changes at YTU (Male, Female, and Total Students)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Change (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(yearly_change_data.index.astype(int))  # Ensure x-axis shows integers
    plt.legend(fontsize=10)
    plt.tight_layout()

    # Show the plot
    plt.show()


# Call the function
plot_ytu_yearly_gender_student_change(exclude_years=[2021, 2024])
# -------------------------------------------------------------------------------------------------------------------- #

