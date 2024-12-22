import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
import seaborn as sns
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


def check_df(dataframe, head=5):
    print("--------- shape -------------")
    print(df.shape)
    print("--------- types -------------")
    print(dataframe.dtypes)
    print("--------- head -------------")
    print(dataframe.head(head))
    print("--------- tail -------------")
    print(dataframe.tail(head))
    print("--------- na -------------")
    print(dataframe.isnull().sum())


def grab_col_names(dataframe, cat_th=10, car_th=20):
    """

    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.
    Not: Kategorik değişkenlerin içerisine numerik görünümlü kategorik değişkenler de dahildir.

    Parameters
    ------
        dataframe: dataframe
                Değişken isimleri alınmak istenilen dataframe
        cat_th: int, optional
                numerik fakat kategorik olan değişkenler için sınıf eşik değeri
        car_th: int, optional
                kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    ------
        cat_cols: list
                Kategorik değişken listesi
        num_cols: list
                Numerik değişken listesi
        cat_but_car: list
                Kategorik görünümlü kardinal değişken listesi

    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))


    Notes
    ------
        cat_cols + num_cols + cat_but_car = toplam değişken sayısı
        num_but_cat cat_cols'un içerisinde.

    """
    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    return cat_cols, num_cols, cat_but_car


# cat_cols, num_cols, cat_but_car = grab_col_names(df2)
numeric_cols = ['Male', 'Female', 'Total Male Number', 'Total Female Number', 'Total Student Number',
                'Exchange to Abroad', 'Exchange from Abroad', 'Professors', 'Assoc Prof', 'Phd', 'Base Point',
                'Success Order', 'Preferred number', 'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT',
                'Total Correct YDT', 'TYT Turkish', 'TYT Math', 'TYT Science', 'TYT Social Science', 'AYT Math',
                'AYT Physics', 'AYT Chemistry', 'AYT Biology', 'AYT Literature', 'AYT Geography1', 'AYT Geography2',
                'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2', 'YDT Foreign Language', 'Marmara',
                'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']


def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist(bins=20)
        plt.xlabel(numerical_col.replace('_', ' ').capitalize())
        plt.title(numerical_col.replace('_', ' ').capitalize())
        plt.show()


# print(num_summary(df2, "success_order", plot=True))

# for col in numeric_cols:
#     num_summary(df2, col, plot=True)


def target_summary_with_num(dataframe, target, numerical_col, year):
    print(f"year: {year} için {numerical_col} ortalamaları")
    filtered_df = dataframe[dataframe["year"] == year]  # Filter dataframe by year
    print(filtered_df.groupby(target).agg({numerical_col: "sum"}), end="\n\n\n")


def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        print(dataframe[col_name])
    return low_limit, up_limit


# for col in numeric_cols:
#     print(col)
#     check_outlier(df2, col)


def department_analysis(data, group_by='Department Name', department_type=None, Year=None):
    columns_to_analyze = ['Male', 'Female', 'Total Male Number', 'Total Female Number', 'Total Student Number',
                'Exchange to Abroad', 'Exchange from Abroad', 'Professors', 'Assoc Prof', 'Phd', 'Base Point',
                'Success Order', 'Preferred number', 'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT',
                'Total Correct YDT', 'TYT Turkish', 'TYT Math', 'TYT Science', 'TYT Social Science', 'AYT Math',
                'AYT Physics', 'AYT Chemistry', 'AYT Biology', 'AYT Literature', 'AYT Geography1', 'AYT Geography2',
                'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2', 'YDT Foreign Language', 'Marmara',
                'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']

    # group_by string ise listeye çevir
    if isinstance(group_by, str):
        group_by = [group_by]

    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8').upper()

    # Department type filtresi
    if department_type:
        normalized_department_type = normalize_string(department_type)
        data = data[data['Department Type'].apply(lambda x: normalize_string(x) == normalized_department_type)].copy()

    # Veriyi sıralayıp, geçmiş yıl verilerini de hesaba katacak şekilde pct_change hesaplamak
    filtered_data = data.copy()

    # Yeni bir DataFrame oluştur
    analysis_data = filtered_data.loc[:, :]  # Tüm satır ve sütunları seçer

    # Kullanıcıdan analiz yapmak istediği sütunları almak
    print("Sorgulamak istediğiniz sütunları seçin. Mevcut sütunlar:")
    for idx, col in enumerate(columns_to_analyze, 1):
        print(f"{idx}. {col}")

    user_input = input("Sorgulamak istediğiniz sütun numaralarını girin (virgülle ayırarak, örn. 1,2) ya da 0 girerek"
                       " tüm sütunları seçebilirsiniz: ")

    # Kullanıcının girdisini işleme
    if user_input == '0':
        selected_columns = columns_to_analyze  # Tüm sütunları seç
    else:
        selected_columns = [columns_to_analyze[int(i) - 1] for i in user_input.split(',') if i.strip().isdigit()]

    for col in selected_columns:
        # Geçmiş yıl verisini kullanarak yüzdelik değişim hesaplama
        analysis_data[f'{col} Change (%)'] = analysis_data.groupby(group_by)[col].pct_change() * 100

    # Yıl filtreleme (year parametresinin kontrolü ve dönüştürülmesi)
    if Year:
        # Ensure 'year' column is in numeric format (int)
        analysis_data['Year'] = pd.to_numeric(analysis_data['Year'], errors='coerce')

        # Yıl filtresi uygulanmadan önce verinin sıralanması
        analysis_data = analysis_data.sort_values(by=['Department Name', 'Year'])

        # Uygulanan yıl filtresi
        analysis_data = analysis_data[analysis_data['Year'] == Year]

    # Sonuçları döndürme
    selected_columns_with_change = ['Year'] + group_by + ['Department Type'] + [f'{col} Change (%)' for col in
                                                                                selected_columns]
    return analysis_data[selected_columns_with_change]


# dep_change = department_analysis(df)
# print(dep_change)
# dep_change.to_csv("ytu_department_yearly_per_change")

def faculty_analysis(data, faculty_name_column='Faculty Name', Year=None):
    # Gruplama ve hesaplamalar için gerekli sütunlar
    columns_to_analyze = ['Male', 'Female', 'Total Male Number', 'Total Female Number', 'Total Student Number',
                'Exchange to Abroad', 'Exchange from Abroad', 'Professors', 'Assoc Prof', 'Phd', 'Base Point',
                'Success Order', 'Preferred number', 'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT',
                'Total Correct YDT', 'TYT Turkish', 'TYT Math', 'TYT Science', 'TYT Social Science', 'AYT Math',
                'AYT Physics', 'AYT Chemistry', 'AYT Biology', 'AYT Literature', 'AYT Geography1', 'AYT Geography2',
                'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2', 'YDT Foreign Language', 'Marmara',
                'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']


    if isinstance(faculty_name_column, str):
        faculty_name_column = [faculty_name_column]

    aggregation_methods = {
        'Male': 'sum',
        'Female': 'sum',
        'Total Male Number': 'sum',
        'Total Female Number': 'sum',
        'Total Student Number': 'sum',
        'Exchange to Abroad': 'sum',
        'Exchange from Abroad': 'sum',
        'Professors': 'sum',
        'Assoc Prof': 'sum',
        'Phd': 'sum',
        'Base Point': 'mean',  # Average
        'Success Order': 'sum',
        'Preferred number': 'sum',
        'Quota': 'sum',
        'Placed Number': 'sum',
        'Total Correct TYT': 'mean',  # Average
        'Total Correct AYT': 'mean',
        'Total Correct YDT': 'mean',
        'TYT Turkish': 'mean',
        'TYT Math': 'mean',
        'TYT Science': 'mean',
        'TYT Social Science': 'mean',
        'AYT Math': 'mean',
        'AYT Physics': 'mean',
        'AYT Chemistry': 'mean',
        'AYT Biology': 'mean',
        'AYT Literature': 'mean',
        'AYT Geography1': 'mean',
        'AYT Geography2': 'mean',
        'AYT Religion': 'mean',
        'AYT Philosophy': 'mean',
        'AYT History1': 'mean',
        'AYT History2': 'mean',
        'YDT Foreign Language': 'mean',
        'Marmara': 'sum',
        'Aegean': 'sum',
        'Mediterranean': 'sum',
        'Black Sea': 'sum',
        'Central Anatolia': 'sum',
        'Eastern Anatolia': 'sum',
        'Southeastern Anatolia': 'sum'
    }

    # Fakülte ve yıl bazında gruplama yapma
    faculty_data = data.groupby(faculty_name_column + ['Year']).agg(aggregation_methods).reset_index()

    # Kullanıcıdan analiz yapmak istediği sütunları almak
    print("Sorgulamak istediğiniz sütunları seçin. Mevcut sütunlar:")
    for idx, col in enumerate(columns_to_analyze, 1):
        print(f"{idx}. {col}")

    user_input = input("Sorgulamak istediğiniz sütun numaralarını girin (virgülle ayırarak, örn. 1,2) ya da 0 girerek"
                       " tüm sütunları seçebilirsiniz: ")

    # Kullanıcının girdisini işleme
    if user_input == '0':
        selected_columns = columns_to_analyze  # Tüm sütunları seç
    else:
        selected_columns = [columns_to_analyze[int(i) - 1] for i in user_input.split(',') if i.strip().isdigit()]

    for col in selected_columns:
        if col in faculty_data.columns:
            faculty_data[f'{col} Change (%)'] = faculty_data.groupby(faculty_name_column)[col].pct_change() * 100

    change_columns = [f'{col} Change (%)' for col in columns_to_analyze]

    if Year:
        # Ensure 'year' column is in numeric format (int)
        faculty_data['Year'] = pd.to_numeric(faculty_data['Year'], errors='coerce')

        # Yıl filtresi uygulanmadan önce verinin sıralanması
        faculty_data = faculty_data.sort_values(by=['Faculty Name', 'Year'])

        # Uygulanan yıl filtresi
        faculty_data = faculty_data[faculty_data['year'] == Year]

    # Sonuçları döndürme
    selected_columns_with_change = ['Year'] + faculty_name_column + change_columns

    return faculty_data[selected_columns_with_change]


# fac_change = faculty_analysis(df)
# fac_change_year = fac_change[fac_change['Year'] != 2021]
# print(fac_change)
# fac_change.to_csv("yut_faculty_yearly_per_change.csv")


def year_analysis(data):

    columns_to_analyze = ['Male', 'Female', 'Total Male Number', 'Total Female Number', 'Total Student Number',
                'Exchange to Abroad', 'Exchange from Abroad', 'Professors', 'Assoc Prof', 'Phd', 'Base Point',
                'Success Order', 'Preferred number', 'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT',
                'Total Correct YDT', 'TYT Turkish', 'TYT Math', 'TYT Science', 'TYT Social Science', 'AYT Math',
                'AYT Physics', 'AYT Chemistry', 'AYT Biology', 'AYT Literature', 'AYT Geography1', 'AYT Geography2',
                'AYT Religion', 'AYT Philosophy', 'AYT History1', 'AYT History2', 'YDT Foreign Language', 'Marmara',
                'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']

    aggregation_methods = {
        'Male': 'sum',
        'Female': 'sum',
        'Total Male Number': 'sum',
        'Total Female Number': 'sum',
        'Total Student Number': 'sum',
        'Exchange to Abroad': 'sum',
        'Exchange from Abroad': 'sum',
        'Professors': 'sum',
        'Assoc Prof': 'sum',
        'Phd': 'sum',
        'Base Point': 'mean',  # Average
        'Success Order': 'sum',
        'Preferred number': 'sum',
        'Quota': 'sum',
        'Placed Number': 'sum',
        'Total Correct TYT': 'mean',  # Average
        'Total Correct AYT': 'mean',
        'Total Correct YDT': 'mean',
        'TYT Turkish': 'mean',
        'TYT Math': 'mean',
        'TYT Science': 'mean',
        'TYT Social Science': 'mean',
        'AYT Math': 'mean',
        'AYT Physics': 'mean',
        'AYT Chemistry': 'mean',
        'AYT Biology': 'mean',
        'AYT Literature': 'mean',
        'AYT Geography1': 'mean',
        'AYT Geography2': 'mean',
        'AYT Religion': 'mean',
        'AYT Philosophy': 'mean',
        'AYT History1': 'mean',
        'AYT History2': 'mean',
        'YDT Foreign Language': 'mean',
        'Marmara': 'sum',
        'Aegean': 'sum',
        'Mediterranean': 'sum',
        'Black Sea': 'sum',
        'Central Anatolia': 'sum',
        'Eastern Anatolia': 'sum',
        'Southeastern Anatolia': 'sum'
    }

    year_data = data.groupby(['Year']).agg(aggregation_methods).reset_index()

    for col in columns_to_analyze:
        if col in year_data.columns:
            year_data[f'{col} Change (%)'] = year_data[col].pct_change() * 100

    # Yıl ve yüzdelik değişimle gösterilecek sütunları seçme
    change_columns = [f'{col} Change (%)' for col in columns_to_analyze]

    # Sonuçları döndürme
    selected_columns_with_change = ['Year'] + change_columns

    return year_data[selected_columns_with_change]

# Years = year_analysis(df)
# print(Years)
# Years.to_csv("ytu_yearly_per_change.csv", index=False)

def plot_yearly_trend_handling_missing(data, metric, group_column='Department Name', top_n=10):
    """
    Plots yearly trends for exactly `top_n` groups, handling missing data gracefully.

    Parameters:
    - data: DataFrame containing the data to analyze.
    - metric: The column name of the metric to plot (e.g., 'base_point Change (%)').
    - group_column: The column to group by (e.g., 'department_name', 'faculty_name', 'university_name').
    - top_n: Number of top and bottom groups to include in the plot.

    Returns:
    - None: Displays the plots.
    """
    # Analyze data by years for the specified metric
    yearly_analysis = data.groupby(['Year', group_column])[metric].mean().unstack()

    # Dynamically determine top and bottom groups based on maximum change
    group_max_change = data.groupby(group_column)[metric].max()
    top_groups = [group for group in group_max_change.nlargest(top_n).index if group in yearly_analysis.columns]
    bottom_groups = [group for group in group_max_change.nsmallest(top_n).index if group in yearly_analysis.columns]

    # Clean up metric and group names
    metric_cleaned = metric.replace('_', ' ').capitalize()

    # Plotting yearly trend for top groups
    plt.figure(figsize=(12, 6))
    for group in top_groups:
        plt.plot(yearly_analysis.index, yearly_analysis[group], marker='o', label=group)

    plt.title(f'Yearly Trend for Top {top_n} {group_column.replace("_", " ").title()}s with the Largest Increase ({metric_cleaned})')
    plt.xlabel('Year')
    plt.ylabel(metric_cleaned)
    plt.xticks(yearly_analysis.index)  # Set x-axis to show only integer years
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plotting yearly trend for bottom groups
    plt.figure(figsize=(12, 6))
    for group in bottom_groups:
        plt.plot(yearly_analysis.index, yearly_analysis[group], marker='o', label=group)

    plt.title(f'Yearly Trend for Top {top_n} {group_column.replace("_", " ").title()}s with the Largest Decrease ({metric_cleaned})')
    plt.xlabel('Year')
    plt.ylabel(metric_cleaned)
    plt.xticks(yearly_analysis.index)  # Set x-axis to show only integer years
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# plot_yearly_trend_handling_missing(df2, metric='Exchange to Abroad')


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

"""
 analyze_and_plot_regional_distribution(df2, region_columns= ['Marmara',
                 'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia',
                                                              'Southeastern Anatolia'])
"""


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

"""
# Apply the function with the correct column name and updated formatting
try:
    analyze_and_visualize_performance(df2, column='Total Correct AYT', top_n=5)
except ValueError as e:
    print(e)
"""


def analyze_base_point_correlations(data):
    """
    Analyze the correlations between base points and influencing factors.

    Args:
        data (pd.DataFrame): The dataset containing base points and potential influencing factors.

    Returns:
        pd.DataFrame: Correlation matrix of factors influencing base points.
    """
    factors = ['Base Point', 'Success Order', 'Preferred number', 'Marmara',
                'Aegean', 'Mediterranean', 'Black Sea', 'Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia']
    correlation_matrix = data[factors].corr()
    print("Correlation Matrix for Base Points:")
    print(correlation_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Base Points and Influencing Factors')
    plt.show()

    return correlation_matrix


# analyze_base_point_correlations(df2)


def analyze_by_department_type(data, columns):
    """
    Analyzes gender-based performance trends by department type.

    Parameters:
        data (DataFrame): The dataset containing performance and gender columns.
        columns (list): List of performance metric columns to analyze.

    Returns:
        None: Displays visualizations.
    """
    # Group data by department type and calculate average scores and gender distribution
    department_type_analysis = data.groupby('Department Type').agg(
        total_male=('Male', 'sum'),
        total_female=('Female', 'sum'),
        **{f'avg_{col}': (col, 'mean') for col in columns}
    ).reset_index()

    # Calculate total students and gender percentages
    department_type_analysis['total_students'] = (
        department_type_analysis['total_male'] + department_type_analysis['total_female']
    )
    department_type_analysis['male_percentage'] = (
        department_type_analysis['total_male'] / department_type_analysis['total_students'] * 100
    )
    department_type_analysis['female_percentage'] = (
        department_type_analysis['total_female'] / department_type_analysis['total_students'] * 100
    )

    # Visualize performance trends for each metric by department type
    for col in columns:
        col_avg = f'avg_{col}'
        fig, ax = plt.subplots(figsize=(10, 6))
        bars_male = ax.bar(department_type_analysis['Department Type'],
                           department_type_analysis['male_percentage'],
                           label='Male %', alpha=0.7)
        bars_female = ax.bar(department_type_analysis['Department Type'],
                             department_type_analysis['female_percentage'],
                             bottom=department_type_analysis['male_percentage'],
                             label='Female %', alpha=0.7)

        ax.set_title(f"Gender Representation and {col.replace('_', ' ').capitalize()} by Department Type")
        ax.set_xlabel("Department Type")
        ax.set_ylabel("Percentage and Average Scores")
        ax.legend()

        # Display numerical values on the bars
        for bar in bars_male + bars_female:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2),
                            ha='center', va='center', fontsize=10, color='white')

        plt.tight_layout()
        plt.show()


#columns_to_analyze_by_type = ['Total Correct TYT', 'Total Correct AYT', 'Total Correct YDT']
# analyze_by_department_type(df, columns_to_analyze_by_type)


def plot_beyond_exchange_factors(data, factors, target='Exchange to Abroad'):
    """
    Plots the correlation of factors beyond exchange program participation with preferences.

    Parameters:
        data (DataFrame): The dataset containing the factors and target column.
        factors (list): List of factor column names to analyze.
        target (str): The target column name for preferences (default: 'preferred').

    Returns:
        None: Displays a bar chart of the correlations.
    """
    # Calculate correlations with the target column
    correlations = data[factors + [target]].corr()[target].sort_values(ascending=False)

    # Plot the correlations
    plt.figure(figsize=(10, 6))
    correlations.drop(target).rename(index=lambda x: x.replace('_', ' ')).plot(
        kind='bar', color='skyblue', alpha=0.8
    )
    plt.title(f"Correlation of Factors Beyond Exchange Programs with {target.capitalize()}")
    plt.xlabel("Factors")
    plt.ylabel(f"Correlation with {target.capitalize()}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


factors_beyond_exchange = ['Professors', 'Assoc Prof', 'Phd', 'Base Point', 'Success Order', 'Preferred number',
                           'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT']

# plot_beyond_exchange_factors(df, factors_beyond_exchange)


# OUTLIER CHECK
"""
# Function to get rows with outliers for each column
df_dep_change.fillna(0, inplace=True)


# Function to detect outliers using the IQR method
def detect_outliers_iqr(data, column):
    # Detects outliers in a column using the IQR method
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

# Function to check for outliers in all numeric columns
def check_outliers_in_all_columns(data):
   Checks for outliers in all numeric columns and returns a summary.
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    outlier_summary = {}
    for column in numeric_columns:
        outliers = detect_outliers_iqr(data, column)
        outlier_summary[column] = len(outliers)
    return outlier_summary

# Apply the outlier detection to the dataset
outlier_summary = check_outliers_in_all_columns(df_dep_change)

# Display the outlier summary
def get_outliers_by_row(data):
   Returns a dictionary with column names as keys and rows with outliers as values.
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    outliers_by_column = {}
    for column in numeric_columns:
        outliers = detect_outliers_iqr(data, column)
        outliers_by_column[column] = outliers.index.tolist()
    return outliers_by_column

# Get rows with outliers for each column
outliers_by_row = get_outliers_by_row(df_dep_change)

# Convert to a DataFrame for easier viewing
outliers_by_row_df = pd.DataFrame(
    [(col, rows) for col, rows in outliers_by_row.items() if rows],
    columns=["Column", "Rows with Outliers"]
)


# print(outliers_by_row_df)

# Highlighting rows with extreme values (outliers)
# Create a copy of the dataset for highlighting
highlighted_data = df_dep_change.copy()

# Mark rows with outliers
for column, rows in outliers_by_row.items():
    highlighted_data.loc[rows, column] = "OUTLIER"

# Display rows with extreme values
extreme_rows = highlighted_data[highlighted_data.isin(["OUTLIER"]).any(axis=1)]

# Display the highlighted rows
extreme_rows.reset_index(inplace=True)
# print(extreme_rows)

# print(df_dep_change)


import plotly.express as px
import plotly.graph_objects as go

# Filter out data for the years 2021 and 2024
filtered_data = df_dep_change[(df_dep_change["Year"] != 2021) & (df_dep_change["Year"] != 2024)]

# Select numeric columns
filtered_numeric_data = filtered_data.select_dtypes(include=[np.number])

# Redo outlier detection for filtered data
filtered_outliers_by_row = get_outliers_by_row(filtered_numeric_data)

# Heatmap for filtered data
filtered_heatmap_data = filtered_numeric_data.copy()
for column, rows in filtered_outliers_by_row.items():
    filtered_heatmap_data[column] = 0  # Default to non-outlier
    filtered_heatmap_data.loc[rows, column] = 1  # Mark outliers as 1

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    filtered_heatmap_data.T,
    cmap="Reds",
    cbar=True,
    linewidths=0.5,
    linecolor='gray',
    yticklabels=True
)
plt.title("Outlier Heatmap (Excluding 2021 and 2024)", fontsize=16)
plt.xlabel("Row Index", fontsize=12)
plt.ylabel("Columns", fontsize=12)
plt.tight_layout()
plt.show()

# Count the number of outliers for each column in filtered data
filtered_outlier_counts = {col: len(rows) for col, rows in filtered_outliers_by_row.items()}

# Convert to DataFrame and sort by the number of outliers
filtered_outlier_counts_df = pd.DataFrame(
    list(filtered_outlier_counts.items()), columns=["Metric", "Number of Outliers"]
).sort_values(by="Number of Outliers", ascending=False)

# Display the top metrics with the most outliers in filtered data
print(filtered_outlier_counts_df.head(15))
"""


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


# Example usage of the extended function with highest subject print:
# i. SAY Departments: Comparison of AYT Math and AYT Biology scores over all years
# plot_department_analysis_with_highest_subjects(df, 'DİL', 'scores',
#                                                 subjects=['Total Correct TYT', 'Total Correct YDT'])

# plot_department_analysis_with_highest_subjects(df, 'EA', 'base_points')


def plot_department_analysis_with_highest_and_lowest_subjects_and_year(data, department_type, analysis_type,
                                                                       subjects=None, year=None):
    # Filter data based on department type
    filtered_data = data[data['Department Type'] == department_type]

    if year:
        # Filter by the specified year
        filtered_data = filtered_data[filtered_data['Year'] == year]

    if analysis_type == 'scores' and subjects:
        # Group by department and calculate mean scores for specified subjects
        score_data = filtered_data.groupby(['Department Name', 'Year'])[subjects].mean().reset_index()
        score_data_pivot = score_data.pivot(index='Department Name', columns='Year', values=subjects)

        # Plot
        if year:
            score_data_year = score_data[score_data['Year'] == year].set_index('Department Name')[subjects]
            score_data_year.plot(kind='bar', figsize=(10, 6))
            plt.title(f"{department_type} Departments: Comparison of {', '.join(subjects)} Scores for {year}")
        else:
            score_data_pivot.plot(kind='bar', figsize=(12, 6))
            plt.title(f"{department_type} Departments: Yearly Comparison of {', '.join(subjects)} Scores")

        plt.ylabel("Average Score")
        plt.xlabel("Department Name")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Subject")
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

        if year:
            # Calculate and plot data for a single year
            metric_data = filtered_data.groupby(['Department Name', 'Year'])[metric].mean().reset_index()
            metric_data_year = metric_data[metric_data['Year'] == year].set_index('Department Name')
            metric_data_year[metric].plot(kind='bar', figsize=(10, 6))
            plt.title(f"{department_type} Departments: Comparison of {metric} for {year}")
        else:
            metric_data_pivot = metric_data.pivot(index='Department Name', columns='Year', values=metric)
            metric_data_pivot.plot(kind='bar', figsize=(12, 6))
            plt.title(f"{department_type} Departments: Yearly Comparison of {metric}")

        plt.ylabel(f"Average {metric}")
        plt.xlabel("Department Name")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Year")
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


# Example usage of the extended function with year-aware highest and lowest subject print:
# SAY Departments: Comparison of AYT Math and AYT Biology scores over all years

# Adjust the function to position the legend outside the plot area


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


# EXCHANGE SUCCESS ORDER RELATION
"""
# Create bins for success order (e.g., high, medium, low success)
bin_labels = ['High Success', 'Medium Success', 'Low Success']
df['Success Category'] = pd.cut(
    df['Success Order'],
    bins=[-np.inf, df['Success Order'].quantile(0.33),
          df['Success Order'].quantile(0.66), np.inf],
    labels=bin_labels
)

# Calculate the average exchange participation for each success category
category_avg = df.groupby('Success Category')['Exchange to Abroad'].mean().reset_index()

# Plot the results
plt.figure(figsize=(10, 6))
plt.bar(category_avg['Success Category'], category_avg['Exchange to Abroad'], alpha=0.8)
plt.title('Exchange Program Participation by Success Category', fontsize=14)
plt.xlabel('Success Category', fontsize=12)
plt.ylabel('Average Exchange Program Participation (Exchange to Abroad)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
"""

# TR EN DEPARTMAN KARŞILAŞTIRMASI

# 1 success order
"""
# Adjusting the filter to use the correct column name
filtered_data = df[~df['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

# Identify pairs of departments with Turkish and English versions
filtered_data['Language'] = filtered_data['Department Name'].apply(
    lambda x: 'English' if '(English)' in x else 'Turkish'
)
filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

# Keep only departments that have both Turkish and English versions
valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)

# Extract success order for Turkish and English departments
success_order = valid_departments[['Base_Department', 'Language', 'Success Order']].dropna()

# Convert Success_Order to numeric if needed
success_order['Success Order'] = pd.to_numeric(success_order['Success Order'], errors='coerce')

# Box plot to compare success order for Turkish and English departments
plt.figure(figsize=(10, 6))
success_order.boxplot(by='Language', column=['Success Order'], grid=False)
plt.title('Comparison of Success Order Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Success Order (Lower is Better)')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()
"""

# 2 exchange to abroad
"""
filtered_data = df[~df['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

# Identify pairs of departments with Turkish and English versions
filtered_data['Language'] = filtered_data['Department Name'].apply(
    lambda x: 'English' if '(English)' in x else 'Turkish'
)
filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

# Keep only departments that have both Turkish and English versions
valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)
# Extract Erasmus participation data for the valid departments
erasmus_data = valid_departments[['Base_Department', 'Language', 'Exchange to Abroad']].dropna()

# Convert 'Exchange to Abroad' to numeric if needed
erasmus_data['Exchange to Abroad'] = pd.to_numeric(erasmus_data['Exchange to Abroad'], errors='coerce')

# Box plot to compare Erasmus participation for Turkish and English departments
plt.figure(figsize=(10, 6))
erasmus_data.boxplot(by='Language', column=['Exchange to Abroad'], grid=False)
plt.title('Comparison of Erasmus Participation Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Number of Students Participating in Erasmus')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()
"""

# 3 male female distr
"""

filtered_data = df[~df['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

# Identify pairs of departments with Turkish and English versions
filtered_data['Language'] = filtered_data['Department Name'].apply(
    lambda x: 'English' if '(English)' in x else 'Turkish'
)
filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

# Keep only departments that have both Turkish and English versions
valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)
# Extract Erasmus participation data for the valid departments
# Extract gender distribution data for the valid departments
gender_data = valid_departments[['Base_Department', 'Language', 'Male', 'Female']].dropna()

# Calculate the percentage of males and females for each department
gender_data['Male_Percentage'] = gender_data['Male'] / (gender_data['Male'] + gender_data['Female']) * 100
gender_data['Female_Percentage'] = gender_data['Female'] / (gender_data['Male'] + gender_data['Female']) * 100

# Box plot to compare male percentage between English and Turkish departments
plt.figure(figsize=(10, 6))
gender_data.boxplot(by='Language', column=['Male_Percentage'], grid=False)
plt.title('Comparison of Male Percentage Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Male Percentage (%)')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()

# Box plot to compare female percentage between English and Turkish departments
plt.figure(figsize=(10, 6))
gender_data.boxplot(by='Language', column=['Female_Percentage'], grid=False)
plt.title('Comparison of Female Percentage Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Female Percentage (%)')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()
"""

# 4 preferred number
"""

filtered_data = df[~df['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

# Identify pairs of departments with Turkish and English versions
filtered_data['Language'] = filtered_data['Department Name'].apply(
    lambda x: 'English' if '(English)' in x else 'Turkish'
)
filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

# Keep only departments that have both Turkish and English versions
valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)
# Extract Erasmus participation data for the valid departments
# Extract gender distribution data for the valid departments
# Extract preferred number data for the valid departments
preferred_data = valid_departments[['Base_Department', 'Language', 'Preferred number']].dropna()

# Convert 'Preferred number' to numeric if needed
preferred_data['Preferred number'] = pd.to_numeric(preferred_data['Preferred number'], errors='coerce')

# Box plot to compare preferred numbers between English and Turkish departments
plt.figure(figsize=(10, 6))
preferred_data.boxplot(by='Language', column=['Preferred number'], grid=False)
plt.title('Comparison of Preferred Numbers Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Preferred Number')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()
"""

# 5 TYT neti
"""
filtered_data = df[~df['Department Name'].str.contains(r'\(TRNC Citizens\)', na=False)]

# Identify pairs of departments with Turkish and English versions
filtered_data['Language'] = filtered_data['Department Name'].apply(
    lambda x: 'English' if '(English)' in x else 'Turkish'
)
filtered_data['Base_Department'] = filtered_data['Department Name'].str.replace(r' \(English\)', '', regex=True)

# Keep only departments that have both Turkish and English versions
valid_departments = filtered_data.groupby('Base_Department').filter(lambda x: x['Language'].nunique() == 2)
# Extract Erasmus participation data for the valid departments
# Extract gender distribution data for the valid department
# Extract Total Correct TYT data for the valid departments
tyt_data = valid_departments[['Base_Department', 'Language', 'Total Correct TYT']].dropna()

# Convert 'Total Correct TYT' to numeric if needed
tyt_data['Total Correct TYT'] = pd.to_numeric(tyt_data['Total Correct TYT'], errors='coerce')

# Box plot to compare Total Correct TYT between English and Turkish departments
plt.figure(figsize=(10, 6))
tyt_data.boxplot(by='Language', column=['Total Correct TYT'], grid=False)
plt.title('Comparison of Total Correct TYT Between English and Turkish Departments')
plt.suptitle('')
plt.xlabel('Language')
plt.ylabel('Total Correct TYT')
plt.xticks([1, 2], ['English', 'Turkish'])
plt.show()
"""

# DEP TÜRLERİ ARASI ANALİZ

# 1 success order
"""
all_department_names = df['Department Name'].str.replace(r' \(English\)', '', regex=True).unique()

# Adjust categorization to include "Education" and "Other" as new groups
final_department_groups = {
    "Engineering": [],
    "Sciences": [],
    "Education": [],
    "Other": []
}

# Updated categorization logic for the new groups
for department in all_department_names:
    if any(keyword in department for keyword in ["Engineering", "Mechatronics", "Automation"]):
        final_department_groups["Engineering"].append(department)
    elif any(
        keyword in department
        for keyword in ["Mathematical", "Chemistry", "Bioengineering", "Physics", "Statistics", "Mathematics", "Molecular Biology"]
    ):
        final_department_groups["Sciences"].append(department)
    elif any(
        keyword in department
        for keyword in ["Education", "Teaching", "Language", "Guidance", "Preschool", "Primary"]
    ):
        final_department_groups["Education"].append(department)
    else:
        final_department_groups["Other"].append(department)

# Move "Elementary Mathematics Education" from Sciences to Education
if "Elementary Mathematics Education" in final_department_groups["Sciences"]:
    final_department_groups["Sciences"].remove("Elementary Mathematics Education")
    final_department_groups["Education"].append("Elementary Mathematics Education")

print(final_department_groups)

success_order_data = df[['Department Name', 'Success Order']].dropna()

# Categorize each department based on the final groups
success_order_data['Group'] = success_order_data['Department Name'].apply(
    lambda dept: (
        "Engineering" if dept.replace(' (English)', '') in final_department_groups["Engineering"] else
        "Sciences" if dept.replace(' (English)', '') in final_department_groups["Sciences"] else
        "Education" if dept.replace(' (English)', '') in final_department_groups["Education"] else
        "Other"
    )
)

# Convert Success Order to numeric
success_order_data['Success Order'] = pd.to_numeric(success_order_data['Success Order'], errors='coerce')

# Filter out rows with missing or invalid data
success_order_data = success_order_data.dropna()

# Box plot to compare success order across groups
plt.figure(figsize=(12, 6))
success_order_data.boxplot(by='Group', column=['Success Order'], grid=False)
plt.title('Comparison of Success Order Across Groups')
plt.suptitle('')
plt.xlabel('Group')
plt.ylabel('Success Order (Lower is Better)')
plt.xticks([1, 2, 3, 4], ['Engineering', 'Sciences', 'Education', 'Other'])
plt.show()
"""

# 2 male female ?????
"""
all_department_names = df['Department Name'].str.replace(r' \(English\)', '', regex=True).unique()

# Adjust categorization to include "Education" and "Other" as new groups
final_department_groups = {
    "Engineering": [],
    "Sciences": [],
    "Education": [],
    "Other": []
}

# Updated categorization logic for the new groups
for department in all_department_names:
    if any(keyword in department for keyword in ["Engineering", "Mechatronics", "Automation"]):
        final_department_groups["Engineering"].append(department)
    elif any(
        keyword in department
        for keyword in ["Mathematical", "Chemistry", "Bioengineering", "Physics", "Statistics", "Mathematics", "Molecular Biology"]
    ):
        final_department_groups["Sciences"].append(department)
    elif any(
        keyword in department
        for keyword in ["Education", "Teaching", "Language", "Guidance", "Preschool", "Primary"]
    ):
        final_department_groups["Education"].append(department)
    else:
        final_department_groups["Other"].append(department)

# Move "Elementary Mathematics Education" from Sciences to Education
if "Elementary Mathematics Education" in final_department_groups["Sciences"]:
    final_department_groups["Sciences"].remove("Elementary Mathematics Education")
    final_department_groups["Education"].append("Elementary Mathematics Education")
gender_distribution_data = df[['Department Name', 'Male', 'Female']].dropna()

# Categorize each department based on the final groups
gender_distribution_data['Group'] = gender_distribution_data['Department Name'].apply(
    lambda dept: (
        "Engineering" if dept.replace(' (English)', '') in final_department_groups["Engineering"] else
        "Sciences" if dept.replace(' (English)', '') in final_department_groups["Sciences"] else
        "Education" if dept.replace(' (English)', '') in final_department_groups["Education"] else
        "Other"
    )
)

# Calculate percentages
gender_distribution_data['Male_Percentage'] = gender_distribution_data['Male'] / (
    gender_distribution_data['Male'] + gender_distribution_data['Female']
) * 100
gender_distribution_data['Female_Percentage'] = gender_distribution_data['Female'] / (
    gender_distribution_data['Male'] + gender_distribution_data['Female']
) * 100

# Filter out rows with missing or invalid data
gender_distribution_data = gender_distribution_data.dropna()

# Box plot to compare male percentage across groups
plt.figure(figsize=(12, 6))
gender_distribution_data.boxplot(by='Group', column=['Male_Percentage'], grid=False)
plt.title('Comparison of Male Percentage Across Groups')
plt.suptitle('')
plt.xlabel('Group')
plt.ylabel('Male Percentage (%)')
plt.xticks([1, 2, 3, 4], ['Engineering', 'Sciences', 'Education', 'Other'])
plt.show()

# Box plot to compare female percentage across groups
plt.figure(figsize=(12, 6))
gender_distribution_data.boxplot(by='Group', column=['Female_Percentage'], grid=False)
plt.title('Comparison of Female Percentage Across Groups')
plt.suptitle('')
plt.xlabel('Group')
plt.ylabel('Female Percentage (%)')
plt.xticks([1, 2, 3, 4], ['Engineering', 'Sciences', 'Education', 'Other'])
plt.show()

print(df.columns)

"""

# 3 exchange
"""
all_department_names = df['Department Name'].str.replace(r' \(English\)', '', regex=True).unique()

# Adjust categorization to include "Education" and "Other" as new groups
final_department_groups = {
    "Engineering": [],
    "Sciences": [],
    "Education": [],
    "Other": []
}

# Updated categorization logic for the new groups
for department in all_department_names:
    if any(keyword in department for keyword in ["Engineering", "Mechatronics", "Automation"]):
        final_department_groups["Engineering"].append(department)
    elif any(
        keyword in department
        for keyword in ["Mathematical", "Chemistry", "Bioengineering", "Physics", "Statistics", "Mathematics", "Molecular Biology"]
    ):
        final_department_groups["Sciences"].append(department)
    elif any(
        keyword in department
        for keyword in ["Education", "Teaching", "Language", "Guidance", "Preschool", "Primary"]
    ):
        final_department_groups["Education"].append(department)
    else:
        final_department_groups["Other"].append(department)

# Move "Elementary Mathematics Education" from Sciences to Education
if "Elementary Mathematics Education" in final_department_groups["Sciences"]:
    final_department_groups["Sciences"].remove("Elementary Mathematics Education")
    final_department_groups["Education"].append("Elementary Mathematics Education")
# Extract relevant columns for exchange analysis
exchange_data = general_data[['Department Name', 'Exchange to Abroad', 'Exchange from Abroad']].dropna()

# Categorize each department based on the final groups
exchange_data['Group'] = exchange_data['Department Name'].apply(
    lambda dept: (
        "Engineering" if dept.replace(' (English)', '') in final_department_groups["Engineering"] else
        "Sciences" if dept.replace(' (English)', '') in final_department_groups["Sciences"] else
        "Education" if dept.replace(' (English)', '') in final_department_groups["Education"] else
        "Other"
    )
)

# Convert exchange numbers to numeric
exchange_data['Exchange to Abroad'] = pd.to_numeric(exchange_data['Exchange to Abroad'], errors='coerce')
exchange_data['Exchange from Abroad'] = pd.to_numeric(exchange_data['Exchange from Abroad'], errors='coerce')

# Filter out rows with missing or invalid data
exchange_data = exchange_data.dropna()

# Box plot for Exchange to Abroad
plt.figure(figsize=(12, 6))
exchange_data.boxplot(by='Group', column=['Exchange to Abroad'], grid=False)
plt.title('Comparison of Exchange to Abroad Across Groups')
plt.suptitle('')
plt.xlabel('Group')
plt.ylabel('Number of Students Exchanged to Abroad')
plt.xticks([1, 2, 3, 4], ['Engineering', 'Sciences', 'Education', 'Other'])
plt.show()

# Box plot for Exchange from Abroad
plt.figure(figsize=(12, 6))
exchange_data.boxplot(by='Group', column=['Exchange from Abroad'], grid=False)
plt.title('Comparison of Exchange from Abroad Across Groups')
plt.suptitle('')
plt.xlabel('Group')
plt.ylabel('Number of Students Exchanged from Abroad')
plt.xticks([1, 2, 3, 4], ['Engineering', 'Sciences', 'Education', 'Other'])
plt.show()
"""

# CORRELATION
"""
correlation_data = df[
    ['Base Point', 'Success Order', 'Preferred number', 'Total Correct TYT',
     'Total Correct AYT', 'Marmara', 'Aegean', 'Mediterranean',
     'Black Sea', 'Central Anatolia', 'Eastern Anatolia',
     'Southeastern Anatolia']
]

# Convert data to numeric, handle missing values
correlation_data = correlation_data.apply(pd.to_numeric, errors='coerce')
correlation_data = correlation_data.dropna()

# Calculate the correlation matrix
correlation_matrix = correlation_data.corr()


plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix")
plt.show()


"""

# Faculty total student repr
"""
# Extract relevant data for total student numbers by faculty and year
faculty_student_data = df[['Faculty Name', 'Year', 'Total Student Number']].dropna()

# Convert year and student numbers to numeric
faculty_student_data['Year'] = pd.to_numeric(faculty_student_data['Year'], errors='coerce')
faculty_student_data['Total Student Number'] = pd.to_numeric(faculty_student_data['Total Student Number'], errors='coerce')

# Filter data for years 2021, 2022, and 2023
filtered_data = faculty_student_data[faculty_student_data['Year'].isin([2021, 2022, 2023])]

# Group by Faculty and Year to calculate total student numbers
grouped_data = filtered_data.groupby(['Faculty Name', 'Year'])['Total Student Number'].sum().reset_index()

# Pivot data for visualization
pivot_data = grouped_data.pivot(index='Faculty Name', columns='Year', values='Total Student Number')

# Plot the graph
pivot_data.plot(kind='bar', figsize=(14, 8), width=0.8)
plt.title("Total Student Numbers by Faculty for 2021-2023")
plt.xlabel("Faculty Name")
plt.ylabel("Total Student Number")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Year", loc="upper right")
plt.tight_layout()
plt.show()
"""
