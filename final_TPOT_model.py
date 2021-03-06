import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.feature_selection import SelectFwe, f_regression
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.7685271642175507
exported_pipeline = make_pipeline(
    make_union(
        StackingEstimator(estimator=make_pipeline(
            StackingEstimator(estimator=GradientBoostingRegressor(alpha=0.99, learning_rate=0.1, loss="huber", max_depth=10, max_features=0.7000000000000001, min_samples_leaf=17, min_samples_split=19, n_estimators=100, subsample=0.9000000000000001)),
            SelectFwe(score_func=f_regression, alpha=0.043000000000000003),
            RandomForestRegressor(bootstrap=False, max_features=0.15000000000000002, min_samples_leaf=1, min_samples_split=3, n_estimators=100)
        )),
        FunctionTransformer(copy)
    ),
    ElasticNetCV(l1_ratio=0.9500000000000001, tol=0.1)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
