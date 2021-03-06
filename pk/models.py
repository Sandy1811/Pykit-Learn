""" This module contains the model objects for the GUI.
    Author: Sean Dai
"""
from sklearn.base import BaseEstimator
from sklearn.base import clone

class BaseModel(object):
    """
    A base model class to hold information.
    """
    def __init__(self):
        self.observers = []
        self.data = None

    def add_observer(self, observer):
        """
        Register an observer.
        """
        self.observers.append(observer)

    def changed(self, event):
        """
        Notify observers of changes.
        """
        for obs in self.observers:
            obs.update(event, self)

class Algorithm(BaseModel):
    """
    This class wraps the machine learning algorithm around an object.
    """
    def __init__(self, clf=BaseEstimator()):
        super(Algorithm, self).__init__()
        self.clf = clf
        # Create a deep copy of origin classifier for retraining purposes.
        self.clf_name = type(clf).__name__
        self.fitted = False

    def __repr__(self):
        return str(vars(self))

    @property
    def params(self):
        """
        Gets the classifier parameters
        """
        return self.clf.__dict__

    def _fit(self, *args, **kwargs):
        """
        Runs the algorithm with the passed-in parameters.
        """
        self.fitted = True
        return self.clf.fit(*args, **kwargs)

    def predict(self, X):
        if not self.fitted:
            raise Exception("Can't predict with untrained classifier!")
        return self.clf.predict(X)

class SupervisedAlgorithm(Algorithm):
    """
    Wrapper class for supervised learning algorithms.
    """
    def __init__(self, clf):
        super(SupervisedAlgorithm, self).__init__(clf)

    def fit(self, X, y):
        self.clf = self._fit(X, y)

class UnsupervisedAlgorithm(Algorithm):
    """
    Class for unsupervised algorithms (eg. clustering, PCA, etc.)
    """
    def __init__(self, clf):
        super(UnsupervisedAlgorithm, self).__init__(clf)

    def fit(self, X):
        self.clf = self._fit(X)


# from sklearn.tree import DecisionTreeClassifier
# from sklearn.mixture import GMM
# from pk.utils.loading import load_csv
# X,y,_ = load_csv('tests/iris2.csv')
# clf = GMM(n_components=3)
# a = UnsupervisedAlgorithm(clf)
# print a.params
# print a.fitted
# import time
# s = time.time()
# a.fit(X)
# print "Took %f secs" % (time.time() - s)
# print a.fitted
# print a.params
# print a
# print a.clf.means_
# print a.predict([[1,2,3,4]])
