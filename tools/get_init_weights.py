from random import shuffle
import numpy as np
import os
import cv2


def get_weight(class_num, pixel_count):
    W = 1 / np.log(pixel_count)
    W = class_num * W / np.sum(W)
    return W


def get_MeanStdWeight(class_num=3, size=(1080, 700)):
    image_path = "data/PV/image/train/"
    label_path = "data/PV/label/train/"

    namelist = os.listdir(image_path)
    """========如果提供的是txt文本，保存的训练集中的namelist=============="""
    # file_name = "../datasets/train.txt"
    # with open(file_name,"r") as f:
    #     namelist = f.readlines()
    #     namelist = [file[:-1].split(",") for file in namelist]
    """==============================================================="""

    MEAN = []
    STD = []
    pixel_count = np.zeros((class_num, 1))

    for i in range(len(namelist)):
        print(i, os.path.join(image_path, namelist[i]))

        image = cv2.imread(os.path.join(image_path, namelist[i]))[:, :, ::-1]
        image = cv2.resize(image, size, interpolation=cv2.INTER_NEAREST)
        print(image.shape)

        mean = np.mean(image, axis=(0, 1))
        std = np.std(image, axis=(0, 1))
        MEAN.append(mean)
        STD.append(std)

        label = cv2.imread(os.path.join(label_path, namelist[i]), 0)
        label = cv2.resize(label, size, cv2.INTER_LINEAR)

        label_uni = np.unique(label)
        for m in label_uni:
            pixel_count[m] += np.sum(label == m)

    MEAN = np.mean(MEAN, axis=0) / 255.0
    STD = np.mean(STD, axis=0) / 255.0

    weight = get_weight(class_num, pixel_count.T)
    print(MEAN)
    print(STD)
    print(weight)

    return MEAN, STD, weight


if __name__ == '__main__':
    get_MeanStdWeight()
