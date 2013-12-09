import random
import unittest

import numpy as np
from scipy.sparse import coo_matrix

from rlscore.learner import CGRankRLS
from rlscore import data_sources
from rlscore.kernel import LinearKernel



class Test(unittest.TestCase):
    
    def setUp(self):
        np.random.seed(100)
        random.seed(100)
    
    
    def testOrdinalRegression(self):
        m, n = 100, 300
        for regparam in [0.00000001, 1, 100000000]:
        #for regparam in [1000]:
            Xtrain = np.mat(np.random.rand(n, m))
            Y = np.mat(np.random.rand(m, 1))
            rpool = {}
            rpool[data_sources.TRAIN_FEATURES] = Xtrain.T
            rpool[data_sources.TRAIN_LABELS] = Y
            rpool[data_sources.TIKHONOV_REGULARIZATION_PARAMETER] = regparam
            rpool["bias"] = 1.0
            k = LinearKernel.createKernel(**rpool)
            rpool[data_sources.KERNEL_OBJ] = k
            rls = CGRankRLS.createLearner(**rpool)
            rls.train()
            model = rls.getModel()   
            W = model.W
            In = np.mat(np.identity(n))
            Im = np.mat(np.identity(m))
            L = np.mat(Im-(1./m)*np.ones((m,m), dtype=np.float64))
            G = Xtrain*L*Xtrain.T+regparam*In
            W2 = np.linalg.inv(G)*Xtrain*L*Y
            for i in range(W.shape[0]):
                for j in range(W.shape[1]):
                    self.assertAlmostEqual(W[i,j],W2[i,j], places=5)
    
    
    def testPairwisePreferences(self):
        m, n = 100, 300
        for regparam in [0.00000001, 1, 100000000]:
            Xtrain = np.mat(np.random.rand(n, m))
            Y = np.mat(np.random.rand(m, 1))
            
            pairs = []
            for i in range(1000):
                a = random.randint(0, m - 1)
                b = random.randint(0, m - 1)
                if Y[a] > Y[b]:
                    pairs.append((a, b))
                else:
                    pairs.append((b, a))
            pairs = np.array(pairs)
            rpool = {}
            rpool[data_sources.TRAIN_FEATURES] = Xtrain.T
            #rpool[data_sources.TRAIN_LABELS] = Y
            rpool['train_preferences'] = pairs
            rpool[data_sources.TIKHONOV_REGULARIZATION_PARAMETER] = regparam
            rpool["bias"] = 1.0
            k = LinearKernel.createKernel(**rpool)
            rpool[data_sources.KERNEL_OBJ] = k
            rls = CGRankRLS.createLearner(**rpool)
            rls.train()
            model = rls.getModel()   
            W = model.W
            In = np.mat(np.identity(n))
            Im = np.mat(np.identity(m))
            vals = np.concatenate([np.ones((pairs.shape[0]), dtype=np.float64), -np.ones((pairs.shape[0]), dtype=np.float64)])
            row = np.concatenate([np.arange(pairs.shape[0]),np.arange(pairs.shape[0])])
            col = np.concatenate([pairs[:,0], pairs[:,1]])
            coo = coo_matrix((vals, (row, col)), shape=(pairs.shape[0], Xtrain.T.shape[0]))
            L = (coo.T*coo).todense()
            G = Xtrain*L*Xtrain.T+regparam*In
            W2 = np.linalg.inv(G)*Xtrain*coo.T*np.mat(np.ones((pairs.shape[0],1)))
            for i in range(W.shape[0]):
                for j in range(W.shape[1]):
                    self.assertAlmostEqual(W[i,j],W2[i,j], places=4)
                    
    def testQueryData(self):
        """ToBeImplemented"""
        pass