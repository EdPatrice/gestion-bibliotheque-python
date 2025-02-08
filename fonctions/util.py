import os
import datetime

def choix_valide(choix: str, borne1: int, borne2: int) -> bool:    
    try: 
        choix = int(choix)
        if choix < borne1 or choix > borne2: 
            return False
    except ValueError: 
        return False
    return True

def clear_screen():
    os.system('cls')

def wait():
    input("\nPressez la touche ENTRER pour continuer...")

def get_date() -> datetime:
    return datetime.datetime.now()    

def add_days_to_date(initial_date: str, days_to_add: int) -> datetime:
    initial_date = initial_date.split('-')
    initial_date = datetime.datetime(int(initial_date[0]), int(initial_date[1]), int(initial_date[2]))
    return initial_date + datetime.timedelta(days_to_add)

def days_diff_between_dates(date1: str, date2: str) -> int: 
    import datetime
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1 = datetime.datetime(int(date1[0]),int(date1[1]),int(date1[2])).date()
    date2 = datetime.datetime(int(date2[0]),int(date2[1]),int(date2[2])).date()
    
    return (date1 - date2).days

def get_last_identity_id(filepath) -> int:
    with open(filepath, 'r') as f: 
        file_content = f.read()
    file_content = file_content.split('\n')

    if (len(file_content) - 1) < 2:
        return 0
    else:
        last_line = file_content[::-1][1]
        last_line = last_line.split(', ')
        last_id = last_line[0]
        return int(last_id)

def date_valide(date: str) -> bool:
    for element in date.split('-'):
        try: 
            int(element)            
        except ValueError:
            return False
        
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])


    if (month > 12):
        return False
    
    if month == 2: 
        if year % 4 == 0 and year % 100 != 0:
            if day > 29: 
                return False       
        else: 
            if day > 28: 
                return False
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31: 
            return False
    else: 
        if day > 30: 
            return False
    return True