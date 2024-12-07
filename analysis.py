import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

csv_file_path = "ytu_general_analysis.csv"

df = pd.read_csv(csv_file_path)


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

