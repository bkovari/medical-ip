# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 22:18:18 2018

@author: Bence Kovari <bkovari93@gmail.com>

Script that moves healthy and nonhealthy Chest X-Ray images into the
corresponding subcategory folder based on the given disease label.

Prerequisite:
    /image folder with Chest X-Ray .png files

Disease label options:
    ALL
    Hernia
    Edema
    Emphysema
    Pneumonia
    Fibrosis
    Nodule
    Pneumothorax
    Mass
    Cardiomegaly
    Atelectasis
    Effusion
    Consolidation
    Infiltration
    Pleural_Thickening
"""

import os
import shutil
import pandas
import time

# Control param
DISEASE_LABEL = 'ALL'

# Paths
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = ROOT_PATH + '\\image'
HEALTHY_IMAGES_PATH = ROOT_PATH + '\\healthy_chests'
NONHEALTHY_IMAGES_PATH = ROOT_PATH + '\\nonhealthy_chests_' + DISEASE_LABEL

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

try:
    os.mkdir(HEALTHY_IMAGES_PATH)
    os.mkdir(NONHEALTHY_IMAGES_PATH)
except FileExistsError:
    print("Clearing existing folders..")
    try:
        shutil.rmtree(HEALTHY_IMAGES_PATH)
        shutil.rmtree(NONHEALTHY_IMAGES_PATH)
    except Exception:
        pass
finally:
    os.mkdir(HEALTHY_IMAGES_PATH)
    os.mkdir(NONHEALTHY_IMAGES_PATH)


def copy_files(filename_list, source, destination):
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


copy_files(healthy_chest_files, IMAGES_PATH, HEALTHY_IMAGES_PATH)
copy_files(nonhealthy_chest_files, IMAGES_PATH, NONHEALTHY_IMAGES_PATH)

assert len(os.listdir(HEALTHY_IMAGES_PATH)) == len(healthy_chest_files) \
       and len(os.listdir(NONHEALTHY_IMAGES_PATH)) == len(nonhealthy_chest_files), \
       "File missing in destination folders, please rerun the script!"

print("All files copied successfully!")

# End of file
