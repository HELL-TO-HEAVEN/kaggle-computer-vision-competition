# -*- coding: utf-8 -*-

# WIP - does not work for now
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# Add ability to read pqcuqet
import pyarrow.parquet as pq
import os
import pickle
import random
import numpy as np
import pandas as pd


# load_dotenv(find_dotenv())
# PATH_DATA_RAW = Path(os.getenv("PATH_DATA_RAW"))
# PATH_DATA_INTERIM = Path(os.getenv("PATH_DATA_INTERIM"))

# PATH_DATA_RAW = r'C:\Users\nasty\data-science\kaggle\bengali\data\raw'
# PATH_DATA_INTERIM = r'C:\Users\nasty\data-science\kaggle\bengali\data\interim'

PATH_DATA_RAW = Path('C:/Users/nasty/data-science/kaggle/bengali/data/raw')
PATH_DATA_INTERIM = Path('C:/Users/nasty/data-science/kaggle/bengali/data/interim')

# featherdir
FEATHERDIR = Path('C:/Users/nasty/data-science/kaggle/bengali/data/interim/feather/')

# Template train data image file variable to be updated. i.e. the ID part
TRAIN_FEATHER_FORM = 'train_image_data_ID.feather'

# Template test data image file variable to be updated. i.e. the ID part
TEST_FEATHER_FORM = 'test_image_data_ID.feather'

LABEL_PATH = 'train.csv'

DEFAULT_H, DEFAULT_W = 137, 236


def train2image(vector_image: pd.DataFrame):
    """
    Convert a vector matrix to an actual image.
    :return:
    """



def load_images(train_test):
    """
    Utility function to Load the images from both the location and return them
    :param train_test:
    :return:
    """

    # ???
    path_form = {
        'train': TRAIN_FEATHER_FORM,
        'test': TEST_FEATHER_FORM
    }[train_test]

    imgs_list = []

    # sequentially load all four files.
    for id in ['0', '1', '2', '3']:

        # Form the path of the files.
        path = FEATHERDIR / path_form.replace('ID', id)

        print('Loading', path)

        df = pd.read_feather(path)

        imgs = df.iloc[:, 1:].to_numpy()

        imgs_list.append(imgs)

    imgs_list = np.concatenate(imgs_list)

    imgs_list = imgs_list.reshape(-1, DEFAULT_H, DEFAULT_W)

    return imgs_list

def load_labels():
    """
    Utility function to load the labels from CSV and dump to numpy memory variables.
    :return:
    """
    labels = pd.read_csv(PATH_DATA_RAW / LABEL_PATH)
    labels = labels.iloc[:, 1:4].to_numpy()
    return labels

def dump_image_labels():
    """
     A combined function to load both trian and label?
    :return:
    """
    # Load all images into a variable.
    imgs = load_images('train')
    labels = load_labels()
    all_data = list(zip(imgs, labels))

    all_data.to_feather('PATH_DATA_INTERIM / all_feather_data.feather')
    return all_data

def split_train_test():
    """
    Shuffle split the train and test sets and save them to separate files in the interim path.
    :return:
    """
    all_data = dump_image_labels()
    _ = random.shuffle(all_data)
    data_size = len(all_data)
    train_size = int(data_size * 0.8)
    train_data = all_data[:train_size]
    val_data = all_data[train_size:]
    write_feather(train_data, 'PATH_DATA_INTERIM / train_data.feather')
    write_feather(val_data, 'PATH_DATA_INTERIM / val_data.feather')


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    split_train_test()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
