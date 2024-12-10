import sqlite3
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init

init(autoreset=True)
conn=sqlite3.connect("yokatlas.db")
cursor=conn.cursor()

order=int(input(Fore.CYAN +"""
Choose order
1.Genders for faculties
2.Prefered for faculties
3.Quota for faculties
4.Student Number for faculties
5.Total Student for faculties
6.Total Gender Percentages for faculties
7.Exchange Program for faculties
8.Academicians for faculties
9.Settlement for faculties
10.Quota Occupancy for faculties
11.Prefered Percentage in School for faculties
12.Cities for faculties
13.Regions for faculties
"""))

def genders_for_faculties(years,genders):
    for gender in genders:
        for year in years:
            year=int(year)
            table = PrettyTable()
            gender=gender.lower()
            if gender=="male":
                cursor.execute("""
                select faculty_name_en,round(CAST(SUM(male) AS FLOAT) / (CAST(SUM(male) AS FLOAT) + CAST(SUM(female) AS FLOAT)) * 100,2) as male_percentage 
                from departments left join genders on departments.id=department_id left join faculties on faculties.id=faculty_id where year=? 
                group by faculty_id order by male_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Male Percentage"]
            elif gender=="female":
                cursor.execute("""
                select faculty_name_en,round(CAST(SUM(female) AS FLOAT) / (CAST(SUM(male) AS FLOAT) + CAST(SUM(female) AS FLOAT)) * 100,2) as female_percentage 
                from departments left join genders on departments.id=department_id left join faculties on faculties.id=faculty_id where year=? 
                group by faculty_id order by female_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Female Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            gender=gender.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Percentage in {}".format(gender,year))
            print(table)
            print("\n\n")

def prefered_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,sum(prefered) as total_prefered from departments left join general_infos on departments.id=department_id 
        left join faculties on faculties.id=faculty_id where year=? group by faculty_id order by total_prefered desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Prefered"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered in {}".format(year))
        print(table)
        print("\n\n")

def quota_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,sum(quota) as total_quota from departments left join general_infos on departments.id=department_id 
        left join faculties on faculties.id=faculty_id where year=? group by faculty_id order by total_quota desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Quota"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota in {}".format(year))
        print(table)
        print("\n\n")

def student_number_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,sum(s_number) as total_student from departments left join general_infos on departments.id=department_id 
        left join faculties on faculties.id=faculty_id where year=? group by faculty_id order by total_student desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Student Number"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number in {}".format(year))
        print(table)
        print("\n\n")

def total_student_number_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,sum(total_number) as total_student from departments left join faculties on faculties.id=faculty_id 
        left join total_student_number on departments.id=department_id where year=? group by faculty_id order by total_student desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Total Student Number"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nTotal Student in {}".format(year))
        print(table)
        print("\n\n")

def total_genders_for_faculties(years,genders):
    for gender in genders:
        for year in years:
            year=int(year)
            table = PrettyTable()
            gender=gender.lower()
            if gender=="male":
                cursor.execute("""
                select faculty_name_en,round(cast(sum(male) as float) / (cast(sum(total_number) as float))*100,2) as male_percentage 
                from departments left join faculties on faculties.id=faculty_id left join total_student_number on departments.id=department_id 
                where year=? group by faculty_id order by male_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Male Percentage"]
            elif gender=="female":
                cursor.execute("""
                select faculty_name_en,round(cast(sum(female) as float) / (cast(sum(total_number) as float))*100,2) as female_percentage 
                from departments left join faculties on faculties.id=faculty_id left join total_student_number on departments.id=department_id 
                where year=? group by faculty_id order by female_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Female Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            gender=gender.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\nTotal {} Percentage in {}".format(gender,year))
            print(table)
            print("\n\n")

def exchange_program_for_faculties(years,types):
    for type in types:
        for year in years:
            year=int(year)
            table = PrettyTable()
            type=type.lower()
            if type=="incoming":
                cursor.execute("""
                select faculty_name_en,sum(incoming) as total_incoming from departments left join faculties on faculties.id=faculty_id 
                left join exchange_program on departments.id=department_id where year=? group by faculty_id order by total_incoming desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Incoming Number"]
            elif type=="leaving":
                cursor.execute("""
                select faculty_name_en,sum(leaving) as total_leaving from departments left join faculties on faculties.id=faculty_id 
                left join exchange_program on departments.id=department_id where year=? group by faculty_id order by total_leaving desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Leaving Number"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            type=type.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Student in {}".format(type,year))
            print(table)
            print("\n\n")

def academician_for_faculties(years,academicians):
    print(academicians)
    for academician in academicians:
        for year in years:
            year=int(year)
            table = PrettyTable()
            academician=academician.lower()
            if academician=="professor":
                cursor.execute("""
                select faculty_name_en, round(cast(sum(proffesor) as float) / (cast(sum(proffesor) as float) + cast(sum(assoc_prof) as float) + cast(sum(phd) as float))*100,2) as professor_percentage 
                from departments left join faculties on faculties.id=faculty_id left join academicians on departments.id=department_id where year=? group by faculty_id 
                order by professor_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Professor Percentage"]
            elif academician=="associate professor":
                cursor.execute("""
                select faculty_name_en, round(cast(sum(assoc_prof) as float) / (cast(sum(proffesor) as float) + cast(sum(assoc_prof) as float) + cast(sum(phd) as float))*100,2) as assoc_professor_percentage 
                from departments left join faculties on faculties.id=faculty_id left join academicians on departments.id=department_id where year=? group by faculty_id 
                order by assoc_professor_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "Associate Professor Percentage"]
            elif academician=="phd":
                cursor.execute("""
                select faculty_name_en, round(cast(sum(phd) as float) / (cast(sum(proffesor) as float) + cast(sum(assoc_prof) as float) + cast(sum(phd) as float))*100,2) as phd_percentage 
                from departments left join faculties on faculties.id=faculty_id left join academicians on departments.id=department_id where year=? group by faculty_id 
                order by phd_percentage desc;
                """, (year,))
                table.field_names = ["No","Faculty Name", "PHD Percentage"]

            output=cursor.fetchall()
    
            
            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            academician=academician.capitalize()
            print(Fore.GREEN+Style.BRIGHT+"\n\n{} Percentage in {}".format(academician,year))
            print(table)
            print("\n\n")

def settlement_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,round(cast(sum(s_number) as float) / (cast(sum(prefered) as float))*100,2) as settlement_percentage 
        from departments left join general_infos on departments.id=department_id left join faculties on faculties.id=faculty_id 
        where year=? group by faculty_id order by settlement_percentage desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Settlement Percentage"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nSettlement Percentage in {}".format(year))
        print(table)
        print("\n\n")

def quota_occupancy_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select faculty_name_en,round(cast(sum(s_number) as float) / (cast(sum(quota) as float))*100,2) as quota_occupancy 
        from departments left join general_infos on departments.id=department_id left join faculties on faculties.id=faculty_id 
        where year=? group by faculty_id order by quota_occupancy desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Quota Occupancy Percentage"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota Occupancy Percentage in {}".format(year))
        print(table)
        print("\n\n")

def prefered_percentage_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT faculty_name_en, ROUND(
        CAST(SUM(prefered) AS FLOAT) / (
            SELECT SUM(prefered) 
            FROM general_infos 
            WHERE year = ?
        ) * 100, 2) AS prefered_percentage
        FROM general_infos LEFT JOIN departments ON departments.id = department_id
        LEFT JOIN faculties ON faculties.id = faculty_id
        WHERE year = ? GROUP BY faculty_name_en ORDER BY prefered_percentage DESC;
        """, (year,year))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Prefered Percentage in School"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered Percentage in School in {}".format(year))
        print(table)
        print("\n\n")

def cities_for_faculties(cities,years):
    for city in cities:
        for year in years:
            city=city.capitalize()
            year=int(year)
            cursor.execute("""
            select faculty_name_en,sum(student_number) as total_student from departments left join faculties on faculties.id=faculty_id 
            left join student_cities on departments.id=department_id left join Cities on Cities.id=city where year=? and city_name=? 
            group by faculty_id order by total_student desc;
            """, (year,city))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Faculty Name", "Student Number"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number from {} in {}".format(city,year))
            print(table)
            print("\n\n")

def regions_for_faculties(regions,years):
    for region in regions:
        for year in years:
            region=region.capitalize()
            year=int(year)
            cursor.execute("""select region_name_en from Regions where id=?""",(region))
            region_name_en=cursor.fetchone()[0]
            cursor.execute("""
            select faculty_name_en,sum(student_number) as total_student from departments left join faculties on faculties.id=faculty_id 
            left join student_regions on departments.id=department_id left join Regions on Regions.id=region where year=? and region_name_en=? 
            group by faculty_id order by total_student desc;
            """, (year,region_name_en))

            output=cursor.fetchall()
            table = PrettyTable()
            table.field_names = ["No","Faculty Name", "Student Number"]

            for index, row in enumerate(output, start=1):
                table.add_row([index] + list(row))
            print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number from {} in {}".format(region_name_en,year))
            print(table)
            print("\n\n")


years=input(Fore.YELLOW+"\nSelect a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
if order==1: 
    genders=input(Fore.YELLOW+"\nSelect a gender(male,female)\nNote:You can choose more than one value, split with ','\n").split(",")
    genders_for_faculties(years,genders)
elif order==2:
    prefered_for_faculties(years)
elif order==3:
    quota_for_faculties(years)
elif order==4:
    student_number_for_faculties(years)
elif order==5:
    total_student_number_for_faculties(years)
elif order==6:
    genders=input(Fore.YELLOW+"\nSelect a gender(male,female)\nNote:You can choose more than one value, split with ','\n").split(",")
    total_genders_for_faculties(years,genders)
elif order==7:
    types=input(Fore.YELLOW+"\nSelect a type(incoming,leaving)\nNote:You can choose more than one value, split with ','\n").split(",")
    exchange_program_for_faculties(years,types)
elif order==8:
    academicians=input(Fore.YELLOW+"\nSelect a academician(professor,associate professor,phd)\nNote:You can choose more than one value, split with ','\n").split(",")
    academician_for_faculties(years,academicians)
elif order==9:
    settlement_for_faculties(years)
elif order==10:
    quota_occupancy_for_faculties(years)
elif order==11:
    prefered_percentage_for_faculties(years)
elif order==12:
    cities=input(Fore.YELLOW+"\nEnter city name\nNote:You can choose more than one value, split with ','\n").split(",")
    cities_for_faculties(cities,years)
elif order==13:
    regions=input(Fore.YELLOW+"\nSelect region(1.Marmara,2.Ege,3.Akdeniz,4.Karadeniz,5.İç Anadolu,6.Doğu Anadolu,7.Güneydoğu Anadolu)\nNote:You can choose more than one value, split with ','\n").split(",")
    regions_for_faculties(regions,years)

conn.close()