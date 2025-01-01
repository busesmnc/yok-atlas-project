import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


csv_file_path = "YTU_General_Data.csv"

df = pd.read_csv(csv_file_path)

# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.1. Success Order Analysis: function for: Question 10
# 10.2.3. Correct Answer Analysis: function for: Question 6
# 10.2.4. Gender Analysis: function for: Question 1
# 10.2.5. Quota, Student Number and Preferred Number Analysis: function for: Question 4
# 10.2.7. Exchange Program Analysis function for: Question 4


def analyze_department_data(data_frame, analysis_type):
    """
    Performs various analyses on department data based on the specified analysis type.
    This version includes updated exchange analysis with participation percentages.

    Parameters:
    - data_frame: Pandas DataFrame containing the dataset.
    - analysis_type: Type of analysis to perform (e.g., "gender", "success_order",
                     "exchange", "preferred_number", "tyt").

    Returns:
    - Displays appropriate plots based on the analysis type.
    """
    # Filter out TRNC Citizens rows
    filtered_data = data_frame[~data_frame['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

    # Identify language and base department
    filtered_data['Language'] = filtered_data['Department Name'].apply(
        lambda x: 'English' if '(English)' in x else 'Turkish'
    )
    filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

    # Keep only departments with both Turkish and English versions
    valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)

    # Perform analysis based on the specified type
    if analysis_type == "exchange":
        erasmus_percentage_summary = valid_departments.groupby('Language').agg(
            Total_Exchange_to_Abroad=('Exchange to Abroad', 'sum'),
            Total_Exchange_from_Abroad=('Exchange from Abroad', 'sum'),
            Total_Students=('Total Student Number', 'sum')
        ).reset_index()

        erasmus_percentage_summary['Percentage_Exchange_to_Abroad'] = (
                                                                              erasmus_percentage_summary[
                                                                                  'Total_Exchange_to_Abroad'] /
                                                                              erasmus_percentage_summary[
                                                                                  'Total_Students']
                                                                      ) * 100
        erasmus_percentage_summary['Percentage_Exchange_from_Abroad'] = (
                                                                                erasmus_percentage_summary[
                                                                                    'Total_Exchange_from_Abroad'] /
                                                                                erasmus_percentage_summary[
                                                                                    'Total_Students']
                                                                        ) * 100

        erasmus_percentage_summary.plot(
            kind='bar',
            x='Language',
            y=['Percentage_Exchange_to_Abroad', 'Percentage_Exchange_from_Abroad'],
            stacked=False,
            figsize=(10, 6),
            color=['blue', 'green']
        )
        plt.title("Erasmus Participation Percentage: Turkish vs English Departments")
        plt.ylabel("Percentage (%)")
        plt.xlabel("Department Language")
        plt.xticks(rotation=0)
        plt.legend(title="Exchange Type")
        plt.tight_layout()
        plt.show()

    elif analysis_type == "gender":
        gender_data = valid_departments[['Base_Department', 'Language', 'Male', 'Female']].dropna()

        # Calculate percentages
        gender_data['Male_Percentage'] = gender_data['Male'] / (gender_data['Male'] + gender_data['Female']) * 100
        gender_data['Female_Percentage'] = gender_data['Female'] / (gender_data['Male'] + gender_data['Female']) * 100

        # Create percentage comparison bar chart
        percentage_data = gender_data.groupby('Language')[['Male_Percentage', 'Female_Percentage']].mean().reset_index()
        percentage_data.plot(x='Language', kind='bar', stacked=True, figsize=(10, 6), color=['orange', 'red'])
        plt.title('Gender Percentage Comparison: Turkish vs English Departments')
        plt.ylabel('Percentage (%)')
        plt.xticks(rotation=0)
        plt.legend(title='Gender')
        plt.tight_layout()
        plt.show()

        # Create total number comparison bar chart
        total_data = gender_data.groupby('Language')[['Male', 'Female']].sum().reset_index()
        total_data.plot(x='Language', kind='bar', figsize=(10, 6), color=['orange', 'red'])
        plt.title('Total Gender Numbers: Turkish vs English Departments')
        plt.ylabel('Total Number')
        plt.xticks(rotation=0)
        plt.legend(title='Gender', labels=['Total Male', 'Total Female'])
        plt.tight_layout()
        plt.show()

    elif analysis_type == "success_order":
        success_order_data = valid_departments[['Base_Department', 'Language', 'Success Order']].dropna()
        success_order_data['Success Order'] = pd.to_numeric(success_order_data['Success Order'], errors='coerce')

        plt.figure(figsize=(10, 6))
        success_order_data.boxplot(by='Language', column=['Success Order'], grid=False)
        plt.title('Comparison of Success Order Between English and Turkish Departments')
        plt.suptitle('')
        plt.xlabel('Language')
        plt.ylabel('Success Order (Lower is Better)')
        plt.xticks([1, 2], ['English', 'Turkish'])
        plt.show()

    elif analysis_type == "preferred_number":
        preferred_data = valid_departments[['Base_Department', 'Language', 'Preferred number']].dropna()
        preferred_data['Preferred number'] = pd.to_numeric(preferred_data['Preferred number'], errors='coerce')

        plt.figure(figsize=(10, 6))
        preferred_data.boxplot(by='Language', column=['Preferred number'], grid=False)
        plt.title('Comparison of Preferred Numbers Between English and Turkish Departments')
        plt.suptitle('')
        plt.xlabel('Language')
        plt.ylabel('Preferred Number')
        plt.xticks([1, 2], ['English', 'Turkish'])
        plt.show()

    elif analysis_type == "tyt":
        tyt_data = valid_departments[['Base_Department', 'Language', 'Total Correct TYT']].dropna()
        tyt_data['Total Correct TYT'] = pd.to_numeric(tyt_data['Total Correct TYT'], errors='coerce')

        plt.figure(figsize=(10, 6))
        tyt_data.boxplot(by='Language', column=['Total Correct TYT'], grid=False)
        plt.title('Comparison of Total Correct TYT Between English and Turkish Departments')
        plt.suptitle('')
        plt.xlabel('Language')
        plt.ylabel('Total Correct TYT')
        plt.xticks([1, 2], ['English', 'Turkish'])
        plt.show()

    else:
        raise ValueError(
            "Invalid analysis type. Choose from 'gender', 'success_order', 'exchange', 'preferred_number', 'tyt'.")


analyze_department_data(df, "success_order")
analyze_department_data(df, "tyt")
analyze_department_data(df, "gender")
analyze_department_data(df, "preferred_number")
analyze_department_data(df, "exchange")
# ----------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# 10.2.1. Success Order Analysis: function for: Question 11
# 10.2.7. Exchange Program Analysis function for: Question 5

def combined_analysis_fixed(data_frame, analysis_type):
    """
    Performs combined analyses for success order, gender distribution, exchange participation,
    correlation matrix, and total student representation based on the specified analysis type.

    Parameters:
    - data_frame: Pandas DataFrame containing the dataset.
    - analysis_type: Type of analysis to perform (e.g., "success_order", "exchange").

    Returns:
    - Visualizations based on the analysis type.
    """

    field_categories = {
        "Engineering": ["Engineering", "Mechatronics", "Automation"],
        "Sciences": ["Mathematical", "Chemistry", "Bioengineering", "Physics", "Statistics", "Mathematics",
                     "Molecular Biology"],
        "Education": ["Education", "Teaching", "Language", "Guidance", "Preschool", "Primary"],
        "Other": ["Architecture", "Design", "Political Science", "Relations", "Communication"]
    }

    # Categorize departments into fields
    def categorize_department(department):
        for field, keywords in field_categories.items():
            if any(keyword in department for keyword in keywords):
                return field
        return "Other"

    if analysis_type == "success_order":
        filtered_data = data_frame[data_frame['Year'] == 2024].copy()  # Create a deep copy
        filtered_data.loc[:, 'Field'] = filtered_data['Department Name'].apply(categorize_department)

        # Select relevant columns and clean data
        success_order_data = filtered_data[['Field', 'Success Order']].dropna()
        success_order_data['Success Order'] = pd.to_numeric(success_order_data['Success Order'], errors='coerce')
        success_order_data = success_order_data.dropna()

        # Create box plot for success order by field
        plt.figure(figsize=(12, 6))
        boxplot = success_order_data.boxplot(by='Field', column=['Success Order'], grid=False, return_type='dict')
        plt.title('Comparison of Success Order Across Fields (Filtered for 2024)')
        plt.suptitle('')
        plt.xlabel('Field')
        plt.ylabel('Success Order (Lower is Better)')

        # Calculate and overlay mean values
        group_means = success_order_data.groupby('Field')['Success Order'].mean()
        for i, group in enumerate(group_means.index, start=1):
            plt.scatter(i, group_means[group], color='red', label='Mean' if i == 1 else '')

        plt.legend(loc='upper right')
        plt.xticks(range(1, len(group_means.index) + 1), group_means.index)
        plt.tight_layout()
        plt.show()

    elif analysis_type == "exchange":
        filtered_data = data_frame[data_frame['Year'] != 2024].copy()  # Create a deep copy to avoid the warning
        filtered_data.loc[:, 'Field'] = filtered_data['Department Name'].apply(categorize_department)

        # Calculate exchange participation as a percentage of total students
        exchange_summary = filtered_data.groupby('Field').agg(
            Total_Exchange_to_Abroad=('Exchange to Abroad', 'sum'),
            Total_Exchange_from_Abroad=('Exchange from Abroad', 'sum'),
            Total_Students=('Total Student Number', 'sum')
        ).reset_index()

        exchange_summary['Percentage_Exchange_to_Abroad'] = (
            exchange_summary['Total_Exchange_to_Abroad'] / exchange_summary['Total_Students'] * 100
        )
        exchange_summary['Percentage_Exchange_from_Abroad'] = (
            exchange_summary['Total_Exchange_from_Abroad'] / exchange_summary['Total_Students'] * 100
        )

        # Calculate average exchange numbers
        avg_exchange_summary = filtered_data.groupby('Field').agg(
            Avg_Exchange_to_Abroad=('Exchange to Abroad', 'mean'),
            Avg_Exchange_from_Abroad=('Exchange from Abroad', 'mean')
        ).reset_index()

        # Create bar plot for exchange participation percentages
        exchange_summary.plot(
            kind='bar',
            x='Field',
            y=['Percentage_Exchange_to_Abroad', 'Percentage_Exchange_from_Abroad'],
            stacked=False,
            figsize=(10, 6),
            color=['orange', 'red']
        )
        plt.title("Percentage of Exchange Students by Academic Field")
        plt.ylabel("Percentage (%)")
        plt.xlabel("Academic Field")
        plt.xticks(rotation=0)
        plt.legend(title="Exchange Type")
        plt.tight_layout()
        plt.show()

        # Create bar plot for average exchange numbers
        avg_exchange_summary.plot(
            kind='bar',
            x='Field',
            y=['Avg_Exchange_to_Abroad', 'Avg_Exchange_from_Abroad'],
            stacked=False,
            figsize=(10, 6),
            color=['orange', 'red']
        )
        plt.title("Average Exchange Numbers by Academic Field")
        plt.ylabel("Average Number")
        plt.xlabel("Academic Field")
        plt.xticks(rotation=0)
        plt.legend(title="Exchange Type")
        plt.tight_layout()
        plt.show()


combined_analysis_fixed(df, "success_order")
combined_analysis_fixed(df, "exchange")
# ----------------------------------------------------------------------------------------------------------------- #
