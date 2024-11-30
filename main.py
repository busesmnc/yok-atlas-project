import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# df = pd.DataFrame(data, columns=columns_for_genders)
csv_file_path = "general_data.csv"

# CSV dosyasını DataFrame'e dönüştür
df = pd.read_csv(csv_file_path)
# df.to_csv('yok_atlas_veri.csv', index=False)  # 'index=False', satır numaralarını CSV'ye dahil etmez
# print(data)
# print(df)

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
# print(df.head())
# print(df.info())

""""""
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

# print(cat_cols)
# print(num_cols)
# print(cat_but_car)


num_cols = ["total_male_number", "total_female_number"]

print("toplam cinsiyet sayısı")

def target_summary_with_num(dataframe, target, numerical_col, year):
    print(f"year: {year} için {numerical_col} ortalamaları")
    filtered_df = dataframe[dataframe["year"] == year]  # Filter dataframe by year
    print(filtered_df.groupby(target).agg({numerical_col: "sum"}), end="\n\n\n")


# Loop through the column names and call the function
for col in num_cols:
    print(f"{col} için fakülte ortalama cinsiyet sayısı:")
    target_summary_with_num(df, 'faculty_name', col, 2023)


print("yıllık ortalama cinsiyet sayısı")
for col in num_cols:
    target_summary_with_num(df, 'year', col, 2023)


"""
# outlier check
""" 

# print("OUTLIER")


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


for col in num_cols:
   print(col, check_outlier(df, col))
"""

print("cinsiyet oranı hesaplama")
import pandas as pd

def calculate_gender_ratio(df, group_by_column):

    # Verilen sütuna göre gruplama ve cinsiyet bazlı toplamları hesapla
    grouped = df.groupby(group_by_column).agg(
        total_students=('total_student_number', 'sum'),
        total_males=('total_male_number', 'sum'),
        total_females=('total_female_number', 'sum')
    )

    # Cinsiyet yüzdelerini hesapla
    grouped['male_ratio'] = (grouped['total_males'] / grouped['total_students']) * 100
    grouped['female_ratio'] = (grouped['total_females'] / grouped['total_students']) * 100

    return grouped[['male_ratio', 'female_ratio']]

print("Fakülte bazlı cinsiyet oranı")
# Fakülte bazlı cinsiyet oranı
faculty_gender_ratios = calculate_gender_ratio(df, 'faculty_name')
print("Fakülte bazlı cinsiyet oranları:")
print(faculty_gender_ratios)

print("Departman bazlı cinsiyet oranı")
# Departman bazlı cinsiyet oranı
department_gender_ratios = calculate_gender_ratio(df, 'department_name')
print("\nDepartman bazlı cinsiyet oranları:")
print(department_gender_ratios)


def calculate_overall_gender_percentage(dataframe, year_filter):

    if year_filter is not None:
        dataframe = dataframe.loc[dataframe['year'] == year_filter]

    total_male = dataframe['total_male_number'].sum()
    total_female = dataframe['total_female_number'].sum()
    total_students = dataframe['total_student_number'].sum()

    male_percentage = (total_male / total_students) * 100
    female_percentage = (total_female / total_students) * 100

    return {
        "total_male": total_male,
        "total_female": total_female,
        "total_students": total_students,
        "male_percentage": male_percentage,
        "female_percentage": female_percentage
    }


overall_percentage = calculate_overall_gender_percentage(df, 2023)

print("YTU GENDER STATISTICS:")
print(f"Total male student number: {overall_percentage['total_male']}")
print(f"Total female student number: {overall_percentage['total_female']}")
print(f"Total student number: {overall_percentage['total_students']}")
print(f"Male percentage: {overall_percentage['male_percentage']:.2f}%")
print(f"Female percentage: {overall_percentage['female_percentage']:.2f}%")


# ### VISUALIZATION


def plot_gender_trends_bar(df, department_name):
    department_data = df[df['department_name'] == department_name]

    department_data_yearly = department_data.groupby('year').agg(
        total_male=('total_male_number', 'sum'),
        total_female=('total_female_number', 'sum')
    ).reset_index()

    # Bar Grafiği
    department_data_yearly.set_index('year', inplace=True)
    department_data_yearly.plot(kind='bar', figsize=(10, 6), stacked=True)

    # Başlık ve etiketler
    plt.title(f'{department_name} department yearly gender ratio', fontsize=14)
    plt.xlabel('Yıl', fontsize=12)
    plt.ylabel('Student Number', fontsize=12)
    plt.tight_layout()
    plt.show()


# Örnek kullanım:
plot_gender_trends_bar(df, 'Bilgisayar Mühendisliği')


def plot_gender_trends(df, level='department', name=None):

    if level == 'department':
        filtered_data = df[df['department_name'] == name]
    elif level == 'faculty':
        filtered_data = df[df['faculty_name'] == name]
    else:
        raise ValueError("Seçilen düzey geçerli değil! Lütfen 'department' veya 'faculty' seçin.")

    filtered_data_yearly = filtered_data.groupby('year').agg(
        total_male=('total_male_number', 'sum'),
        total_female=('total_female_number', 'sum')
    ).reset_index()

    plt.figure(figsize=(10, 6))

    plt.plot(filtered_data_yearly['year'], filtered_data_yearly['total_male'], label='Erkek Öğrenciler', marker='o')

    plt.plot(filtered_data_yearly['year'], filtered_data_yearly['total_female'], label='Kadın Öğrenciler', marker='o')

    title = f"{name} {level.capitalize()} Yearly Gender Distribution"
    plt.title(title, fontsize=14)
    plt.xlabel('Yıl', fontsize=12)
    plt.ylabel('Student Number', fontsize=12)
    plt.legend()

    plt.grid(True)
    plt.xticks(filtered_data_yearly['year'], rotation=45)
    plt.tight_layout()
    plt.show()
"""
