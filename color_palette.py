from collections import Counter

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import PIL
from sklearn.cluster import KMeans


def rgb_to_hex(rgb):
    rgb = [int(num) for num in rgb]
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]).upper()


def extract_colors(clusters):
    color_palette = {}

    n_pixels = len(clusters.labels_)  # no. of pixels
    counter = Counter(clusters.labels_)  # Count how many pixels per cluster
    counter = dict(sorted(counter.items()))  # sorting dictionary by idx
    perc = [float(np.round((counter[key] / n_pixels) * 100, 2)) for key in counter]  # Calculate percentage of each cluster

    # create list of rgb colors
    for idx, centers in enumerate(clusters.cluster_centers_):
        centers = rgb_to_hex(centers)
        color_palette[centers] = perc[idx]
    return dict(sorted(color_palette.items(), key=lambda item: item[1], reverse=True))

    # Display the image
    # plt.imshow(palette)
    # plt.axis('off')  # Hide the axis
    # plt.show()


def find_colors(image_filepath):
    # img = cv.imread("static/uploads/image.jpg")
    img = cv.imread(image_filepath)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # convert tp rgb colors

    # resize image
    dim = (500, 300)
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    # KMeans Algorithm
    # clusters n=10 for number of colors
    clt = KMeans(n_clusters=10, random_state=0)
    clt = clt.fit(img.reshape(-1, 3))
    color_list = extract_colors(clt)
    return [(hash_code, color) for hash_code, color in color_list.items()]

