import math
import cv2
import os

import numpy
from matplotlib import pyplot as plt


def get_files(dir_path) -> dict:
    dir_list = os.listdir(dir_path)
    file_to_path_lookup = {}
    for file_name in dir_list:
        file_to_path_lookup[file_name] = f'{dir_path}/{file_name}'
    return file_to_path_lookup


def image_preprocessing(file_to_path_lookup: dict, dest_dir_path) -> list:
    dimensions = (256, 256)
    file_paths = []
    dir_list = os.listdir(dest_dir_path)
    for file_name, old_file_path in file_to_path_lookup.items():
        new_file_path = f'{dest_dir_path}/{file_name}'
        if dir_list.count(file_name) == 0:
            image = cv2.imread(old_file_path, cv2.IMREAD_COLOR)
            image = cv2.resize(image, dimensions, cv2.INTER_NEAREST)
            cv2.imwrite(new_file_path, image)
        file_paths.append(new_file_path)
    return file_paths


def generate_histogram(file_paths: list):
    images = []
    for file_path in file_paths:
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        cv2.cvtColor(image, cv2.COLOR_BGR2HSV, image)
        images.append(image)

    # hue bins followed by saturation bins
    hist_size = [12, 4]

    # hue range followed by saturation range
    hist_ranges = [0, 180, 0, 256]

    channels = [0, 1]

    hist = cv2.calcHist(images, channels, None, hist_size, hist_ranges, accumulate=False)
    print(f'shape: {hist.shape}')
    (col1, col2, col3, col4) = numpy.split(hist, 4, 1)
    plt.plot(col1, 'Red')
    plt.plot(col2, 'Green')
    plt.plot(col3, 'Blue')
    plt.plot(col4, 'Black')
    plt.xlabel('Hue Bin #')
    plt.ylabel('# of Pixels')
    plt.title('Pixels per Hue-Saturation Bin')
    plt.show()
