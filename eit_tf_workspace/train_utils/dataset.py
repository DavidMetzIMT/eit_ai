
from abc import ABC, abstractmethod
from enum import Enum
from logging import getLogger

import numpy as np
import sklearn.model_selection
from eit_tf_workspace.train_utils.metadata import MetaData
from eit_tf_workspace.raw_data.raw_samples import RawSamples
from sklearn.preprocessing import MinMaxScaler

logger = getLogger(__name__)

################################################################################
# Abstract Class for Dataset
################################################################################

class Datasets(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.train=None
        self.val=None
        self.test=None
        self._nb_samples:int= 0
        self._batch_size:int=32
        self._test_ratio:float=0.20
        self._val_ratio:float=0.2
        self._train_len:int= 0
        self._val_len:int= 0
        self._test_len:int= 0
        self._idx_train:list=[]
        self._idx_val:list=[]
        self._idx_test:list= []
        self.fwd_model:dict={}
        self.src_file:str= ''
        self.input_size:int= 0
        self.ouput_size:int= 0

    def build(self,raw_samples:RawSamples, metadata:MetaData):
        X=raw_samples.X
        Y=raw_samples.Y
        self.fwd_model= raw_samples.fwd_model
        self._set_sizes_dataset(X, Y, metadata)
        


        X, Y= self._preprocess(X, Y, metadata)
        if self._is_indexes(metadata):
            self._mk_dataset_from_indexes(X, Y, metadata)
        else:
            self._mk_dataset(X, Y, metadata)
        self._compute_sizes()
        metadata._nb_samples= self._nb_samples
        metadata._train_len=self._train_len
        metadata._val_len=self._val_len
        metadata._test_len=self._test_len
        metadata.input_size=self.input_size
        metadata.output_size=self.ouput_size

    def _set_sizes_dataset(self,X, Y, metadata:MetaData):
        self._nb_samples= np.shape(X)[0]
        self._batch_size = metadata.batch_size
        self._test_ratio= metadata.test_ratio
        self._val_ratio = metadata.val_ratio
        self.input_size= np.shape(X)[1]
        self.ouput_size= np.shape(Y)[1]

    def _compute_sizes(self):
        self._train_len=self.get_X('train').shape[0]
        self._val_len=self.get_X('val').shape[0]
        self._test_len= self.get_X('test').shape[0]
        logger.info(f'Length of train: {self._train_len}')
        logger.info(f'Length of val: {self._val_len}' )
        logger.info(f'Length of test: {self._test_len}')

    def _is_indexes(self, metadata:MetaData):
        return metadata.idx_samples['idx_train']

    @abstractmethod
    def get_X(self, part:str='train'):
        """return X from a dataset part (train, val, test)"""

    @abstractmethod
    def get_Y(self, part:str='train'):
        """return Y from a dataset part (train, val, test)"""

    @abstractmethod
    def get_samples(self, part: str):
        """Return all samples_x, and samples_y as a tuple"""

    @abstractmethod
    def _preprocess(self, X, Y, metadata:MetaData):
        """return X, Y preprocessed"""

    @abstractmethod
    def _mk_dataset(self, X, Y, metadata:MetaData)-> None:
        """build the dataset"""

    @abstractmethod
    def _mk_dataset_from_indexes(self, X, Y, metadata:MetaData)-> None:
        """rebuild the dataset with the indexes """


################################################################################
# XY Set Class for Custom standard dataset
################################################################################

class XYSet(object):
    x=np.array([])
    y = np.array([])
    def __init__(self,x=np.array([]), y=np.array([])) -> None:
        super().__init__()
        self.set_data(x, y)
 
    def set_data(self, x, y):
        self.x=x
        self.y=y

    def get_set(self):
        return self.x, self.y
    
################################################################################
# Custom standard dataset
################################################################################

class StdDataset(Datasets):
   
    def get_X(self, part:str='train'):
        return getattr(self, part).get_set()[0]

    def get_Y(self, part:str='train'):
        return getattr(self, part).get_set()[1]

    def get_samples(self, part: str):
        return getattr(self, part).get_set()

    def _preprocess(self, X, Y, metadata:MetaData):
        """return X, Y preprocessed"""
        X=scale_prepocess(X, metadata.normalize[0])
        Y=scale_prepocess(Y, metadata.normalize[0])
        return X, Y

    def _mk_dataset(self, X, Y, metadata:MetaData)-> None:
        """build the dataset"""
        idx=np.reshape(range(X.shape[0]),(X.shape[0],1))
        X= np.concatenate(( X, idx ), axis=1)
        x_tmp, x_test, y_tmp, y_test = sklearn.model_selection.train_test_split(X, Y,test_size=self._test_ratio)
        x_train, x_val, y_train, y_val = sklearn.model_selection.train_test_split(x_tmp, y_tmp, test_size=self._val_ratio)
        
        self._idx_train= x_train[:,-1].tolist()
        self._idx_val= x_val[:,-1].tolist()
        self._idx_test= x_test[:,-1].tolist()
        metadata.set_idx_samples(self._idx_train, self._idx_val, self._idx_test)

        self.train=XYSet(x=x_train[:,:-1], y=y_train)
        self.val=XYSet(x=x_val[:,:-1], y=y_val)
        self.test=XYSet(x=x_test[:,:-1], y=y_test)

    def _mk_dataset_from_indexes(self, X, Y, metadata:MetaData)-> None:
        """rebuild the dataset with the indexes """
        self._idx_train= convert_vec_to_int(metadata.idx_samples['idx_train'])
        self._idx_val= convert_vec_to_int(metadata.idx_samples['idx_val'])
        self._idx_test= convert_vec_to_int(metadata.idx_samples['idx_test'])   
        self.train=XYSet(x=X[self._idx_train,:], y=Y[self._idx_train,:])
        self.val=XYSet(x=X[self._idx_val,:], y=Y[self._idx_val,:])
        self.test=XYSet(x=X[self._idx_test,:], y=Y[self._idx_test,:])

################################################################################
# Methods
################################################################################

def scale_prepocess(x, scale:bool=True):
    if scale:
        scaler = MinMaxScaler()
        x= scaler.fit_transform(x)
    return x

def convert_to_int(x):
    return np.int(x)
convert_vec_to_int = np.vectorize(convert_to_int)


if __name__ == "__main__":
    from eit_tf_workspace.utils.log import change_level, main_log
    import logging
    main_log()
    change_level(logging.DEBUG)
