from math import pow, pi
import os, csv

def calcThreadTensileArea(thread):
    # calculate the tensile thread area
    # assuming english only
    tensile_area = pi / 4 * pow(thread['basic_diameter'] * 1 / thread['threads_per_inch'], 2)
    return tensile_area

def calcThreadShearArea(external_thread, internal_thread, engagement_length):
    # return a tuple, external & interal shear area
    external_thread_area =  pi * external_thread['threads_per_inch'] * engagement_length * internal_thread['max_minor_diameter'] * (1 / (2 * external_thread['threads_per_inch']) + 0.57735 * (external_thread['min_pitch_diameter'] - internal_thread['max_minor_diameter']))
    internal_thread_area =  pi * external_thread['threads_per_inch'] * engagement_length * external_thread['min_major_diameter'] * (1 / (2 * external_thread['threads_per_inch']) + 0.57735 * (external_thread['min_major_diameter'] - internal_thread['max_pitch_diameter']))
    return [external_thread_area, internal_thread_area]



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
