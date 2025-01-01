import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
import seaborn as sns
from plotly import tools
from scipy.stats import pearsonr

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


csv_file_path = "YTU_General_Data.csv"
csv_file_path_city = "department_city_student_counts.csv"
csv_file_path_dep = "ytu_department_yearly_per_change"
csv_file_path_fac = "yut_faculty_yearly_per_change.csv"
csv_file_path_ytu = "ytu_yearly_per_change.csv"


df = pd.read_csv(csv_file_path)
df_city = pd.read_csv(csv_file_path_city)
df_dep_change = pd.read_csv(csv_file_path_dep)
df_fac_change = pd.read_csv(csv_file_path_fac)
df_ytu_change = pd.read_csv(csv_file_path_ytu)


def plot_department_analysis_with_highest_and_lowest_subjects_and_year(data, department_type, analysis_type,
                                                                       subjects=None, year=None):

    # Filter data based on department type
    filtered_data = data[(data['Department Type'] == department_type) & (~data['Department Name'].str.contains("TRNC Citizens"))]

    if year:
        # Filter by the specified year
        filtered_data = filtered_data[filtered_data['Year'] == year]

    if analysis_type == 'scores' and subjects:
        # Group by department and calculate mean scores for specified subjects
        score_data = filtered_data.groupby(['Department Name', 'Year'])[subjects].mean().reset_index()
        score_data_pivot = score_data.pivot(index='Department Name', columns='Year', values=subjects)

        # Sort and limit to top 5 departments if SAY type

        # Plot
        if year:
            score_data_year = score_data[score_data['Year'] == year].set_index('Department Name')[subjects]
            ax = score_data_year.plot(kind='bar', figsize=(10, 6))
            plt.title(f"{department_type} Departments: Comparison of {', '.join(subjects)} Scores for {year}")
        else:
            ax = score_data_pivot.plot(kind='bar', figsize=(12, 6))
            plt.title(f"{department_type} Departments: Yearly Comparison of {', '.join(subjects)} Scores")

        # Adjust legend placement
        plt.legend(title="Subject", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.ylabel("Average Score")
        plt.xlabel("Department Name")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Identify the department with the highest and lowest scores for each subject
        for subject in subjects:
            highest_row = score_data.loc[score_data[subject].idxmax()]
            lowest_row = score_data.loc[score_data[subject].idxmin()]

            print(
                f"{highest_row['Department Name']} department has the highest score at {subject} "
                f"({highest_row[subject]:.2f}) in {int(highest_row['Year'])}."
            )
            print(
                f"{lowest_row['Department Name']} department has the lowest score at {subject} "
                f"({lowest_row[subject]:.2f}) in {int(lowest_row['Year'])}."
            )

    elif analysis_type in ['base_points', 'success_order']:
        metric = 'Base Point' if analysis_type == 'base_points' else 'Success Order'

        metric_data = filtered_data.groupby(['Department Name', 'Year'])[metric].mean().reset_index()

        # Sort and limit to top 5 departments if SAY type
        if department_type == 'SAY':
            metric_data = metric_data.sort_values(by=metric, ascending=False).head(5)

        if year:
            # Calculate and plot data for a single year
            metric_data_year = metric_data[metric_data['Year'] == year].set_index('Department Name')
            ax = metric_data_year[metric].plot(kind='bar', figsize=(10, 6))
            plt.title(f"{department_type} Departments: Comparison of {metric} for {year}")
        else:
            metric_data_pivot = metric_data.pivot(index='Department Name', columns='Year', values=metric)
            ax = metric_data_pivot.plot(kind='bar', figsize=(12, 6))
            plt.title(f"{department_type} Departments: Yearly Comparison of {metric}")

        # Adjust legend placement
        plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.ylabel(f"Average {metric}")
        plt.xlabel("Department Name")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        if not year:
            # Identify highest and lowest per year
            for current_year in metric_data['Year'].unique():
                year_data = metric_data[metric_data['Year'] == current_year]
                highest_row = year_data.loc[year_data[metric].idxmax()]
                lowest_row = year_data.loc[year_data[metric].idxmin()]
                print(
                    f"{highest_row['Department Name']} department has the highest {metric.lower()} "
                    f"({highest_row[metric]:.2f}) in {int(highest_row['Year'])}."
                )
                print(
                    f"{lowest_row['Department Name']} department has the lowest {metric.lower()} "
                    f"({lowest_row[metric]:.2f}) in {int(lowest_row['Year'])}."
                )

    else:
        print("Invalid analysis type or missing parameters for the selected analysis.")


"""
plot_department_analysis_with_highest_and_lowest_subjects_and_year(
    data=df,
    department_type="DİL",
    analysis_type="base_points")

plot_department_analysis_with_highest_and_lowest_subjects_and_year(
    data=df,
    department_type="DİL",
    analysis_type="success_order")



plot_department_analysis_with_highest_and_lowest_subjects_and_year(
    data=df,
    department_type="SAY",
    analysis_type="scores",
    subjects=["TYT Math", "AYT Math"])
def calculate_subject_improvements(data, department_type, subject):

    # Grouping data to calculate trends in the specified subject across years for the specified department type
    subject_trend = data[(data["Department Type"] == department_type) & (~data["Department Name"].str.contains("TRNC Citizens"))]\
        .groupby(["Department Name", "Year"])[subject].mean().unstack()

    # Calculate the average score across years
    subject_trend["Average"] = subject_trend.mean(axis=1)

    # Calculate the improvement as the difference between the average scores of 2024 and 2021
    subject_trend["Change"] = subject_trend["Average"] - subject_trend["Average"].iloc[0]

    # Sorting by improvement to find the top departments
    subject_trend_sorted = subject_trend.sort_values(by="Change", ascending=False)

    # Plotting the improvements for the specified subject
    plt.figure(figsize=(12, 8))
    subject_trend_sorted["Change"].plot(kind='bar', color='skyblue')
    plt.title(f"{subject} Score Improvements for {department_type} Departments (Average 2021-2024)", fontsize=14)
    plt.ylabel("Score Improvement", fontsize=12)
    plt.xlabel("Department Name", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.show()

    return subject_trend_sorted


def compare_subject_improvements(data, department_type, subjects):
    
    results = {}
    for subject in subjects:
        print(f"Analyzing improvements for {subject}...")
        results[subject] = calculate_subject_improvements(data, department_type, subject)

    # Combine all improvements into one plot
    plt.figure(figsize=(20, 12))  # Larger plot size
    for subject in subjects:
        if "Change" in results[subject].columns:
            results[subject]["Change"].plot(kind='line', marker='o', label=subject)

    plt.title(f"Comparison of Score Improvements for {department_type} Departments (Average 2021-2024)", fontsize=16)
    plt.ylabel("Score Improvement", fontsize=12)
    plt.xlabel("Department Name", fontsize=12)
    plt.xticks(
        ticks=range(len(results[subjects[0]].index)),
        labels=results[subjects[0]].index,
        rotation=45, ha='right', fontsize=10
    )
    plt.legend(title="Subjects")
    plt.tight_layout()
    plt.show()

    return results


subjects_to_compare = ["AYT Math", 'AYT Literature', 'AYT Geography1', 'AYT History1']
comparison_results = compare_subject_improvements(df, "EA", subjects_to_compare)

subjects_to_compare2 = ['AYT Literature', 'AYT Geography1', 'AYT Geography2', 'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2']
comparison_results2 = compare_subject_improvements(df, "EA", subjects_to_compare2)
"""

print(df.columns)
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

# YILDIZ TEKNİK PER CHANGE GRAFİKLERİ
""" 
data_filtered = df_ytu_change[df_ytu_change['Year'] != 2021]
# First Graph: Total Male, Total Female, and Total Student Number Change (%)
plt.figure(figsize=(10, 6))
plt.plot(data_filtered['Year'], data_filtered['Total Male Number Change (%)'], label='Total Male Number Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Total Female Number Change (%)'], label='Total Female Number Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Total Student Number Change (%)'], label='Total Student Number Change (%)', marker='o')
plt.xlabel('Year')
plt.ylabel('Change (%)')
plt.title('Total Male, Female, and Student Enrollment Changes')
plt.xticks(range(int(data_filtered['Year'].min()), int(data_filtered['Year'].max()) + 1))
plt.legend()
plt.grid(True)
plt.show()

# Second Graph: Exchange to Abroad and Exchange from Abroad Change (%)
plt.figure(figsize=(10, 6))
plt.plot(data_filtered['Year'], data_filtered['Exchange to Abroad Change (%)'], label='Exchange to Abroad Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Exchange from Abroad Change (%)'], label='Exchange from Abroad Change (%)', marker='o')
plt.xlabel('Year')
plt.ylabel('Change (%)')
plt.title('Exchange Program Changes (To and From Abroad)')
plt.xticks(range(int(data_filtered['Year'].min()), int(data_filtered['Year'].max()) + 1))
plt.legend()
plt.grid(True)
plt.show()

# Third Graph: Academician Change (%) (Average of Professors, Assoc Prof, PhD), and other metrics
academician_change = (data_filtered['Professors Change (%)'] + data_filtered['Assoc Prof Change (%)'] + data_filtered['Phd Change (%)']) / 3

plt.figure(figsize=(10, 6))
plt.plot(data_filtered['Year'], academician_change, label='Academician Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Base Point Change (%)'], label='Base Point Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Success Order Change (%)'], label='Success Order Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Preferred number Change (%)'], label='Preferred number Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Quota Change (%)'], label='Quota Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Placed Number Change (%)'], label='Placed Number Change (%)', marker='o')
plt.xlabel('Year')
plt.ylabel('Change (%)')
plt.title('Academic and Enrollment Metrics Changes')
plt.xticks(range(int(data_filtered['Year'].min()), int(data_filtered['Year'].max()) + 1))
plt.legend()
plt.grid(True)
plt.show()

# Fourth Graph: Total Correct TYT, AYT, and YDT Change (%)
plt.figure(figsize=(10, 6))
plt.plot(data_filtered['Year'], data_filtered['Total Correct TYT Change (%)'], label='Total Correct TYT Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Total Correct AYT Change (%)'], label='Total Correct AYT Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Total Correct YDT Change (%)'], label='Total Correct YDT Change (%)', marker='o')
plt.xlabel('Year')
plt.ylabel('Change (%)')
plt.title('Total Correct Exam Scores Change (TYT, AYT, YDT)')
plt.xticks(range(int(data_filtered['Year'].min()), int(data_filtered['Year'].max()) + 1))
plt.legend()
plt.grid(True)
plt.show()

# Fifth Graph: Regional Enrollment Changes
plt.figure(figsize=(10, 6))
plt.plot(data_filtered['Year'], data_filtered['Marmara Change (%)'], label='Marmara Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Aegean Change (%)'], label='Aegean Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Mediterranean Change (%)'], label='Mediterranean Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Black Sea Change (%)'], label='Black Sea Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Central Anatolia Change (%)'], label='Central Anatolia Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Eastern Anatolia Change (%)'], label='Eastern Anatolia Change (%)', marker='o')
plt.plot(data_filtered['Year'], data_filtered['Southeastern Anatolia Change (%)'], label='Southeastern Anatolia Change (%)', marker='o')
plt.xlabel('Year')
plt.ylabel('Change (%)')
plt.title('Regional Enrollment Changes')
plt.xticks(range(int(data_filtered['Year'].min()), int(data_filtered['Year'].max()) + 1))
plt.legend()
plt.grid(True)
plt.show()
"""

# FAKÜLTE BAZLI PER CHANGE GRAFİKLERİ
"""
columns_1 = ['Faculty Name', 'Year', 'Total Male Number Change (%)', 'Total Female Number Change (%)', 'Total Student Number Change (%)']
columns_2 = ['Faculty Name', 'Year', 'Exchange to Abroad Change (%)', 'Exchange from Abroad Change (%)']
columns_3 = ['Faculty Name', 'Year', 'Professors Change (%)', 'Assoc Prof Change (%)', 'Phd Change (%)', 'Quota Change (%)', 'Placed Number Change (%)']
columns_5 = ['Faculty Name', 'Year', 'Marmara Change (%)', 'Aegean Change (%)', 'Mediterranean Change (%)', 'Black Sea Change (%)', 'Central Anatolia Change (%)', 'Eastern Anatolia Change (%)', 'Southeastern Anatolia Change (%)']

# Filter data based on the selected columns
data_1 = df_fac_change[columns_1].dropna(subset=['Total Male Number Change (%)', 'Total Female Number Change (%)', 'Total Student Number Change (%)'])
data_2 = df_fac_change[columns_2].dropna(subset=['Exchange to Abroad Change (%)', 'Exchange from Abroad Change (%)'])
data_3 = df_fac_change[columns_3].dropna(subset=['Professors Change (%)', 'Assoc Prof Change (%)', 'Phd Change (%)', 'Quota Change (%)', 'Placed Number Change (%)'])
data_5 = df_fac_change[columns_5].dropna(subset=['Marmara Change (%)', 'Aegean Change (%)', 'Mediterranean Change (%)', 'Black Sea Change (%)', 'Central Anatolia Change (%)', 'Eastern Anatolia Change (%)', 'Southeastern Anatolia Change (%)'])

# Average for Academician change
data_3['Academician Change (%)'] = data_3[['Professors Change (%)', 'Assoc Prof Change (%)', 'Phd Change (%)']].mean(axis=1)
# First Graph: Total Male Number Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Total Male Number Change (%)", hue="Year", data=data_1, ci=None)
plt.title('Total Male Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Second Graph: Total Female Number Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Total Female Number Change (%)", hue="Year", data=data_1, ci=None)
plt.title('Total Female Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Third Graph: Total Student Number Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Total Student Number Change (%)", hue="Year", data=data_1, ci=None)
plt.title('Total Student Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Fourth Graph: Exchange to Abroad Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Exchange to Abroad Change (%)", hue="Year", data=data_2, ci=None)
plt.title('Exchange to Abroad Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Fifth Graph: Exchange from Abroad Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Exchange from Abroad Change (%)", hue="Year", data=data_2, ci=None)
plt.title('Exchange from Abroad Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Sixth Graph: Academician Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Academician Change (%)", hue="Year", data=data_3, ci=None)
plt.title('Academician Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Seventh Graph: Quota Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Quota Change (%)", hue="Year", data=data_3, ci=None)
plt.title('Quota Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Eighth Graph: Placed Number Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Placed Number Change (%)", hue="Year", data=data_3, ci=None)
plt.title('Placed Number Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Ninth Graph: Marmara Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Marmara Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Marmara Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Tenth Graph: Aegean Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Aegean Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Aegean Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Eleventh Graph: Mediterranean Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Mediterranean Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Mediterranean Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Twelfth Graph: Black Sea Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Black Sea Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Black Sea Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Thirteenth Graph: Central Anatolia Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Central Anatolia Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Central Anatolia Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Fourteenth Graph: Eastern Anatolia Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Eastern Anatolia Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Eastern Anatolia Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()

# Fifteenth Graph: Southeastern Anatolia Change (%)
plt.figure(figsize=(12, 8))
sns.barplot(x="Faculty Name", y="Southeastern Anatolia Change (%)", hue="Year", data=data_5, ci=None)
plt.title('Southeastern Anatolia Region Enrollment Change by Faculty')
plt.xticks(rotation=90)
plt.ylabel('Change (%)')
plt.xlabel('Faculty')
plt.legend(title="Year")
plt.grid(True)
plt.show()
"""

# fakülte toplam cinsiyet grafiiği
"""
faculty_yearly_data_updated = df.groupby(['Faculty Name', 'Year'])[['Total Male Number', 'Total Female Number']].sum().reset_index()

# Pivot the data to have years as columns for each faculty
faculty_yearly_pivot_updated = faculty_yearly_data_updated.pivot(index='Faculty Name', columns='Year', values=['Total Male Number', 'Total Female Number'])

# Plotting the bar chart with space between the faculties
fig, ax = plt.subplots(figsize=(12, 8))

# Set the width for each bar and space between faculties
bar_width = 0.25
index = range(len(faculty_yearly_pivot_updated))

# Plotting the bars for each year, adjusting the position to place them next to each other
for i, year in enumerate(faculty_yearly_pivot_updated.columns.levels[1]):
    male_column = ('Total Male Number', year)
    female_column = ('Total Female Number', year)
    ax.bar([x + bar_width * i + (bar_width * 2) for x in index], faculty_yearly_pivot_updated[male_column] + faculty_yearly_pivot_updated[female_column],
           width=bar_width, label=f'Year {year}')

ax.set_xlabel('Faculty')
ax.set_ylabel('Total Number of Students')
ax.set_title('Total Number of Students by Faculty and Year')
ax.set_xticks([x + bar_width * 1.5 for x in index])  # Adjust the x-ticks to center the bars with space
ax.set_xticklabels(faculty_yearly_pivot_updated.index, rotation=90)
ax.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
"""


# akademisyen öğrenci oranı hesaplama
def calculate_academician_student_ratio(data, group_by_columns=['Year']):
    # Adding a new column 'Academician Number' by summing Professors, PhD, and Associate Professors
    data['Academician Number'] = data['Professors'] + data['Phd'] + data['Assoc Prof']

    # Grouping the data by the specified columns (default is 'Year')
    yearly_data = data.groupby(group_by_columns).agg({
        'Academician Number': 'sum',  # Sum of academicians per group
        'Total Student Number': 'sum'  # Sum of students per group
    }).reset_index()

    # Calculating the number of students per academician for each group
    yearly_data['Students per Academician'] = yearly_data['Total Student Number'] / yearly_data['Academician Number']

    # Print the result to the console
    print(yearly_data)

    # Plotting the bar chart for 'Students per Academician'
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotting the bars
    ax.bar(yearly_data[yearly_data.columns[0]], yearly_data['Students per Academician'], color='teal')

    # Setting the x-ticks to be integers
    ax.set_xticks(yearly_data[yearly_data.columns[0]])
    ax.set_xticklabels(yearly_data[yearly_data.columns[0]].astype(int), rotation=90)

    ax.set_xlabel(group_by_columns[0])
    ax.set_ylabel('Students per Academician')
    ax.set_title('Students per Academician Ratio')

    plt.tight_layout()
    plt.show()

    return yearly_data


# result = calculate_academician_student_ratio(df)

def plot_students_per_academician_by_year(data):
    # Adding a new column 'Academician Number' by summing Professors, PhD, and Associate Professors
    data['Academician Number'] = data['Professors'] + data['Phd'] + data['Assoc Prof']

    # Grouping the data by 'Faculty Name' and 'Year'
    yearly_data = data.groupby(['Faculty Name', 'Year']).agg({
        'Academician Number': 'sum',  # Sum of academicians per group
        'Total Student Number': 'sum'  # Sum of students per group
    }).reset_index()

    # Calculating the number of students per academician for each group
    yearly_data['Students per Academician'] = yearly_data['Total Student Number'] / yearly_data['Academician Number']

    # Plotting separate bar charts for each year
    years = [2021, 2022, 2023, 2024]

    for year in years:
        fig, ax = plt.subplots(figsize=(12, 8))

        # Filter the data for the current year
        year_data = yearly_data[yearly_data['Year'] == year]

        # Plotting the bars for the students per academician for the current year
        ax.bar(year_data['Faculty Name'], year_data['Students per Academician'], color='teal')

        # Set labels and title
        ax.set_xlabel('Faculty')
        ax.set_ylabel('Students per Academician')
        ax.set_title(f'Students per Academician Ratio in {year}')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.show()


# Run the function to plot the charts for each year
# plot_students_per_academician_by_year(df)

# Revised function to include department names on the x-axis and exclude AYT Math
# Function to calculate average yearly changes and display them with department names on the x-axis
# Function to calculate average yearly changes and ensure department names on x-axis


print(df.columns)

#### 30.12.2024
# net gelişimi

# Final correction: Retain and properly align Department Names during calculations
def calculate_and_display_changes_final_fixed(group_type, subjects, title):
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

# Test the corrected function for SAY departments
calculate_and_display_changes_final_fixed(
    "SAY",
    ['AYT Biology', 'AYT Physics', 'AYT Chemistry'],
    "Average Yearly Score Changes for SAY Departments"
)
# EA Departments
calculate_and_display_changes_final_fixed(
    "EA",
    ['AYT Literature', 'AYT History1', 'AYT Geography1'],
    "Average Yearly Score Changes for EA Departments"
)

# SÖZ Departments
calculate_and_display_changes_final_fixed(
    "SÖZ",
    ['AYT Literature', 'AYT Geography1', 'AYT Geography2', 'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2'],
    "Average Yearly Score Changes for SÖZ Departments"
)

# DİL Departments
calculate_and_display_changes_final_fixed(
    "DİL",
    ['YDT Foreign Language'],
    "Average Yearly Score Changes for DİL Departments"
)