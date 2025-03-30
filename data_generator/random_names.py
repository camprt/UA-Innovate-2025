#! python3
# -*- coding: utf-8 -*-
import random
import string
from os.path import dirname, join

script_dir    = dirname(__file__)
names_dir     = join(script_dir, 'Names')

FirstNames    = join(names_dir, 'MaleFirstNames.txt')
MiddleNames   = join(names_dir, 'MiddleNames.txt')
LastNames     = join(names_dir, 'LastNames.txt')
CountyNames   = join(names_dir, 'CountyNames.txt')
PlaceNames    = join(names_dir, 'PlaceNames.txt')
StateNames    = join(names_dir, 'StateNames.txt')
CountryNames  = join(names_dir, 'CountryNames.txt')
CompanyNames  = join(names_dir, 'CompanyNames.txt')
StreetTypes   = join(names_dir, 'StreetTypes.txt')


def Number(start=0, end=100000):
    """
    Returns random integer between range of numbers
    """
    return random.randint(start, end)


def UpperChars(NoOfChars=2):
    """
    UpperChars(NoOfChars=2) Returns 2 random CAPITAL letters.
    """
    _char = ''
    for num in range(NoOfChars):
        _char += random.choice(string.ascii_uppercase)
    return _char


def rawCount(filename):
    """
    Function to get Line Count in txt files.
    rawcount('C:\A.txt') outputs integer value of count of lines.
    """
    with open(filename, 'rb') as f:
        lines = 1
        buf_size = 1024 * 1024
        read_f = f.raw.read

        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)
        return lines


def randomLine(filename):
    """
    Read the given text file and return a random line
    """
    num = int(random.uniform(0, rawCount(filename)))
    with open(filename, 'r', encoding="UTF-8") as f:
        for i, line in enumerate(f, 1):
            if i == num:
                break
    return line.strip('\n')


def First():
    return randomLine(FirstNames)


def Last():
    return randomLine(LastNames)


def Middle():
    return randomLine(MiddleNames)


def States():
    return randomLine(StateNames)


def Places():
    return randomLine(PlaceNames)


def County():
    return randomLine(CountyNames)


def Company():
    return randomLine(CompanyNames)


def Country():
    _Cc = randomLine(CountryNames)
    _Cc = _Cc.split('|')
    return _Cc[1]


def CountryCode():
    _Cc = randomLine(CountryNames)
    _Cc = _Cc.split('|')
    return _Cc[0]


def StateCode():
    return States().split(', ')[1]

def StreetType():
    return randomLine(StreetTypes)


def Full():
    """
    Returns a random First Name and Last Name combination
    """
    return ' '.join([First(), Last()])

def Address():
    """
    Returns a Random address in the Format:
    54F - Sauk, Middle, New Mexico, NM, 4292.
    """
    _door = str(Number(11, 99))
    #_zip  = str(Number(1000, 9999))
    #_adrs = ', '.join([Places(), County(), States(), _zip])
    #_adrs = _door + UpperChars(1) + ' - ' + _adrs + '.'
    _adrs = ' '.join([_door, Places(), StreetType()])
    return _adrs


def ShortAddress():
    """
    Returns a Short Random address in the Format:
    31 Outagamie, Wisconsin, WI, 8281
    """
    _door = str(Number(11, 99))
    _zip  = str(Number(1000, 9999))
    _adrs = ', '.join([County(), States(), _zip])
    _adrs = _door + ' ' + _adrs
    return _adrs

def Email(first_name, last_name):
    _init = first_name[0]
    _email = ''.join([_init, '.',last_name, "@email.com"])
    return _email

def create_date():
    """
    Generates a random date with numeric month and day.
    Format: 'MM/DD' (e.g., '03/15')
    """
    # Define the number of days in each month
    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    # Choose a random month (1-12)
    month = random.randint(1, 12)
    
    # Pick a random day based on the selected month
    day = random.randint(1, days_in_month[month])
    
    return f"yyyy{month:02}{day:02}"  # Format as MM/DD


def random_phone_number():
    """
    Generates a random US-style phone number in the format: (XXX) XXX-XXXX
    """
    area_code = random.randint(200, 999)  # Area codes don't start with 0 or 1
    central_office_code = random.randint(200, 999)  # First digit can't be 0 or 1
    line_number = random.randint(1000, 9999)  # 4-digit line number

    return f"{area_code}-{central_office_code}-{line_number}"

def generate_ssn():
    """
    Generates a random ssn in the format: AAA-GG-SSSS
    """
    area_code = random.randint(100, 999)  # Area codes don't start with 0 or 1
    central_office_code = random.randint(00, 99)  # First digit can't be 0 or 1
    line_number = random.randint(1000, 9999)  # 4-digit line number

    return f"{area_code}-{central_office_code}-{line_number}"

def generate_act_no():
    _letter = random.choice(string.ascii_uppercase)
    _number = random.randint(100000000, 999999999)
    return f"{_letter}{_number}"

if __name__ == '__main__':
    first_name = First()
    last_name = Last()
    street_address = Address()
    _city = County()
    _county = County()
    #state = same
    #_zip = find take state and search file "[state]_zip.txt"
    _birthday = create_date() # 
    _phone = random_phone_number()
    email_address = Email(first_name, last_name)
    _ssn = generate_ssn()
    act_no = generate_act_no()
    #act #s
    
    

    print(first_name,last_name, 
        '\nlives at', Address(),', STATE XXXXX',
        '\nEmail:', Email(first_name, last_name), 
        '\nBirthdate (yyyymmdd):', _birthday, 
        '\nphone number: ', _phone,
        '\nsocial: ', _ssn,
        '\nact no: ', act_no
        )
