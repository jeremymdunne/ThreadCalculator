"""
materialdatReader.py
Reads and parses the .materialdat file extension
Author: Jeremy Dunne
Date: September, 2021
"""

# imports
import os
import csv

def readMaterialdat(file):
    in_file = open(file,'r')
    data = []
    dictReader = csv.DictReader(in_file)
    for a in dictReader:
        entry = {}
        for key in a:
            if key != 'material_name':
                entry[key] = float(a[key])
            else:
                entry[key] = a[key]
        data.append(entry)
    return data

def getMaterialdatFiles():
    material_files = []
    for file in os.listdir('./resources'):
        if file.endswith('.materialdat'):
            material_files.append(os.path.join('./resources',file))
    return material_files

if __name__ == '__main__':
    file = './resources/material_properties.materialdat'
    print(readMaterialdat(file))
    print(getMaterialdatFiles())
