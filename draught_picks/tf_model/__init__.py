"""
__init__.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jake

Setup k means clustering.
"""

#import os
##import tensorflow as tf
#import numpy as np
#
#from django.conf import settings as s
#
#from beers.models import BeerLearning
#
#NUM_CLUSTERS = 8
#
#
#class TFModelException(Exception):
#    def __init__(self):
#        super().__init__("No existing Tensorflow model found.")
#
#
#model_path = os.path.join(s.BASE_DIR, 'tf_model/model')
#
#if not os.path.exists(model_path):
#    raise TFModelException()
#
## Create the estimator
#k_means = tf.contrib.factorization.KMeansClustering(
#            num_clusters=NUM_CLUSTERS, use_mini_batch=False,
#            model_dir=model_path
#)
#
## All beer learning with a beer description and at least one feature with a 1
#beer_desc_learnings, col_names = BeerLearning.objects.beer_descriptions()
#
#col_names = col_names[1:]
#ids = []
#tf_points = []
#for r in beer_desc_learnings:
#    ids.append(r[0])
#    tf_points.append(r[1:])
#
#tf_points = np.array(tf_points, dtype=np.float32)
#
## Get cluster indices for all descriptions
#cluster_indices = list(k_means.predict_cluster_index(lambda: tf.train.limit_epochs(
#        tf.convert_to_tensor(tf_points), num_epochs=1
#    )))



