#!/usr/bin/env python3

import re

required_codes = {
    'byr', 'iyr', 'eyr', 'hgt',
    'hcl', 'ecl', 'pid'
}
optional_codes = {
    'cid'
}
valid_passports = 0
passport = {}


def evaluate_passport(passport):
    missing_keys = required_codes - passport.keys()
    return not missing_keys


with open('input.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if line == '':
            valid_passports += evaluate_passport(passport)
            passport = {}
            continue

        elements = line.split()
        for element in elements:
            code, value = element.split(':')

            # Validation rules
            if code == 'byr':
                if int(value) not in range(1920, 2002+1):
                    continue
            elif code == 'iyr':
                if int(value) not in range(2010, 2020+1):
                    continue
            elif code == 'eyr':
                if int(value) not in range(2020, 2030+1):
                    continue
            elif code == 'hgt':
                if value.endswith('cm'):
                    if int(value[:-2]) not in range(150, 193+1):
                        continue
                elif value.endswith('in'):
                    if int(value[:-2]) not in range(59, 76+1):
                        continue
                else:
                    continue
            elif code == 'hcl':
                if not re.match(r'^#[a-f\d]{6}$', value):
                    continue
            elif code == 'ecl':
                if 'ecl' in passport.keys():
                    continue
                elif value not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
                    continue
            elif code == 'pid':
                if not re.match(r'^\d{9}$', value):
                    continue
            elif code == 'cid':
                continue

            # Only add valid codes
            passport[code] = value

valid_passports += evaluate_passport(passport)
print(valid_passports)
