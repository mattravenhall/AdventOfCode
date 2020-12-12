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
    missing_keys = required_codes - (passport.keys() - optional_codes)
    # print(f"{'INVALID' if missing_keys else 'VALID'}: {passport} - {missing_keys if missing_keys else None}")
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
            passport[code] = value

valid_passports += evaluate_passport(passport)
print(valid_passports)
