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


# columns_to_analyze_by_type = ['Total Correct TYT', 'Total Correct AYT', 'Total Correct YDT']
# analyze_by_department_type(df2, columns_to_analyze_by_type)


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


factors_beyond_exchange = ['Professors', 'Assoc Prof', 'Phd', 'Base Point',
                'Success Order', 'Preferred number', 'Quota', 'Placed Number', 'Total Correct TYT', 'Total Correct AYT'
]

# plot_beyond_exchange_factors(df2, factors_beyond_exchange)

