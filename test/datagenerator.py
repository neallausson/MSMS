# -*- coding: utf-8 -*-
"""generator.py

This module provides Classes and Function to parkour data from a FileManager
which contains infos about the dataset.

"""
import tensorflow.keras as keras
import numpy as np
import math

class DataLoader(keras.utils.Sequence):
    """DataLoader to parkour dataset

    Attributes:
        files (pd.DataFrame): DataFrame containings data pathes
        batch_size (int): Batch Size
        shuffle (bool): Suffle Dataset or Not
        validation (bool): Train or Validation Files
    """

    def __init__(self, file_manager, batch_size, shuffle=True, validation=True):
        """Init function for DataLoader class

        Args:
            files (pd.DataFrame): DataFrame containings data pathes
            batch_size (int): Batch Size
            shuffle (bool): Suffle Dataset or Not
            validation (bool): Train or Validation Files
        """
        self.files = file_manager.valid if validation else file_manager.train
        self.batch_size = batch_size
        self.shuffle = shuffle
        if self.shuffle: self.on_epoch_end()

    def on_epoch_end(self):
        """Executed when epoch ends (shuffle dataset)
        """
        if self.shuffle:
            self.files = self.files.sample(frac=1).reset_index(drop=True)

    def __len__(self):
        """Len function for DataLoader class (number of batches)
        """
        return math.ceil(self.files.shape[0] / self.batch_size)

    def __get_file(self, idx):
        """Get File from dataset by id

        Args:
            idx (int): File index

        Returns:
            (np.ndarray): Sample t-1 (1, 128, 32)
            (np.ndarray): Sample t   (1, 128, 32)
            (np.ndarray): Mouth      (20, 3)
        """
        data = np.load(self.files['path'][idx])
        return data['sample_t_1'], data['sample_t'], data['mouth']

    def __getitem__(self, idx):
        """Get Item from DataLoader

        Args:
            idx (int): Batch index

        Returns:
            (np.ndarray): Array of Sample t-1 (batch, 1, 128, 32)
            (np.ndarray): Array of Sample t   (batch, 1, 128, 32)
            (np.ndarray): Array of Mouth      (batch, 20, 3)
        """
        start   = idx * self.batch_size
        end     = min((idx + 1) * self.batch_size, self.files.shape[0])
        indexes = range(start, end)
        datas   = list(map(self.__get_file, indexes))

        X_t_1 = np.array([d[0] for d in datas], dtype=np.float32)
        X_t   = np.array([d[1] for d in datas], dtype=np.float32)
        X_t_1 = X_t_1.reshape((X_t_1.shape[0], 128, 32, 1))
        X_t   = X_t.reshape((    X_t.shape[0], 128, 32, 1))

        X = [X_t_1, X_t]
        Y = np.array([d[2] for d in datas], dtype=np.float32)
        return X, Y
