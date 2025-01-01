import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
import seaborn as sns

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


