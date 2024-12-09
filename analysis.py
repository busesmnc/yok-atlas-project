import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

csv_file_path = "ytu_general_analysis.csv"
csv_file_path_dep_gen = "z_department_gender_change.csv"
csv_file_path_dep_acd = "z_department_academic_changes.csv"
csv_file_path_dep_tyt = "z_department_tyt_ayt_ydt_changes"
csv_file_path_fac_gen = "z_faculty_gender_change.csv"
csv_file_path_fac_acd = "z_faculty_academic_changes.csv"
csv_file_path_fac_tyt = "z_faculty_tyt_ayt_ydt_changes"
csv_file_path_ytu_gen = "z_ytu_gender_change.csv"
csv_file_path_ytu_acd = "z_ytu_academic_changes_"
csv_file_path_ytu_tyt = "z_ytu_tyt_ayt_ydt_changes"

df = pd.read_csv(csv_file_path)
df_dep_gen = pd.read_csv(csv_file_path_dep_gen)
df_dep_acd = pd.read_csv(csv_file_path_dep_acd)
df_dep_tyt = pd.read_csv(csv_file_path_dep_tyt)
df_fac_gen = pd.read_csv(csv_file_path_fac_gen)
df_fac_acd = pd.read_csv(csv_file_path_fac_acd)
df_fac_tyt = pd.read_csv(csv_file_path_fac_tyt)
df_ytu_gen = pd.read_csv(csv_file_path_ytu_gen)
df_ytu_acd = pd.read_csv(csv_file_path_ytu_acd)
df_ytu_tyt = pd.read_csv(csv_file_path_ytu_tyt)


def gender_change_analysis(dataframe, group_col):
    """
    Yıllara göre cinsiyet değişimini analiz eden ve sonuçları sıralı tablo halinde döndüren bir fonksiyon.

    Args:
        dataframe (pd.DataFrame): Analiz yapılacak veri çerçevesi.
        group_col (str): Gruplama yapılacak sütun (örneğin: 'faculty_name' veya 'department_name').

    Returns:
        pd.DataFrame: Gruplama sütununa ve yıla göre sıralı toplam cinsiyet, sayısal değişim ve yüzdesel değişimleri içeren tablo.
    """
    # Yıllara göre toplam kadın ve erkek sayılarını hesapla
    yearly_totals = dataframe.groupby([group_col, 'year'])[['total_male_number', 'total_female_number']].sum().reset_index()

    # Erkek ve kadın değişimlerini hesapla
    yearly_totals['male_change'] = yearly_totals.groupby(group_col)['total_male_number'].diff().fillna(0)
    yearly_totals['male_percentage_change'] = yearly_totals.groupby(group_col)['total_male_number'].pct_change().fillna(0) * 100

    yearly_totals['female_change'] = yearly_totals.groupby(group_col)['total_female_number'].diff().fillna(0)
    yearly_totals['female_percentage_change'] = yearly_totals.groupby(group_col)['total_female_number'].pct_change().fillna(0) * 100

    # Sıralı tablo oluştur
    sorted_table = yearly_totals.sort_values(by=[group_col, 'year']).reset_index(drop=True)

    return sorted_table


def ytu_gender_changes(data):

    # İlgili sütunları seçip yıllara göre toplamları hesaplama
    gender_data = data.groupby('year')[['total_male_number', 'total_female_number']].sum().reset_index()
    gender_data.rename(columns={'total_male_number': 'Male Students', 'total_female_number': 'Female Students'},
                       inplace=True)

    # Artış/Azalış ve yüzdelik değişim sütunları ekleme
    gender_data['Male Change'] = gender_data['Male Students'].diff()
    gender_data['Female Change'] = gender_data['Female Students'].diff()
    gender_data['Male Change (%)'] = gender_data['Male Change'] / gender_data['Male Students'].shift(1) * 100
    gender_data['Female Change (%)'] = gender_data['Female Change'] / gender_data['Female Students'].shift(1) * 100

    # Grafik oluşturma
    plt.figure(figsize=(12, 6))
    plt.plot(gender_data['year'], gender_data['Male Students'], marker='o', label='Male Students')
    plt.plot(gender_data['year'], gender_data['Female Students'], marker='o', label='Female Students')
    plt.title('Yearly Male and Female Student Changes')
    plt.xlabel('Year')
    plt.ylabel('Number of Students')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Grafik gösterimi
    # plt.show()

    # Analiz tablosunu döndürme
    return gender_data


def analyze_academic_changes(data, group_by='department_name'):
    """
    Yıllara göre akademik değişiklikleri analiz eden bir fonksiyon.

    Args:
        data (pd.DataFrame): Analiz yapılacak veri çerçevesi.
        group_by (str): Gruplama yapılacak sütun (örneğin: 'department_name' veya 'faculty_name').

    Returns:
        pd.DataFrame: Yıllara göre toplam kontenjan, tercih, yerleşen öğrenci ve akademik personel değişimlerini içeren tablo.
    """

    # Yerleşen öğrenci sayısını hesaplama
    data['placed_students'] = data['male'] + data['female']

    # Veriyi gruplama ve toplamları hesaplama
    grouped_data = data.groupby([group_by, 'year']).agg({
        'quota': 'sum',  # Kontenjan toplamı
        'preferred': 'sum',  # Tercih edilme toplamı
        'placed_students': 'sum',  # Yerleşen öğrenci toplamı
        'professors': 'sum',  # Profesör sayısı toplamı
        'phd': 'sum',  # Doktora sahibi personel toplamı
        'assoc_prof': 'sum'  # Doçent sayısı toplamı
    }).reset_index()

    # Değişim hesaplamaları
    for col in ['quota', 'preferred', 'placed_students', 'professors', 'phd', 'assoc_prof']:
        grouped_data[f'{col.capitalize()} Change'] = grouped_data.groupby(group_by)[col].diff()
        grouped_data[f'{col.capitalize()} Change (%)'] = grouped_data.groupby(group_by)[col].pct_change() * 100

    # Sıralama
    if group_by == 'department_name':
        grouped_data.sort_values(by=['department_name', 'year'], ascending=[True, True], inplace=True)
    else:
        grouped_data.sort_values(by=['faculty_name', 'year'], ascending=[True, True], inplace=True)

    return grouped_data


def ytu_analyze_academic_changes(data):
    """
    Yıllara göre tüm okulun akademik değişikliklerini analiz eden bir fonksiyon.

    Args:
        data (pd.DataFrame): Analiz yapılacak veri çerçevesi.

    Returns:
        pd.DataFrame: Yıllara göre toplam kontenjan, tercih, yerleşen öğrenci ve akademik personel değişimlerini içeren tablo.
    """

    # Yerleşen öğrenci sayısını hesaplama
    data['placed_students'] = data['male'] + data['female']

    # Yıllara göre toplamları hesaplama
    yearly_totals = data.groupby('year').agg({
        'quota': 'sum',  # Kontenjan toplamı
        'preferred': 'sum',  # Tercih edilme toplamı
        'placed_students': 'sum',  # Yerleşen öğrenci toplamı
        'professors': 'sum',  # Profesör sayısı toplamı
        'phd': 'sum',  # Doktora sahibi personel toplamı
        'assoc_prof': 'sum'  # Doçent sayısı toplamı
    }).reset_index()

    # Değişim hesaplamaları
    for col in ['quota', 'preferred', 'placed_students', 'professors', 'phd', 'assoc_prof']:
        yearly_totals[f'{col.capitalize()} Change'] = yearly_totals[col].diff()
        yearly_totals[f'{col.capitalize()} Change (%)'] = yearly_totals[col].pct_change() * 100

    # Sıralama (Yıllara göre)
    yearly_totals.sort_values(by='year', ascending=True, inplace=True)

    return yearly_totals


def analyze_base_point_changes(data, group_by='faculty_name', department_type=None):
    """
    TYT, AYT ve YDT başarılarını, correct answers ayrımı ile yıllara göre analiz eder.

    Args:
    - data (pd.DataFrame): Girdi veri çerçevesi.
    - group_by (str): Analiz için grup değişkeni ('department_name' veya 'faculty_name').
    - department_type (str, optional): Bölüm türü filtresi ('ea', 'söz', 'dil').

    Returns:
    - pd.DataFrame: Yıllık analiz tablosu, artış/azalış ve yüzdelik değişimlerle birlikte.
    """

    # TYT, AYT ve YDT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # NaN değerlerini 0 ile doldurma
    data[tyt_columns] = data[tyt_columns].fillna(0)
    data[ayt_columns] = data[ayt_columns].fillna(0)
    data[ydt_columns] = data[ydt_columns].fillna(0)

    # Correct answers ayrımı
    data['tyt_correct_answer'] = data[tyt_columns].sum(axis=1)
    data['ayt_correct_answer'] = data[ayt_columns].sum(axis=1)
    data['ydt_correct_answer'] = data[ydt_columns].sum(axis=1)

    # group_by string ise listeye çevir
    if isinstance(group_by, str):
        group_by = [group_by]

    # Bölüm türü filtresi
    if department_type:
        normalized_department_type = department_type.strip().lower()
        data = data[data['department_type'].str.strip().str.lower() == normalized_department_type].copy()

    # Analiz sütunlarını belirleme
    columns_to_analyze = ['base_point', 'success_order', 'tyt_correct_answer',
                          'ayt_correct_answer', 'ydt_correct_answer']

    # Gruplama fonksiyonu seçimi
    aggregation_function = 'mean' if 'faculty_name' in group_by else 'sum'

    # Gruplama ve analiz
    grouped_data = data.groupby(['year'] + group_by).agg({
        col: aggregation_function for col in columns_to_analyze
    }).reset_index()

    # Değişim hesaplamaları
    for col in columns_to_analyze:
        grouped_data[f'{col} Change'] = grouped_data.groupby(group_by)[col].diff()
        grouped_data[f'{col} Change (%)'] = grouped_data.groupby(group_by)[col].pct_change() * 100

    # Sonuçları sıralama
    grouped_data.sort_values(by=group_by + ['year'], inplace=True)

    # Döndürülecek sütunlar
    selected_columns = ['year'] + group_by + columns_to_analyze + \
                       [f'{col} Change' for col in columns_to_analyze] + \
                       [f'{col} Change (%)' for col in columns_to_analyze]

    return grouped_data[selected_columns]


def ytu_analyze_base_point_changes(data):
    """
    Sütunları yıla göre gruplayarak ortalama değerleri hesaplayan bir fonksiyon.

    Args:
    - data (pd.DataFrame): Girdi veri çerçevesi.

    Returns:
    - pd.DataFrame: Yıllara göre ortalama değerleri içeren tablo.
    """

    # TYT, AYT ve YDT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # NaN değerlerini 0 ile doldurma
    data[tyt_columns] = data[tyt_columns].fillna(0)
    data[ayt_columns] = data[ayt_columns].fillna(0)
    data[ydt_columns] = data[ydt_columns].fillna(0)

    # Correct answers ayrımı
    data['tyt_correct_answer'] = data[tyt_columns].sum(axis=1)
    data['ayt_correct_answer'] = data[ayt_columns].sum(axis=1)
    data['ydt_correct_answer'] = data[ydt_columns].sum(axis=1)

    # Analiz edilecek sütunlar
    columns_to_analyze = ['base_point', 'success_order', 'tyt_correct_answer',
                          'ayt_correct_answer', 'ydt_correct_answer']

    # Yıla göre gruplayarak ortalama değerleri hesaplama
    yearly_averages = data.groupby('year').agg({
        col: 'mean' for col in columns_to_analyze
    }).reset_index()

    # Sonuçları sıralama
    yearly_averages.sort_values(by='year', inplace=True)

    return yearly_averages


def dep_visualize_trends_by_column_with_top_and_bottom(data, metric, group_column='department_name', top_n=10):
    """
    Visualizes trends for a specified metric over years for the top and bottom N departments.

    Parameters:
    - data: DataFrame containing the data to analyze.
    - metric: The column name of the metric to visualize (e.g., 'professors').
    - group_column: The column to group by (default is 'department_name').
    - top_n: Number of departments to include in the top and bottom visualizations (default is 10).

    Returns:
    - None: Displays two plots (top N and bottom N trends).
    """
    # Calculate the average value of the metric for each department
    department_means = data.groupby(group_column)[metric].mean()

    # Get the top N and bottom N departments based on the metric
    top_departments = department_means.nlargest(top_n).index
    bottom_departments = department_means.nsmallest(top_n).index

    # Filter the data for top and bottom departments
    top_data = data[data[group_column].isin(top_departments)]
    bottom_data = data[data[group_column].isin(bottom_departments)]

    # Pivot data for easier plotting
    top_trends = top_data.pivot(index='year', columns=group_column, values=metric)
    bottom_trends = bottom_data.pivot(index='year', columns=group_column, values=metric)

    # Plot trends for top departments
    plt.figure(figsize=(14, 8))
    for column in top_trends.columns:
        plt.plot(top_trends.index, top_trends[column], marker='o', label=column)

    metric_cleaned = metric.replace('_', ' ').capitalize()
    plt.title(f'{metric_cleaned} Trends Over Years for Top {top_n} Departments', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(metric_cleaned, fontsize=14)
    plt.xticks(top_trends.index, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot trends for bottom departments
    plt.figure(figsize=(14, 8))
    for column in bottom_trends.columns:
        plt.plot(bottom_trends.index, bottom_trends[column], marker='o', label=column)

    plt.title(f'{metric_cleaned} Trends Over Years for Bottom {top_n} Departments', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(metric_cleaned, fontsize=14)
    plt.xticks(bottom_trends.index, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def visualize_column_trends_by_year(data, metric, top_n=10):
    """
    Visualizes trends for a specified metric over years.

    Parameters:
    - data: DataFrame containing the data to analyze.
    - metric: The column name of the metric to visualize (e.g., 'Male Students').
    - top_n: Maximum number of groups to display, if applicable (default is 10).

    Returns:
    - None: Displays the plot.
    """
    # Sort the data by year for consistent plotting
    sorted_data = data.sort_values(by='year')

    # Plot the trends
    plt.figure(figsize=(12, 6))
    plt.plot(sorted_data['year'], sorted_data[metric], marker='o', label=metric)

    # Set plot details
    metric_cleaned = metric.replace('_', ' ').capitalize()
    plt.title(f'{metric_cleaned} Trends Over Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(metric_cleaned, fontsize=14)
    plt.xticks(sorted_data['year'], fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()


# Example usage: Visualize trends for 'Male Students'
# visualize_column_trends_by_year(df_ytu_gen, metric='Male Students')

# plot_yearly_trend_handling_missing(data=df_fac_change, group_column='faculty_name',
#                                  metric='base_point Change (%)', top_n=10)


# dep_visualize_trends_by_column_with_top_and_bottom(df_fac_tyt, group_column='faculty_name',
#                                                    metric='tyt_correct_answer', top_n=10)



