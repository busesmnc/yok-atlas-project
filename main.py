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

csv_file_path = "ytu_general_analysis.csv"
csv_file_path2 = "ytu_general_analysis2.csv"
csv_file_path_city = "department_city_student_counts.csv"
csv_file_path_dep = "department_yearly__percentage_change.csv"
csv_file_path_fac = "faculty_yearly_percentage_change.csv"
csv_file_path_ytu = "ytu_yearly_percentage_change.csv"

df = pd.read_csv(csv_file_path)
df2 = pd.read_csv(csv_file_path2)
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

# cat_cols, num_cols, cat_but_car = grab_col_names(df)


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
        return True
    else:
        return False


def department_general_analysis(data, group_by='department_name', department_type=None, year=None):
    columns_to_analyze = ['total_male_number',
                          'total_female_number', 'total_student_number_', 'professors',
                          'assoc_prof', 'phd', 'base_point', 'success_order', 'preferred',
                          'quota', 'placed_number', 'tyt_turkce', 'tyt_matematik', 'tyt_fen',
                          'tyt_sosyal', 'ayt_matematik', 'ayt_fizik', 'ayt_kimya', 'ayt_biyoloji',
                          'ayt_edebiyat', 'ayt_cografya1', 'ayt_cografya2', 'ayt_din',
                          'ayt_felsefe', 'ayt_tarih1', 'ayt_tarih2', 'ydt_yabanci_dil', 'Marmara',
                          'Ege', 'Akdeniz', 'Karadeniz', 'Ic_Anadolu', 'Dogu_Anadolu',
                          'Guney_Dogu_Anadolu', 'tyt_correct_answer', 'ayt_correct_answer',
                          'ydt_correct_answer']

    # TYT ve AYT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # NaN değerlerini 0 ile doldurma
    data[tyt_columns] = data[tyt_columns].fillna(0)
    data[ayt_columns] = data[ayt_columns].fillna(0)
    data[ydt_columns] = data[ydt_columns].fillna(0)

    # Correct answers ayrımı
    data.loc[:, 'tyt_correct_answer'] = data[tyt_columns].sum(axis=1)
    data.loc[:, 'ayt_correct_answer'] = data[ayt_columns].sum(axis=1)
    data.loc[:, 'ydt_correct_answer'] = data[ydt_columns].sum(axis=1)

    # Eksik sütunlar varsa 0 ile doldurma
    for col in tyt_columns + ayt_columns + ydt_columns:
        if col not in data.columns:
            data[col] = 0

    # group_by string ise listeye çevir
    if isinstance(group_by, str):
        group_by = [group_by]

    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8').upper()

    # Department type filtresi
    if department_type:
        normalized_department_type = normalize_string(department_type)
        data = data[data['department_type'].apply(lambda x: normalize_string(x) == normalized_department_type)].copy()

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

    # Correct answers ayrımı
    correct_answers = ['tyt_correct_answer', 'ayt_correct_answer', 'ydt_correct_answer']
    for i in correct_answers:
        if i in selected_columns:
            # Geçmiş yıl verisini kullanarak yüzdelik değişim hesaplama
            analysis_data[f'{i} Change (%)'] = analysis_data.groupby(group_by)[i].pct_change() * 100

    # Değişim ve yüzdelik değişim hesaplamaları
    for col in [col for col in selected_columns if col not in correct_answers]:
        # Geçmiş yıl verisini kullanarak yüzdelik değişim hesaplama
        analysis_data[f'{col} Change (%)'] = analysis_data.groupby(group_by)[col].pct_change() * 100

    # Yıl filtreleme (year parametresinin kontrolü ve dönüştürülmesi)
    if year:
        # Ensure 'year' column is in numeric format (int)
        analysis_data['year'] = pd.to_numeric(analysis_data['year'], errors='coerce')

        # Yıl filtresi uygulanmadan önce verinin sıralanması
        analysis_data = analysis_data.sort_values(by=['department_name', 'year'])

        # Uygulanan yıl filtresi
        analysis_data = analysis_data[analysis_data['year'] == year]

    # Sonuçları döndürme
    selected_columns_with_change = ['year'] + group_by + ['department_type'] + [f'{col} Change (%)' for col in
                                                                                selected_columns]
    return analysis_data[selected_columns_with_change]


def faculty_analysis(data, faculty_name_column='faculty_name', year=None):
    # Gruplama ve hesaplamalar için gerekli sütunlar
    columns_to_analyze = ['total_male_number', 'total_female_number', 'total_student_number_', 'professors',
                          'assoc_prof', 'phd', 'base_point', 'success_order', 'preferred', 'quota', 'placed_number',
                          'tyt_turkce', 'tyt_matematik', 'tyt_fen', 'tyt_sosyal', 'ayt_matematik', 'ayt_fizik',
                          'ayt_kimya', 'ayt_biyoloji', 'ayt_edebiyat', 'ayt_cografya1', 'ayt_cografya2', 'ayt_din',
                          'ayt_felsefe', 'ayt_tarih1', 'ayt_tarih2', 'ydt_yabanci_dil', 'Marmara', 'Ege', 'Akdeniz',
                          'Karadeniz', 'Ic_Anadolu', 'Dogu_Anadolu', 'Guney_Dogu_Anadolu', 'tyt_correct_answer',
                          'ayt_correct_answer', 'ydt_correct_answer']

    # TYT ve AYT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # NaN değerlerini 0 ile doldurma
    data[tyt_columns] = data[tyt_columns].fillna(0)
    data[ayt_columns] = data[ayt_columns].fillna(0)
    data[ydt_columns] = data[ydt_columns].fillna(0)

    # Correct answers ayrımı
    data.loc[:, 'tyt_correct_answer'] = data[tyt_columns].sum(axis=1)
    data.loc[:, 'ayt_correct_answer'] = data[ayt_columns].sum(axis=1)
    data.loc[:, 'ydt_correct_answer'] = data[ydt_columns].sum(axis=1)

    # Eğer faculty_name_column bir string ise listeye dönüştür
    if isinstance(faculty_name_column, str):
        faculty_name_column = [faculty_name_column]

    # Gruplama ve hesaplama türlerine göre dict
    aggregation_methods = {
        'total_male_number': 'sum',
        'total_female_number': 'sum',
        'total_student_number_': 'sum',
        'professors': 'sum',
        'assoc_prof': 'sum',
        'phd': 'sum',
        'base_point': 'mean',  # Ortalama
        'success_order': 'sum',
        'preferred': 'sum',
        'quota': 'sum',
        'placed_number': 'sum',
        'tyt_turkce': 'mean',  # Ortalama
        'tyt_matematik': 'mean',
        'tyt_fen': 'mean',
        'tyt_sosyal': 'mean',
        'ayt_matematik': 'mean',
        'ayt_fizik': 'mean',
        'ayt_kimya': 'mean',
        'ayt_biyoloji': 'mean',
        'ayt_edebiyat': 'mean',
        'ayt_cografya1': 'mean',
        'ayt_cografya2': 'mean',
        'ayt_din': 'mean',
        'ayt_felsefe': 'mean',
        'ayt_tarih1': 'mean',
        'ayt_tarih2': 'mean',
        'ydt_yabanci_dil': 'mean',  # Ortalama
        'Marmara': 'sum',
        'Ege': 'sum',
        'Akdeniz': 'sum',
        'Karadeniz': 'sum',
        'Ic_Anadolu': 'sum',
        'Dogu_Anadolu': 'sum',
        'Guney_Dogu_Anadolu': 'sum',
        'tyt_correct_answer': 'mean',  # Ortalama
        'ayt_correct_answer': 'mean',
        'ydt_correct_answer': 'mean'
    }

    # Fakülte ve yıl bazında gruplama yapma
    faculty_data = data.groupby(faculty_name_column + ['year']).agg(aggregation_methods).reset_index()

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

    # Correct answers ayrımı
    correct_answers = ['tyt_correct_answer', 'ayt_correct_answer', 'ydt_correct_answer']
    for i in correct_answers:
        if i in selected_columns:
            # Geçmiş yıl verisini kullanarak yüzdelik değişim hesaplama
            faculty_data[f'{i} Change (%)'] = faculty_data.groupby(faculty_name_column)[i].pct_change() * 100

    # Yüzdelik değişim hesaplama (pct_change)
    for col in [col for col in selected_columns if col not in correct_answers]:
        if col in faculty_data.columns:
            faculty_data[f'{col} Change (%)'] = faculty_data.groupby(faculty_name_column)[col].pct_change() * 100

    # Yıl ve fakülte adı hariç, sadece yüzdelik değişimle gösterilecek sütunları seçme
    change_columns = [f'{col} Change (%)' for col in columns_to_analyze]

    if year:
        # Ensure 'year' column is in numeric format (int)
        faculty_data['year'] = pd.to_numeric(faculty_data['year'], errors='coerce')

        # Yıl filtresi uygulanmadan önce verinin sıralanması
        faculty_data = faculty_data.sort_values(by=['faculty_name', 'year'])

        # Uygulanan yıl filtresi
        faculty_data = faculty_data[faculty_data['year'] == year]

    # Sonuçları döndürme
    selected_columns_with_change = ['year'] + faculty_name_column + [f'{col} Change (%)'
                                                                   for col in selected_columns]

    return faculty_data[selected_columns_with_change]


def year_analysis(data):
    # Gruplama ve hesaplamalar için gerekli sütunlar
    columns_to_analyze = ['total_male_number', 'total_female_number', 'total_student_number_', 'professors',
                          'assoc_prof', 'phd', 'base_point', 'success_order', 'preferred', 'quota', 'placed_number',
                          'tyt_turkce', 'tyt_matematik', 'tyt_fen', 'tyt_sosyal', 'ayt_matematik', 'ayt_fizik',
                          'ayt_kimya', 'ayt_biyoloji', 'ayt_edebiyat', 'ayt_cografya1', 'ayt_cografya2', 'ayt_din',
                          'ayt_felsefe', 'ayt_tarih1', 'ayt_tarih2', 'ydt_yabanci_dil', 'Marmara', 'Ege', 'Akdeniz',
                          'Karadeniz', 'Ic_Anadolu', 'Dogu_Anadolu', 'Guney_Dogu_Anadolu', 'tyt_correct_answer',
                          'ayt_correct_answer', 'ydt_correct_answer']

    # TYT ve AYT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # NaN değerlerini 0 ile doldurma
    data[tyt_columns] = data[tyt_columns].fillna(0)
    data[ayt_columns] = data[ayt_columns].fillna(0)
    data[ydt_columns] = data[ydt_columns].fillna(0)

    # Correct answers ayrımı
    data.loc[:, 'tyt_correct_answer'] = data[tyt_columns].sum(axis=1)
    data.loc[:, 'ayt_correct_answer'] = data[ayt_columns].sum(axis=1)
    data.loc[:, 'ydt_correct_answer'] = data[ydt_columns].sum(axis=1)

    # Gruplama ve hesaplama türlerine göre dict
    aggregation_methods = {
        'total_male_number': 'sum',
        'total_female_number': 'sum',
        'total_student_number_': 'sum',
        'professors': 'sum',
        'assoc_prof': 'sum',
        'phd': 'sum',
        'base_point': 'mean',  # Ortalama
        'success_order': 'sum',
        'preferred': 'sum',
        'quota': 'sum',
        'placed_number': 'sum',
        'tyt_turkce': 'mean',  # Ortalama
        'tyt_matematik': 'mean',
        'tyt_fen': 'mean',
        'tyt_sosyal': 'mean',
        'ayt_matematik': 'mean',
        'ayt_fizik': 'mean',
        'ayt_kimya': 'mean',
        'ayt_biyoloji': 'mean',
        'ayt_edebiyat': 'mean',
        'ayt_cografya1': 'mean',
        'ayt_cografya2': 'mean',
        'ayt_din': 'mean',
        'ayt_felsefe': 'mean',
        'ayt_tarih1': 'mean',
        'ayt_tarih2': 'mean',
        'ydt_yabanci_dil': 'mean',  # Ortalama
        'Marmara': 'sum',
        'Ege': 'sum',
        'Akdeniz': 'sum',
        'Karadeniz': 'sum',
        'Ic_Anadolu': 'sum',
        'Dogu_Anadolu': 'sum',
        'Guney_Dogu_Anadolu': 'sum',
        'tyt_correct_answer': 'mean',  # Ortalama
        'ayt_correct_answer': 'mean',
        'ydt_correct_answer': 'mean'
    }

    # Yıl bazında gruplama yapma
    year_data = data.groupby(['year']).agg(aggregation_methods).reset_index()

    # Yüzdelik değişim hesaplama (pct_change)
    for col in columns_to_analyze:
        if col in year_data.columns:
            year_data[f'{col} Change (%)'] = year_data[col].pct_change() * 100

    # Yıl ve yüzdelik değişimle gösterilecek sütunları seçme
    change_columns = [f'{col} Change (%)' for col in columns_to_analyze]

    # Sonuçları döndürme
    selected_columns_with_change = ['year'] + change_columns

    return year_data[selected_columns_with_change]


def plot_yearly_trend_handling_missing(data, metric, group_column='department_name', top_n=10):
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
    yearly_analysis = data.groupby(['year', group_column])[metric].mean().unstack()

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


def analyze_and_plot_regional_distribution(data, region_columns, year_column='year'):
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


def analyze_and_visualize_performance(data, column='tyt_matematik', top_n=5):
    """
    Analyzes and visualizes gender representation in the specified column.

    Parameters:
        data (DataFrame): The dataset containing gender and performance columns.
        column (str): The column name for the performance metric to analyze.
        top_n (int): Number of top departments to analyze.

    Returns:
        None: Displays a bar chart of male and female percentages for the top departments.
    """
    if column not in data.columns:
        raise ValueError(f"The column '{column}' does not exist in the dataset.")

    # Calculate average scores for each department
    department_avg = data.groupby('department_name').agg(
        avg_score=(column, 'mean'),
        total_male=('male', 'sum'),
        total_female=('female', 'sum')
    ).reset_index()

    # Calculate percentages for males and females
    department_avg['total_students'] = department_avg['total_male'] + department_avg['total_female']
    department_avg['male_percentage'] = department_avg['total_male'] / department_avg['total_students'] * 100
    department_avg['female_percentage'] = department_avg['total_female'] / department_avg['total_students'] * 100

    # Sort departments by average score and select top N
    top_departments = department_avg.sort_values(by='avg_score', ascending=False).head(top_n)

    # Append average score to department names for labeling
    top_departments['department_label'] = top_departments.apply(
        lambda row: f"{row['department_name']} ({row['avg_score']:.2f})", axis=1
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
    ax.set_title(f'Male vs Female Percentage in Top {top_n} Departments by {column_title.capitalize()}')
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
    analyze_and_visualize_performance(df2, column='total_correct_ydt', top_n=5)
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
    factors = ['base_point', 'success_order', 'quota', 'preferred', 'professors', 'phd', 'assoc_prof']
    correlation_matrix = data[factors].corr()
    print("Correlation Matrix for Base Points:")
    print(correlation_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix for Base Points and Influencing Factors')
    plt.show()

    return correlation_matrix


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
    department_type_analysis = data.groupby('department_type').agg(
        total_male=('male', 'sum'),
        total_female=('female', 'sum'),
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
        bars_male = ax.bar(department_type_analysis['department_type'],
                           department_type_analysis['male_percentage'],
                           label='Male %', alpha=0.7)
        bars_female = ax.bar(department_type_analysis['department_type'],
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


columns_to_analyze_by_type = ['total_correct_tyt', 'total_correct_ayt', 'total_correct_ydt', 'tyt_matematik']


# analyze_by_department_type(df2, columns_to_analyze_by_type)


def analyze_academic_staff_impact(data, staff_columns, preference_column='preferred'):
    """
    Analyzes the correlation between academic staff numbers and student preferences.

    Parameters:
        data (DataFrame): The dataset containing academic staff and preference columns.
        staff_columns (list): Columns representing academic staff counts (e.g., professors, assoc_prof).
        preference_column (str): Column representing student preference counts.

    Returns:
        None: Displays scatter plots and correlation coefficients.
    """
    for staff_col in staff_columns:
        if staff_col not in data.columns or preference_column not in data.columns:
            print(f"Column '{staff_col}' or '{preference_column}' not found in the dataset.")
            continue

        # Calculate correlation
        valid_data = data[[staff_col, preference_column]].dropna()
        if valid_data.empty:
            print(f"No valid data for {staff_col} and {preference_column}.")
            continue

        correlation, p_value = pearsonr(valid_data[staff_col], valid_data[preference_column])

        # Display scatter plot with regression line
        plt.figure(figsize=(8, 6))
        sns.regplot(x=staff_col, y=preference_column, data=valid_data, scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
        plt.title(f"Correlation Between {staff_col.capitalize()} and {preference_column.capitalize()} (r = {correlation:.2f})")
        plt.xlabel(staff_col.replace('_', ' ').capitalize())
        plt.ylabel(preference_column.replace('_', ' ').capitalize())
        plt.tight_layout()
        plt.show()

        print(f"Correlation between {staff_col} and {preference_column}: r = {correlation:.2f}, p = {p_value:.4f}")


# Columns representing academic staff
staff_columns = ['professors', 'assoc_prof', 'phd']

# Perform the analysis
# analyze_academic_staff_impact(df2, staff_columns)


def plot_beyond_exchange_factors(data, factors, target='preferred'):
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


# Call the function with relevant parameters
factors_beyond_exchange = [
    'base_point', 'success_order', 'quota', 'placed_number',
    'professors', 'assoc_prof', 'phd',
    'total_correct_tyt'
]

# plot_beyond_exchange_factors(df2, factors_beyond_exchange)


def plot_top_bottom_departments(data, metric, top_n=5):
    """
    Plots the top and bottom N departments by a specified metric percentage change.

    Parameters:
    data (DataFrame): The input DataFrame containing department data.
    metric (str): The column name for the metric to analyze (e.g., "tyt_correct_answer Change (%)").
    top_n (int): The number of top and bottom departments to display (default is 5).
    """
    # Sort the data by the selected metric
    top_departments = data.sort_values(metric, ascending=False).head(top_n)
    bottom_departments = data.sort_values(metric).head(top_n)

    # Clean the metric name for the title
    metric_title = metric.replace("_", " ")

    # Plot the top and bottom departments
    plt.figure(figsize=(12, 6))
    plt.barh(top_departments["department_name"], top_departments[metric], color='green', label='Highest % Increase')
    plt.barh(bottom_departments["department_name"], bottom_departments[metric], color='red', label='Highest % Decrease')

    plt.title(f"Top {top_n} and Bottom {top_n} Departments by {metric_title}")
    plt.xlabel("Percentage Change (%)")
    plt.ylabel("Department Name")
    plt.legend()
    plt.grid(True)
    plt.show()


# Call the function for the "tyt_correct_answer Change (%)" metric
plot_top_bottom_departments(df_dep_change, "total_student_number_ Change (%)")