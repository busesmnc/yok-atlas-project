import pandas as pd
import matplotlib.pyplot as plt

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
