import sqlite3
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init

init(autoreset=True)
conn=sqlite3.connect("yokatlas.db")
cursor=conn.cursor()
order=int(input(Fore.CYAN +"""
Choose order
1.Success Order for Departments
2.Base Points for Departments
3.Correct Answers for Departments
4.Genders for Departments
5.Prefered for Departments
6.Quota for Departments
7.Student Number for Departments
8.Total Student for Departments
9.Total Gender Percentages for Departments
10.Exchange Program for Departments
11.Academicians for Departments
12.Settlement for Departments
13.Quota Occupancy for Departments
14.Prefered Percentage in School for Departments
15.Cities for Departments
16.Regions for Departments
"""))

def success_orders_for_departments(department_types,years):
    for d_type in department_types:
        for year in years:
            d_type=d_type.upper().strip()
            d_type = "DİL" if d_type == "DIL" else d_type
            year=int(year)
            cursor.execute("""
            SELECT department_name_en, success_order
            FROM success_orders
            LEFT JOIN departments ON department_id = departments.id
            WHERE success_order != 0
            AND d_type = ?
            AND year = ?
            ORDER BY success_order
            limit 5
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
            d_type = "DİL" if d_type == "DIL" else d_type
            year=int(year)
            cursor.execute("""
            SELECT department_name_en, base_point
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
            d_type = "DİL" if d_type == "DIL" else d_type
            year=int(year)
            cursor.execute("""
            SELECT department_name_en,total_correct_answers FROM
            Combined_Correct_Answers left join departments on department_id=departments.id 
            where total_correct_answers>0.0 and d_type=? and year=? order by total_correct_answers desc limit 5;
            """, (d_type, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Correct Answers"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nCorrect Answers for {} in {}".format(d_type,year))
            print(table)
            print("\n\n")

def genders_for_departments(years,genders):
    for gender in genders:
        for year in years:
            year=int(year)
            table = PrettyTable()
            gender=gender.lower()
            if gender=="male":
                cursor.execute("""
                SELECT department_name_en, male_percentage from genders 
                left join departments on departments.id=department_id 
                where year=? order by male_percentage desc;
                """, (year,))
                table.field_names = ["No","Department Name", "Male Percentage"]
            elif gender=="female":
                cursor.execute("""
                SELECT department_name_en, female_percentage from genders 
                left join departments on departments.id=department_id 
                where year=? order by female_percentage desc;
                """, (year,))
                table.field_names = ["No","Department Name", "Female Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            gender=gender.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Percentage in {}".format(gender,year))
            print(table)
            print("\n\n")

def prefered_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT department_name_en,prefered from general_infos LEFT JOIN 
        departments on departments.id=department_id where year=? order by prefered desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Prefered"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered in {}".format(year))
        print(table)
        print("\n\n")

def quota_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT department_name_en,quota from general_infos LEFT JOIN 
        departments on departments.id=department_id where year=? order by quota desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Quota"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota in {}".format(year))
        print(table)
        print("\n\n")

        
def student_number_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT department_name_en,s_number from general_infos LEFT JOIN 
        departments on departments.id=department_id where year=? order by s_number desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Student Number"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number in {}".format(year))
        print(table)
        print("\n\n")

def total_student_number_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select department_name_en,total_number from total_student_number 
        left join departments on departments.id=department_id 
        where year=? order by total_number desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Total Student Number"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nTotal Student in {}".format(year))
        print(table)
        print("\n\n")


def total_genders_for_departments(years,genders):
    for gender in genders:
        for year in years:
            year=int(year)
            table = PrettyTable()
            gender=gender.lower()
            if gender=="male":
                cursor.execute("""
                SELECT department_name_en, 
                ROUND(CAST(male as float)/(cast(total_number as float))*100,2) as male_percentage  
                from total_student_number left join departments on departments.id=department_id 
                where total_number!=0 and year=? order by male_percentage desc;
                """, (year,))
                table.field_names = ["No","Department Name", "Male Percentage"]
            elif gender=="female":
                cursor.execute("""
                SELECT department_name_en, 
                ROUND(CAST(female as float)/(cast(total_number as float))*100,2) as female_percentage  
                from total_student_number left join departments on departments.id=department_id 
                where total_number!=0 and year=? order by female_percentage desc;
                """, (year,))
                table.field_names = ["No","Department Name", "Female Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            gender=gender.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\nTotal {} Percentage in {}".format(gender,year))
            print(table)
            print("\n\n")

def exchange_program_for_departments(years,types):
    for type in types:
        for year in years:
            year=int(year)
            table = PrettyTable()
            type=type.lower()
            if type=="incoming":
                cursor.execute("""
                SELECT 
                    TRIM(
                        CASE 
                            WHEN department_name_en like '%(English)%' THEN 
                                REPLACE(department_name_en, '(English)', '')  
                            ELSE department_name_en
                        END
                    ) AS normalized_department_name,
                    SUM(incoming) AS incoming_student
                FROM departments
                LEFT JOIN exchange_program as ep ON departments.id = ep.department_id
                WHERE ep.year = ?
                GROUP BY normalized_department_name
                ORDER BY incoming_student DESC
                LIMIT 5;
                """, (year,))
                table.field_names = ["No","Department Name", "Incoming Number"]
            elif type=="leaving":
                cursor.execute("""
                SELECT 
                    TRIM(
                        CASE 
                            WHEN department_name_en like '%(English)%' THEN 
                                REPLACE(department_name_en, '(English)', '')  -- Removes the "(İngilizce)" part
                            ELSE department_name_en
                        END
                    ) AS normalized_department_name,
                    SUM(leaving) AS leaving_student
                FROM departments
                LEFT JOIN exchange_program as ep ON departments.id = ep.department_id
                WHERE ep.year = ?
                GROUP BY normalized_department_name
                ORDER BY leaving_student DESC
                LIMIT 5;
                """, (year,))
                table.field_names = ["No","Department Name", "Leaving Number"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            type=type.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Student in {}".format(type,year))
            print(table)
            print("\n\n")

def academician_for_departments(years,academicians):
    print(academicians)
    for academician in academicians:
        for year in years:
            year=int(year)
            table = PrettyTable()
            academician=academician.lower()
            if academician=="professor":
                cursor.execute("""
                SELECT department_name_en, ROUND(CAST(proffesor AS FLOAT) / (CAST(proffesor AS FLOAT) + CAST(assoc_prof AS FLOAT) + CAST(phd AS FLOAT)) * 100, 2) AS professor_percentage
                FROM academicians left JOIN departments on departments.id=department_id where year=?
                ORDER BY professor_percentage DESC;
                """, (year,))
                table.field_names = ["No","Department Name", "Professor Percentage"]
            elif academician=="associate professor":
                cursor.execute("""
                SELECT department_name_en, ROUND(CAST(assoc_prof AS FLOAT) / (CAST(proffesor AS FLOAT) + CAST(assoc_prof AS FLOAT) + CAST(phd AS FLOAT)) * 100, 2) AS assoc_professor_percentage
                FROM academicians left JOIN departments on departments.id=department_id where year=?
                ORDER BY assoc_professor_percentage DESC;
                """, (year,))
                table.field_names = ["No","Department Name", "Associate Professor Percentage"]
            elif academician=="phd":
                cursor.execute("""
                SELECT department_name_en, ROUND(CAST(phd AS FLOAT) / (CAST(proffesor AS FLOAT) + CAST(assoc_prof AS FLOAT) + CAST(phd AS FLOAT)) * 100, 2) AS phd_percentage
                FROM academicians left JOIN departments on departments.id=department_id where year=?
                ORDER BY phd_percentage DESC;
                """, (year,))
                table.field_names = ["No","Department Name", "PHD Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            academician=academician.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Percentage in {}".format(academician,year))
            print(table)
            print("\n\n")

def settlement_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select department_name_en, ROUND(CAST(s_number as float)/(cast(prefered as float))*100,2) as settlement_percentage 
        from general_infos left join departments on departments.id=department_id where year=? 
        order by settlement_percentage desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Settlement Percentage"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nSettlement Percentage in {}".format(year))
        print(table)
        print("\n\n")

def quota_occupancy_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select department_name_en, ROUND(CAST(s_number as float)/(cast(quota as float))*100,2) as quota_occupancy 
        from general_infos left join departments on departments.id=department_id where year=? order by quota_occupancy desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Quota Occupancy Percentage"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota Occupancy Percentage in {}".format(year))
        print(table)
        print("\n\n")

def prefered_percentage_for_departments(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT department_name_en, 
        ROUND(CAST(prefered AS FLOAT) / (
            SELECT SUM(prefered) 
            FROM general_infos 
            WHERE year = ?) * 100, 2) AS prefered_percentage
        FROM general_infos LEFT JOIN departments ON departments.id = department_id 
        WHERE year =? GROUP BY department_name_en ORDER BY prefered_percentage DESC;
        """, (year,year))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Department Name", "Prefered Percentage in School"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered Percentage in School in {}".format(year))
        print(table)
        print("\n\n")

def cities_for_departments(cities,years):
    for city in cities:
        for year in years:
            city=city.capitalize()
            year=int(year)
            cursor.execute("""
            select department_name_en,student_number from student_cities left join departments on departments.id=department_id 
            left join Cities on city=Cities.id where city_name=? and year=? order by student_number desc;
            """, (city, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Student Number"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number from {} in {}".format(city,year))
            print(table)
            print("\n\n")

def regions_for_departments(regions,years):
    for region in regions:
        for year in years:
            region=region.capitalize()
            year=int(year)
            cursor.execute("""select region_name_en from Regions where id=?""",(region))
            region_name_en=cursor.fetchone()[0]
            cursor.execute("""
            select department_name_en,student_number from student_regions left join departments on departments.id=department_id 
            left join Regions on region=Regions.id where region_name_en=? and year=? order by student_number desc;
            """, (region_name_en, year))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Department Name", "Student Number"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number from {} in {}".format(region_name_en,year))
            print(table)
            print("\n\n")

years=input(Fore.YELLOW+"\nSelect a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
if order==1:
    department_types=input(Fore.YELLOW+"\nSelect Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    success_orders_for_departments(department_types,years)
elif order==2:
    department_types=input(Fore.YELLOW+"\nSelect Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    base_points_for_departments(department_types,years)
elif order==3:
    department_types=input(Fore.YELLOW+"\nSelect Department Type(SAY,SÖZ,EA,DİL)\nNote:You can choose more than one value, split with ','\n").split(",")
    correct_answers_for_departments(department_types,years)
elif order==4: 
    genders=input(Fore.YELLOW+"\nSelect a gender(male,female)\nNote:You can choose more than one value, split with ','\n").split(",")
    genders_for_departments(years,genders)
elif order==5:
    prefered_for_departments(years)
elif order==6:
    quota_for_departments(years)
elif order==7:
    student_number_for_departments(years)
elif order==8:
    total_student_number_for_departments(years)
elif order==9:
    genders=input(Fore.YELLOW+"\nSelect a gender(male,female)\nNote:You can choose more than one value, split with ','\n").split(",")
    total_genders_for_departments(years,genders)
elif order==10:
    types=input(Fore.YELLOW+"\nSelect a type(incoming,leaving)\nNote:You can choose more than one value, split with ','\n").split(",")
    exchange_program_for_departments(years,types)
elif order==11:
    academicians=input(Fore.YELLOW+"\nSelect a academician(professor,associate professor,phd)\nNote:You can choose more than one value, split with ','\n").split(",")
    academician_for_departments(years,academicians)
elif order==12:
    settlement_for_departments(years)
elif order==13:
    quota_occupancy_for_departments(years)
elif order==14:
    prefered_percentage_for_departments(years)
elif order==15:
    cities=input(Fore.YELLOW+"\nEnter city name\nNote:You can choose more than one value, split with ','\n").split(",")
    cities_for_departments(cities,years)
elif order==16:
    regions=input(Fore.YELLOW+"\nSelect region(1.Marmara,2.Ege,3.Akdeniz,4.Karadeniz,5.İç Anadolu,6.Doğu Anadolu,7.Güneydoğu Anadolu)\nNote:You can choose more than one value, split with ','\n").split(",")
    regions_for_departments(regions,years)

conn.close()