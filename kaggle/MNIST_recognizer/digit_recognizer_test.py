# -*- coding: utf-8 -*-

import unittest
import digit_recognizer as dr

class DigitDataProcessorTest(unittest.TestCase):

  def digit_data_processor(self):
    dr.DigitDataProcessor('./data/train02.csv')


class DigitClassifierTest(unittest.TestCase):

  def test_train(self):
    data_source = dr.DigitDataProcessor('./data/train02.csv')
    dc = dr.DigitClassifier(data_source)
    self.assertIsNone(dc.train())

  def test_score(self):
    data_source = dr.DigitDataProcessor('./data/train80.csv')
    dc = dr.DigitClassifier(data_source)
    dc.score()


