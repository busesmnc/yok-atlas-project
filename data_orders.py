import sqlite3
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init

init(autoreset=True)
conn=sqlite3.connect("yokatlas.db")
cursor=conn.cursor()
order=int(input("""Choose order\n1.Success Order for Departments\n2.Base Points for Departments\n3.Correct Answers for Departments\n"""))

def success_orders_for_departments(department_types,years):
    for d_type in department_types:
        for year in years:
            d_type=d_type.upper().strip()
            year=int(year)
            cursor.execute("""
            SELECT department_name, success_order
            FROM success_orders
            LEFT JOIN departments ON department_id = departments.id
            WHERE success_order != 0
            AND d_type = ?
            AND year = ?
            ORDER BY success_order
            """, (d_type, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Success Order"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nSucces orders for {} in {}".format(d_type,year))
            print(table)
            print("\n\n")


def base_points_for_departments(department_types,years):
    for d_type in department_types:
        for year in years:
            d_type=d_type.upper().strip()
            year=int(year)
            cursor.execute("""
            SELECT department_name, base_point
            FROM base_points
            LEFT JOIN departments ON department_id = departments.id
            WHERE base_point != 0.0
            AND d_type = ?
            AND year = ?
            ORDER BY base_point desc
            """, (d_type, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Base Point"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nBase Points for {} in {}".format(d_type,year))
            print(table)
            print("\n\n")

def correct_answers_for_departments(department_types,years):
    for d_type in department_types:
        for year in years:
            d_type=d_type.upper().strip()
            year=int(year)
            cursor.execute("""
            SELECT department_name,total_correct_answers FROM
            Combined_Correct_Answers left join departments on department_id=departments.id 
            where total_correct_answers>0.0 and d_type=? and year=? order by total_correct_answers desc;
            """, (d_type, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Correct Answers"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nCorrect Answers for {} in {}".format(d_type,year))
            print(table)
            print("\n\n")

if order==1:
    department_types=input("Select Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    years=input("Select a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
    success_orders_for_departments(department_types,years)
elif order==2:
    department_types=input("Select Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    years=input("Select a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
    base_points_for_departments(department_types,years)
elif order==3:
    department_types=input("Select Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    years=input("Select a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
    correct_answers_for_departments(department_types,years)
conn.close()