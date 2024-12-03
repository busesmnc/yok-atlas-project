import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

csv_file_path = "gen_data.csv"

df = pd.read_csv(csv_file_path)

# general info


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


# check_df(df)

# ############################################### gender_change_analysis
print("GENDER ANALYSIS")


def gender_change_analysis(dataframe, group_col, years_col='year', male_col='total_male_number', female_col='total_female_number'):
    """
    Yıllara göre cinsiyet değişimini analiz eden bir fonksiyon.

    Args:
        dataframe (pd.DataFrame): Analiz yapılacak veri çerçevesi.
        group_col (str): Gruplama yapılacak sütun (örneğin: 'faculty_name' veya 'department_name').
        years_col (str): Yıl sütunu adı (default: 'year').
        male_col (str): Erkek öğrenci sayısını temsil eden sütun adı (default: 'male').
        female_col (str): Kadın öğrenci sayısını temsil eden sütun adı (default: 'female').

    Returns:
        pd.DataFrame: Yıllara göre toplam cinsiyet ve yüzdesel değişimleri içeren tablo.
    """

    yearly_totals = dataframe.groupby([group_col, years_col])[[male_col, female_col]].sum().reset_index()

    # Pivot tablo oluştur
    pivot_table = yearly_totals.pivot(index=group_col, columns=years_col, values=[male_col, female_col])

    # Erkek sayısı değişim oranlarını hesapla
    male_changes = pivot_table[(male_col)].pct_change(axis=1) * 100
    male_changes.columns = [f"male_change_{col}" for col in male_changes.columns]

    # Kadın sayısı değişim oranlarını hesapla
    female_changes = pivot_table[(female_col)].pct_change(axis=1) * 100
    female_changes.columns = [f"female_change_{col}" for col in female_changes.columns]

    # Tüm sonuçları birleştir
    result = pd.concat([pivot_table, male_changes, female_changes], axis=1).reset_index()

    # Sütun isimlerini düzelt
    result.columns = ['_'.join([str(i) for i in col]) if isinstance(col, tuple) else col for col in result.columns]

    return result


def plot_gender_change(dataframe, group_name, male_cols, female_cols):
    """
    Cinsiyet değişimlerini grafikle gösteren bir fonksiyon.

    Args:
        dataframe (pd.DataFrame): Gruplama sonrası elde edilen pivot tablo.
        group_name (str): Grafik çizilecek grubun adı (örneğin: bir fakülte veya departman).
        male_cols (list): Erkek öğrenci sayısının sütun isimleri (örneğin: ['male_2022', 'male_2023']).
        female_cols (list): Kadın öğrenci sayısının sütun isimleri (örneğin: ['female_2022', 'female_2023']).

    Returns:
        None
    """
    data = dataframe[dataframe.iloc[:, 0] == group_name]

    if data[male_cols].empty or data[female_cols].empty:
        print(f"Data for {group_name} or one of the columns is missing!")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(male_cols, data[male_cols].values.flatten(), label='Male', marker='o')
    plt.plot(female_cols, data[female_cols].values.flatten(), label='Female', marker='o')
    plt.title(f"Gender Change Over Years: {group_name}")
    plt.ylabel("Total Student Count")
    plt.xlabel("Years")
    plt.legend()
    plt.grid(True)
    plt.show()


# Fakülte bazlı cinsiyet değişimi analizi

faculty_analysis = gender_change_analysis(df, group_col='faculty_name')
# faculty_analysis.to_csv('faculty_gender_change_analysis.csv', index=False)

print("Fakülteler Bazında Cinsiyet Değişimi:")
print(faculty_analysis)


# Departman bazlı cinsiyet değişimi analizi
department_analysis = gender_change_analysis(df, group_col='department_name')
# department_analysis.to_csv('department_gender_change_analysis.csv', index=False)

print("Departmanlar Bazında Cinsiyet Değişimi:")
print(department_analysis)

"""
# Grafikle bir fakülteyi analiz etme
plot_gender_change(
    faculty_analysis,
    group_name="Elektrik-Elektronik Fakültesi",  # Specify an actual group
    male_cols=['total_male_number_2021', 'total_male_number_2022', 'total_male_number_2023'],
    female_cols = ['total_female_number_2021', 'total_female_number_2022', 'total_female_number_2023']

)

plot_gender_change(
    department_analysis,
    group_name="Matematik Mühendisliği",
    male_cols=['total_male_number_2021', 'total_male_number_2022', 'total_male_number_2023'],
    female_cols=['total_female_number_2021', 'total_female_number_2022', 'total_female_number_2023']
)

"""
# ############################################### college_gender_change_analysis

def analyze_gender_changes(data):

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


college_gender_change_analysis = analyze_gender_changes(df)
print("OKUL BAZINDA")

print(college_gender_change_analysis)

# college_gender_change_analysis.to_csv('department_gender_change_analysis.csv', index=False)

# ########################################################## TERCİH EDİLME KONTENJAN VE YERLEŞME ORANLARI

print("TERCİH EDİLME KONTENJAN VE YERLEŞME ORANLARI")


def analyze_academic_changes(data, group_by='department_name'):

    # Yerleşen öğrenci sayısını hesaplama
    data['placed_students'] = data['male'] + data['female']

    grouped_data = data.groupby(['year', group_by]).agg({
        'quota': 'sum',  # Kontenjan toplamı
        'preferred': 'sum',  # Tercih edilme toplamı
        'placed_students': 'sum'  # Yerleşen öğrenci toplamı
    }).reset_index()

    grouped_data['Quota Change'] = grouped_data.groupby(group_by)['quota'].diff()
    grouped_data['Preferred Change'] = grouped_data.groupby(group_by)['preferred'].diff()
    grouped_data['Placed Students Change'] = grouped_data.groupby(group_by)['placed_students'].diff()

    grouped_data['Quota Change (%)'] = grouped_data.groupby(group_by)['quota'].pct_change() * 100
    grouped_data['Preferred Change (%)'] = grouped_data.groupby(group_by)['preferred'].pct_change() * 100
    grouped_data['Placed Students Change (%)'] = grouped_data.groupby(group_by)['placed_students'].pct_change() * 100

    if group_by == 'department_name':
        grouped_data.sort_values(by=['department_name', 'year'], ascending=[True, True], inplace=True)
    else:
        grouped_data.sort_values(by=['faculty_name', 'year'], ascending=[True, True], inplace=True)

    return grouped_data


quota_preferred_placed = analyze_academic_changes(df, 'faculty_name')
print(quota_preferred_placed)

# quota_preferred_placed.to_csv('quota_preferred_placed_student_analysis.csv', index=False)

quota_preferred_placed_dep = analyze_academic_changes(df, 'department_name')
print(quota_preferred_placed_dep)

# quota_preferred_placed_dep.to_csv('department_quota_preferred_placed_student_analysis.csv', index=False)

# ##################################################  analyze_base_point_changes

print('NET karşılaştırması')


def analyze_base_point_changes(data, group_by='department_name', department_type=None):
    """
    TYT ve AYT başarılarını, correct answers ayrımı ile yıllara göre analiz eder.

    Args:
    - data (pd.DataFrame): Girdi veri çerçevesi.
    - group_by (str): Analiz için grup değişkeni ('department_name' veya 'faculty_name').
    - department_type (str, optional): Bölüm türü filtresi ('ea', 'söz', 'dil').

    Returns:
    - pd.DataFrame: Yıllık analiz tablosu, artış/azalış ve yüzdelik değişimlerle birlikte.
    """

    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8').upper()

    # Department type filtresi
    if department_type:
        normalized_department_type = normalize_string(department_type)
        data = data[data['department_type'].apply(lambda x: normalize_string(x) == normalized_department_type)].copy()

    # TYT ve AYT ile başlayan sütunları bulma
    tyt_columns = [col for col in data.columns if col.startswith('tyt')]
    ayt_columns = [col for col in data.columns if col.startswith('ayt')]
    ydt_columns = [col for col in data.columns if col.startswith('ydt')]

    # Eksik sütunlar varsa 0 ile doldurma
    for col in tyt_columns + ayt_columns + ydt_columns:
        if col not in data.columns:
            data[col] = 0

    # Correct answers ayrımı
    data.loc[:, 'tyt_correct_answer'] = data[tyt_columns].fillna(0).sum(axis=1)
    data.loc[:, 'ayt_correct_answer'] = data[ayt_columns].fillna(0).sum(axis=1)
    data.loc[:, 'ydt_correct_answer'] = data[ydt_columns].fillna(0).sum(axis=1)

    # Sütunların sayısal (numeric) veri türünde olduğunu kontrol et
    for col in tyt_columns + ayt_columns + ydt_columns:
        data.loc[:, col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

    # Base point ve correct answers ile ilgili analiz
    aggregation_function = 'mean' if group_by == 'faculty_name' else 'sum'

    grouped_data = data.groupby(['year', group_by]).agg({
        'success_order': aggregation_function,
        'base_point': aggregation_function,
        'tyt_correct_answer': aggregation_function,
        'ayt_correct_answer': aggregation_function,
        'ydt_correct_answer': aggregation_function
    }).reset_index()

    # Artış/Azalış hesaplama
    grouped_data['Success Order Change'] = grouped_data.groupby(group_by)['success_order'].diff().fillna(0)
    grouped_data['Base Point Change'] = grouped_data.groupby(group_by)['base_point'].diff().fillna(0)
    grouped_data['TYT Correct Answer Change'] = grouped_data.groupby(group_by)['tyt_correct_answer'].diff().fillna(0)
    grouped_data['AYT Correct Answer Change'] = grouped_data.groupby(group_by)['ayt_correct_answer'].diff().fillna(0)
    grouped_data['YDT Correct Answer Change'] = grouped_data.groupby(group_by)['ydt_correct_answer'].diff().fillna(0)

    # Yüzdelik değişim
    grouped_data['Base Point Change (%)'] = grouped_data.groupby(group_by)['base_point'].pct_change().fillna(0) * 100
    grouped_data['Success Order Change (%)'] = grouped_data.groupby(group_by)['success_order'].pct_change().fillna(0) * 100
    grouped_data['TYT Correct Answer Change (%)'] = grouped_data.groupby(group_by)['tyt_correct_answer'].pct_change().fillna(0) * 100
    grouped_data['AYT Correct Answer Change (%)'] = grouped_data.groupby(group_by)['ayt_correct_answer'].pct_change().fillna(0) * 100
    grouped_data['YDT Correct Answer Change (%)'] = grouped_data.groupby(group_by)['ydt_correct_answer'].pct_change().fillna(0) * 100
    print("HELP")
    # Success Order'ı css dosyasından alıyoruz (data'ya ekliyoruz)
    # data'dan diff ve pct_change hesaplanır, grouped_data'ya eklenir
    for col in tyt_columns + ayt_columns + ydt_columns:
        grouped_data[f'{col} Change'] = data.groupby(group_by)[col].diff().reset_index(drop=True)
        grouped_data[f'{col} Change (%)'] = (data.groupby(group_by)[col].pct_change() * 100).reset_index(drop=True)

    # Sıralama
    grouped_data.sort_values(by=[group_by, 'year'], ascending=[True, True], inplace=True)

    return grouped_data


# tyt_ayt_correct_answer_analysis = analyze_base_point_changes(df, group_by='department_name')
# print(tyt_ayt_correct_answer_analysis)

# tyt_ayt_correct_answer_analysis.to_csv('tyt_ayt_correct_answer_analysis.csv', index=False)

# #################################################################

ad = analyze_base_point_changes(df, department_type='say')
print(":(")
print(ad)