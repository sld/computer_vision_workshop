# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import numpy.random as random
import matplotlib.pyplot as plt
from sklearn import neighbors, datasets, cross_validation
import cv2
import csv
import sys


class DigitClassifier:
  def __init__(self, data_source, k=10):
    self.data = data_source.data()
    self.__process_data()
    self.__make_classifier(k)

  def train(self):
    self.classifier.fit(self.feature_vectors, self.labels)

  def classify(self, feature_vectors):
    labels = self.classifier.predict(feature_vectors)
    return labels

  def score(self):
    vectors_train, vectors_test, labels_train, labels_test = cross_validation \
      .train_test_split(self.feature_vectors, self.labels, test_size=0.2, random_state=100)

    self.classifier.fit(vectors_train, labels_train)
    score = self.classifier.score(vectors_test, labels_test)
    return score

  def make_feature_vector(self, image):
    return image.flatten()


  def __process_data(self):
    self.labels = []
    self.feature_vectors = []
    for image_and_label in self.data:
      label = image_and_label[0]
      image = image_and_label[1]
      feature_vector = self.make_feature_vector(image)
      self.labels.append(label)
      self.feature_vectors.append(feature_vector)

  def __make_classifier(self, k):
    self.classifier = neighbors.KNeighborsClassifier(k)


class DigitDataProcessor:

  def __init__(self, csv_file, is_train=True, thresh_val=233):
    self.pandas_data = pd.read_csv(csv_file)
    self.thresh_val = thresh_val
    self.is_train = is_train
    self.__process_data()

  # Format: [[label, image], ...]
  def data(self):
    return self.processed_data


  def __process_data(self):
    self.__make_processed_data()

  def __make_processed_data(self):
    self.processed_data = []
    for arr in self.pandas_data.values:
      label, image = self.__get_label_and_image(arr)
      self.processed_data.append([label, self.__process_image(image)])

  def __process_image(self, image):
    image = image.astype(np.uint8).reshape(28,28)
    # resized = cv2.resize(image, (10,10))
    # ret, thresholded = cv2.threshold(image, self.thresh_val, 255, cv2.THRESH_BINARY)
    return image

  def __get_label_and_image(self, arr):
    if self.is_train:
      return [arr[0], arr[1:]]
    else:
      return [0, arr[0:]]


class Runner:

  def cross_validation(self):
    train_data_source = DigitDataProcessor('./data/train.csv')
    dc = DigitClassifier(train_data_source)
    print dc.score()

  def make_what_kaggle_needs(self):
    # Training classifier
    train_data_source = DigitDataProcessor('./data/train.csv')
    dc = DigitClassifier(train_data_source, 10)
    dc.train()

    print "After Train!"

    # Predicting values
    test_data_source = DigitDataProcessor('./data/test.csv', False)
    images = [label_and_image[1] for label_and_image in test_data_source.data()]
    feature_vectors = [dc.make_feature_vector(image) for image in images]
    labels = dc.classify(feature_vectors)

    print "After Classifying!"

    c = csv.writer(open("./predict2.csv", "wb"))
    c.writerow(["ImageId", "Label"])
    for index, label in enumerate(labels):
      c.writerow([index+1, label])


Runner().make_what_kaggle_needs()
