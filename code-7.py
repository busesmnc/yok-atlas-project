import pandas as pd
import unicodedata

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

csv_file_path = "YTU_General_Data.csv"
df = pd.read_csv(csv_file_path)


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
# dep_change.to_csv("ytu_department_yearly_per_change.csv")


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
# fac_change.to_csv("ytu_faculty_yearly_per_change.csv")


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

