from os import path as osp

import numpy as np

from model import DeepLab
from tqdm import trange
from utils import (Dataset, Iterator, save_load_means, subtract_channel_means,
                   validation_single_demo_collage)

import time
import cv2

if __name__ == '__main__':

    data_dir = '/content/Data_Camera_SanTennis_Labeled/'
    testset_filename = osp.join(data_dir, 'valid.txt')
    images_dir = osp.join(data_dir, 'RGBs/')
    labels_dir = osp.join(data_dir, 'Labels/')
    demo_dir = 'data/demos/deeplab/resnet_101_voc2012/'
    models_dir = '/content/drive/MyDrive/Colab Notebooks/RobotNhatBongTennis2021/Models/'
    model_filename = 'resnet_101_0.7076.ckpt'

    channel_means = save_load_means(means_filename='channel_means.npz', image_filenames=None)

    minibatch_size = 16

    test_dataset = Dataset(dataset_filename=testset_filename, images_dir=images_dir, labels_dir=labels_dir, image_extension='.png', label_extension='.png')
    test_iterator = Iterator(dataset=test_dataset, minibatch_size=minibatch_size, process_func=None, random_seed=None, scramble=False, num_jobs=1)

    deeplab = DeepLab('resnet_101', training=False, num_classes=5)
    deeplab.load(osp.join(models_dir, model_filename))

    n_samples = 1000
    for i in trange(n_samples):
        image, label = test_iterator.next_raw_data()
        # image_input = subtract_channel_means(image=image, channel_means=channel_means)
        image = cv2.resize(image, (256, 256))

        output = deeplab.test(inputs=[image], target_height=image.shape[0], target_width=image.shape[1])[0]

        # validation_single_demo_collage(image, np.squeeze(label, axis=-1), np.argmax(output, axis=-1), demo_dir, str(i))

    n_test = 10000
    sum_time = 0
    log_time = ""
    for i in range(n_test):
        t = time.time()
        image, label = test_iterator.next_raw_data()
        # image_input = subtract_channel_means(image=image, channel_means=channel_means)
        image = cv2.resize(image, (256, 256))

        output = deeplab.test(inputs=[image], target_height=image.shape[0], target_width=image.shape[1])[0]
        t = time.time() - t
        log_time += str(t) + ","
        print(t)
        sum_time += t

    avg_time = sum_time/n_test
    print(avg_time)

    dir_log = open("/content/drive/MyDrive/Colab Notebooks/RobotNhatBongTennis2021/Models/log_resnet_101.txt", "w")
    dir_log.write(log_time)
    dir_log.close()

    deeplab.close()
