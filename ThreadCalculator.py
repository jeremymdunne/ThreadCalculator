from math import pow, pi
import os, csv

# TODO rename this
def calcThreadTensileArea(thread):
    # calculate the tensile thread area
    # assuming english only
    tensile_area = pi / 4 * pow(thread['basic_diameter'] - 0.9743 / thread['pitch'], 2)
    return tensile_area

def calcThreadShearArea(external_thread, internal_thread, engagement_length):
    # return a tuple, external & interal shear area
    external_thread_area =  pi * external_thread['pitch'] * engagement_length * internal_thread['max_minor_diameter'] * (1 / (2 * external_thread['pitch']) + 0.57735 * (external_thread['min_pitch_diameter'] - internal_thread['max_minor_diameter']))
    internal_thread_area =  pi * external_thread['pitch'] * engagement_length * external_thread['min_major_diameter'] * (1 / (2 * external_thread['pitch']) + 0.57735 * (external_thread['min_major_diameter'] - internal_thread['max_pitch_diameter']))
    return [external_thread_area, internal_thread_area]

def calcFailureThreadShearForce(external_thread, material):
    # shear uses 0.6 scalar
    dict = {}
    area = calcThreadTensileArea(external_thread)
    dict['area'] = area
    dict['yield_strength'] = area * 0.6 * material['yield_strength']
    dict['tensile_strength'] = area * 0.6 * material['tensile_strength']
    return dict

def calcFailureThreadTensileForce(external_thread, material):
    dict = {}
    area = calcThreadTensileArea(external_thread)
    dict['area'] = area
    dict['yield_strength'] = area * material['yield_strength']
    dict['tensile_strength'] = area * material['tensile_strength']
    return dict

def calcFailureThreadEngagement(external_thread, external_material, internal_thread, internal_material, engagement_length):
    dict = {}
    areas = calcThreadShearArea(external_thread, internal_thread, engagement_length)
    dict['internal_thread_area'] = areas[1]
    dict['external_thread_area'] = areas[0]

    dict['external_yield_strength'] = external_material['yield_strength'] * 0.6 * dict['external_thread_area']
    dict['external_tensile_strength'] = external_material['tensile_strength'] * 0.6 * dict['external_thread_area']

    dict['internal_yield_strength'] = internal_material['yield_strength'] * 0.6 * dict['internal_thread_area']
    dict['internal_tensile_strength'] = internal_material['tensile_strength'] * 0.6 * dict['internal_thread_area']

    return dict 


def getThreadData():
    thread_files = getThreadDataFiles()
    thread_data = {}
    for f in thread_files:
        # print(f)
        in_file = open(f,'r')
        data = []
        dict = csv.DictReader(in_file)
        for d in dict:
            entry = {}
            # print(d)
            for key in d:
                # print(key)
                if key != 'thread_class' and key != 'screw_size':
                    entry[key] = float(d[key])
                else:
                    entry[key] = d[key]
                # print(entry[key])
            data.append(entry)
        thread_data[f] = data
        in_file.close()
    # print(thread_data)

if __name__ == '__main__':
    import csv
