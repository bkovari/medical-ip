# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 22:18:18 2018

@author: Bence Kovari <bkovari93@gmail.com>

Script that moves healthy and nonhealthy Chest X-Ray images into the
corresponding subcategory folder based on the given disease label.

Prerequisite:
    /image folder with Chest X-Ray .png files

Disease label options with filecount:
    ALL                 51759
    Hernia              110
    Edema               628
    Emphysema           892
    Pneumonia           322
    Fibrosis            727
    Nodule              2705
    Pneumothorax        2194
    Mass                2139
    Cardiomegaly        1093
    Atelectasis         4215
    Effusion            3955
    Consolidation       1310
    Infiltration        9547
    Pleural_Thickening  1126
"""

import os
import shutil
import pandas
import time
import sys

# Control param
DISEASE_LABEL = 'ALL'

# Paths
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = ROOT_PATH + '\\image'
HEALTHY_IMAGES_PATH = ROOT_PATH + '\\healthy_chests'
NONHEALTHY_IMAGES_PATH = ROOT_PATH + '\\nonhealthy_chests_' + DISEASE_LABEL

if DISEASE_LABEL not in [
    'ALL',
    'Hernia',
    'Edema',
    'Emphysema',
    'Pneumonia',
    'Fibrosis',
    'Nodule',
    'Pneumothorax',
    'Mass',
    'Cardiomegaly',
    'Atelectasis',
    'Effusion,'
    'Consolidation',
    'Infiltration',
    'Pleural_Thickening'
]:
    sys.exit("Given label not found, exiting.")

fields = ['ImageName', 'FindingLabels']
image_data = pandas.read_csv(ROOT_PATH + '\\' + 'Data_Entry_2017.csv', usecols=fields)
healthy = image_data.loc[image_data['FindingLabels'] == 'No Finding']

if DISEASE_LABEL == 'ALL':
    non_healthy = image_data.loc[image_data['FindingLabels'] != 'No Finding']
else:
    non_healthy = image_data.loc[image_data['FindingLabels'] == DISEASE_LABEL]

assert healthy['ImageName'].count() + non_healthy['ImageName'].count() == image_data['ImageName'].count()

healthy_chest_files = healthy['ImageName'].tolist()
nonhealthy_chest_files = non_healthy['ImageName'].tolist()


def check_folder(path, filename_list):
    """
    Checks the completeness of a folder based on a given filelist.
    :param path: directory to be checked
    :param filename_list: name of the files
    :return:
        True: directory is complete
        False: directory is incomplete
    """
    if os.path.exists(path):
        if len(os.listdir(path)) == len(filename_list):
            print("Directory {} is complete, no changes.".format(path.split("\\")[-1]))
            return True
        else:
            print("Clearing {}".format(path.split("\\")[-1]))
            shutil.rmtree(path)
            os.mkdir(path)
    else:
        os.mkdir(path)
    return False


def copy_files(filename_list, source, destination):
    """
    Copies the given files from source to destination folder.
    :param filename_list: name of the files
    :param source: source directory
    :param destination: destination directory
    :return:
    """
    cnt = 0
    print("\nCopying files to {}".format(destination.split("\\")[-1]))
    start = time.time()
    for png in filename_list:
        shutil.copy(source + '\\' + png, destination);
        cnt += 1
        if cnt % 5000 == 0:
            print("Moved image {} of {}".format(cnt, len(filename_list)))
    elapsed = time.strftime("%M:%S", time.gmtime(time.time() - start))
    print("Image copying finished in {}".format(elapsed))


print("Checking folders structure..")

if check_folder(HEALTHY_IMAGES_PATH, healthy_chest_files) is False:
    copy_files(healthy_chest_files, IMAGES_PATH, HEALTHY_IMAGES_PATH)

if check_folder(NONHEALTHY_IMAGES_PATH, nonhealthy_chest_files) is False:
    copy_files(nonhealthy_chest_files, IMAGES_PATH, NONHEALTHY_IMAGES_PATH)

assert len(os.listdir(HEALTHY_IMAGES_PATH)) == len(healthy_chest_files) \
       and len(os.listdir(NONHEALTHY_IMAGES_PATH)) == len(nonhealthy_chest_files), \
       "File missing in destination folders, please rerun the script!"

print("Labeling done.")

# End of file
