import numpy as np
from itertools import repeat
import cv2
import os
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


def generate_histogram(file_paths: list, title, dest_dir_path):
    # read in images
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

    # calculate histogram
    hist = cv2.calcHist(images, channels, None, hist_size, hist_ranges, accumulate=False)

    # create inputs to 3d bar chart
    x_edges = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    y_edges = np.array([1, 2, 3, 4])
    x_pos, y_pos = np.meshgrid(x_edges * 2, y_edges, indexing='ij')
    x_pos = x_pos.ravel()
    y_pos = y_pos.ravel()
    dx = list(repeat(1.5, 48))
    dy = list(repeat(0.5, 48))
    dz = hist.ravel()
    max_val = dz.max()
    min_val = dz.min()

    # map colors
    color_map = plt.cm.get_cmap('jet')
    colors = [color_map((val - min_val)/max_val) for val in dz]

    # create and display figure
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.tick_params(axis='both', which='both', labelsize=8)
    ax.bar3d(x_pos, y_pos, 0, dx, dy, dz, color=colors)
    plt.xticks(x_edges[::2] * 2, x_edges[::2])
    sat_labels = [f'Level {level}' for level in y_edges]
    plt.yticks(y_edges + 0.25, sat_labels)
    plt.title(f'{title} Pixels per Hue-Saturation Bin')
    plt.xlabel('Hue Bin Number')
    plt.ylabel('Saturation Level', labelpad=10)
    plt.savefig(dest_dir_path)
    plt.show()


