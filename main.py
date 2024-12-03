import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import unicodedata

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# df = pd.DataFrame(data, columns=columns_for_genders)
csv_file_path = "gen_data.csv"
csv_file_path_city = "department_city_student_counts.csv"

# CSV dosyasını DataFrame'e dönüştür
df = pd.read_csv(csv_file_path)
df_city = pd.read_csv(csv_file_path_city)
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


# yearly_change_dep = department_general_analysis(df)
# print(yearly_change_dep)


# yearly_change_fac = faculty_analysis(df, year=2022)
# print(yearly_change_fac)


# yearly_change_ytu = year_analysis(df)
# print(yearly_change_ytu)


selected_cols = ['total_male_number',
                          'total_female_number', 'total_student_number_', 'professors',
                          'assoc_prof', 'phd', 'base_point', 'success_order', 'preferred',
                          'quota', 'placed_number', 'tyt_turkce', 'tyt_matematik', 'tyt_fen',
                          'tyt_sosyal', 'ayt_matematik', 'ayt_fizik', 'ayt_kimya', 'ayt_biyoloji',
                          'ayt_edebiyat', 'ayt_cografya1', 'ayt_cografya2', 'ayt_din',
                          'ayt_felsefe', 'ayt_tarih1', 'ayt_tarih2', 'ydt_yabanci_dil', 'Marmara',
                          'Ege', 'Akdeniz', 'Karadeniz', 'Ic_Anadolu', 'Dogu_Anadolu',
                          'Guney_Dogu_Anadolu']

for i in selected_cols:
    outl = check_outlier(df, i)
    if outl:
        print(i)

