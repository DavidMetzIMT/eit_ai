
from dataclasses import dataclass
from logging import error, getLogger
import sys
from typing import List

import eit_tf_workspace.constants as const
from eit_tf_workspace.train_utils.lists import ListDatasets, ListGenerators, ListLosses, ListModels, ListOptimizers
from eit_tf_workspace.utils.path_utils import *
from eit_tf_workspace.utils.log import log_msg_highlight
from scipy.io.matlab.mio import savemat

logger = getLogger(__name__)

################################################################################
# Class MetaData
################################################################################
@dataclass
class MetaData(object):
    """ Metadata Class regroup the data and information of the training
    for the training and eval"""
    time:str=None
    training_name:str=None
    ouput_dir:str=None

    raw_src_file:list[str]=None
    # dataset_src_file_pkl:List[str]=None
    idx_samples_file:list[str]=None
    model_saving_path:list[str]=None
    save_summary:bool=None

    data_select:list[str]=None
    _nb_samples:int=None
    batch_size:int=None
    test_ratio:float=None
    val_ratio:float=None
    # use_tf_dataset:bool=None
    normalize:list[bool]=None
    idx_samples:dict= None
    epoch:int=None
    max_trials_autokeras:int=None
    _train_len:int=None
    _val_len:int=None
    _test_len:int=None
    input_size:int=None
    output_size:int=None
    _steps_per_epoch:int =None
    _validation_steps:int =None
    _test_steps:int=None
    callbacks=None
    optimizer:str=None
    learning_rate:float= None
    loss:str= None
    metrics:list[str]= None

    training_duration:str=None
    gen_type:ListGenerators=None
    model_type:ListModels=None
    dataset_type:ListDatasets=None

    def __post_init__(self):
        self.set_idx_samples(save=False)
    
    def set_ouput_dir(self, training_name:str='', append_date_time:bool= True) -> None:
        """Create the ouput directory for training results

        Args:
            training_name (str, optional): if empty training_name='training_default_name'. Defaults to ''.
            append_date_time (bool, optional): Defaults to True.
        """

        self.time = get_date_time()
        if not training_name:
            training_name='training_default_name'
        self.training_name= f'{training_name}_{self.time}' if append_date_time else training_name
        self.ouput_dir= mk_ouput_dir(
            self.training_name,
            default_out_dir=const.DEFAULT_OUTPUTS_DIR)
        msg=f'Training results will be found in : {self.ouput_dir}'
        logger.info(log_msg_highlight(msg))

    def set_model_dataset_type(self, gen_type:ListGenerators, model_type:ListModels, dataset_type:ListDatasets):
        """"""
        self.gen_type= gen_type.value
        self.model_type= model_type.value
        self.dataset_type= dataset_type.value

    def set_4_dataset(  
            self, 
            batch_size:int=32, test_ratio:float=0.2, val_ratio:float=0.2, 
            # use_tf_dataset:bool=False, 
            normalize= [True, True]):
        """ """             
        self.batch_size = batch_size
        self.val_ratio, self.test_ratio =check_ratios(val_ratio, test_ratio)
        self.normalize=normalize 

    def set_4_model(   
            self,
            epoch:int=10,
            max_trials_autokeras=10, 
            callbacks=[],
            optimizer:ListOptimizers=None,
            learning_rate:float=None,
            loss:ListLosses=None,
            metrics=['mse'],
            save_summary:bool=False)-> None:
        """ """
        if not self.batch_size:
            error('call first set_4_dataset')

        self.epoch= epoch
        self.max_trials_autokeras=max_trials_autokeras
        self.callbacks=callbacks      
        self.optimizer=optimizer.value if optimizer else None
        self.learning_rate= learning_rate
        self.loss=loss.value if loss else None
        self.metrics=metrics
        self.save_summary=save_summary

        self._steps_per_epoch=compute_steps(self.batch_size, self._train_len)
        self._validation_steps=compute_steps(self.batch_size, self._val_len)
        self._test_steps=compute_steps(self.batch_size, self._test_len)

    def set_raw_src_file(self, src_file):
        self.raw_src_file=make_PoSIX_abs_rel(src_file, self.ouput_dir)
    def set_model_saving_path(self, model_saving_path):
        self.model_saving_path=make_PoSIX_abs_rel(model_saving_path, self.ouput_dir)

    def set_idx_samples(self, idx_train:list=[], idx_val:list=[], idx_test:list=[], save:bool=True):
        self.idx_samples={
            'idx_train': idx_train,
            'idx_val': idx_val,
            'idx_test': idx_test
        }
        if save:
            self.save_idx_samples_2matfile()

    def get_idx_samples(self):
        return [
            self.idx_samples['idx_train'],
            self.idx_samples['idx_val'],
            self.idx_samples['idx_test'],
        ] 

    def set_idx_samples_file(self, path):
        self.idx_samples_file=make_PoSIX_abs_rel(path, self.ouput_dir)

    def save_idx_samples_2matfile(self):
        """ save the indexes of the samples used to build 
        the dataset train, val and test """

        indexes = self.idx_samples
        time = self.time or get_date_time()
        path =  os.path.join(self.ouput_dir, f'{time}_{const.EXT_IDX_FILE}')
        savemat(path, indexes)
        save_as_pickle(path, indexes)
        save_as_txt(path,indexes)
        self.set_idx_samples_file(path)

    def set_training_duration(self, duration:str=''):
        self.training_duration= duration

    def set_4_raw_samples(self, data_sel):
        self.data_select=data_sel

    def save(self, dir_path= None):

        if not self.ouput_dir:
            return
        dir_path = dir_path or self.ouput_dir
        filename=os.path.join(dir_path,const.METADATA_FILENAME)
        copy=MetaData()
        for key, val in self.__dict__.items():
            if hasattr(val, '__dict__'):
                setattr(copy, key, type(val).__name__)
            elif isinstance(val, list):
                l = []
                for elem in val:
                    if hasattr(elem, '__dict__'):
                        l.append(type(elem).__name__)
                    else:
                        l.append(elem)
                setattr(copy, key, l)
            else:
                setattr(copy, key, val)
        save_as_txt(filename, copy)
        logger.info(log_msg_highlight(f'Metadata saved in: {filename}'))
        
        
    def read(self, path):
        
        load_dict=read_txt(path)
        for key in load_dict.keys():
            if key in self.__dict__.keys():
                setattr(self,key, load_dict[key])

        logger.info(log_msg_highlight(f'Metadata loaded from: {path}, '))
        logger.info(f'Metadata loaded :\n{self.__dict__.keys()}')
        logger.debug(f'Metadata loaded (details):\n{self.__dict__}')

    def reload(self, dir_path:str=''):

        if not os.path.isdir(dir_path):
            title= 'Select directory of model to evaluate'
            try: 
                dir_path=get_dir(title=title)
            except DialogCancelledException as e:
                logger.critical('User cancelled the loading')
                sys.exit()
            
        self.read(os.path.join(dir_path,const.METADATA_FILENAME))

################################################################################
# Methods
################################################################################

def compute_steps(batch_size:int, len_dataset:int)->int :
    return len_dataset // batch_size if batch_size or len_dataset==0 else None

def check_ratios(val_ratio:float, test_ratio:float)-> tuple[float, float]:
    """Check the ratios of val and test dataset"""
    if val_ratio <=0.0:
        val_ratio=0.2
        logger.warning(f'val ratio <=0.0: set to {val_ratio}')

    if test_ratio <=0.0:
        test_ratio=0.2
        logger.warning(f'test ratio <=0.0: set to {test_ratio}')

    if test_ratio+val_ratio>=0.5:
        test_ratio=0.2
        val_ratio=0.2
        logger.warning(f'val and test ratios:{val_ratio} and {test_ratio}')
    return val_ratio, test_ratio

def make_PoSIX_abs_rel(path:str, rel_path:str)-> list[str]:
    rel=os.path.relpath(path, start=rel_path)
    return [ get_POSIX_path(path), get_POSIX_path(rel)]



if __name__ == "__main__":
    from eit_tf_workspace.utils.log import change_level, main_log
    import logging
    main_log()
    change_level(logging.DEBUG)
    a= MetaData()
    a.reload()
    

