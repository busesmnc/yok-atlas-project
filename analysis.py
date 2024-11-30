import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

csv_file_path = "yok_atlas_data.csv"

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

    # Yıllara göre toplamları gruplandır
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

# ##########################################################



