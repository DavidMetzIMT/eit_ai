import numpy as np
from sklearn.metrics import mean_squared_error
import tensorflow.keras.backend as K


def EIT_mse(y_true, y_pred):
    return 

def EIT_rie(y_true, y_pred):
    return K.sqrt(K.sum(K.pow(K.abs(y_true-y_pred),2))/K.sum(K.pow(K.abs(y_pred),2)))

def EIT_re(y_true, y_pred):
    """Relative error

    Args:
        y_true ([type]): [description]
        y_pred ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    return K.sqrt(K.sum(K.square(y_true-y_pred))/K.sum(K.square(y_pred)))
    

def EIT_icc(y_true, y_pred):
    
    icc_matrix = np.corrcoef(y_true, y_pred,rowvar=False) #(Image) Correlation Coefficient (ICC)

    nb_samples=y_true.shape[1]
    I=np.eye(nb_samples)
    return np.diag(icc_matrix[:nb_samples,nb_samples:]*I)



def normalized(y_true, y_pred):

    #!!!I don't know why, but only in that form it normalized correctly, and if I don't put values in [], drops an error: Found input variables with inconsistent numbers of samples: [3054, 1]
    #y_true = tf.keras.utils.normalize(y_true, axis=1) #if I normalize like this, then it is normalized too much (like to 0.02.., not 1), maybe because of [3054, 1]
    y_true = [(y_true-min(y_true))/(max(y_true)-min(y_true))] #normalize 

    print('Real normalized values: ' + str(y_true) + '; Solved normalized values: ' + str(y_pred))

def error_eval(y_true, y_pred, verbose=False, axis_samples=0, info='set from error_eval'):

    if y_true.shape==y_pred.shape:
        
        if y_true.ndim==1:
            y_true= np.reshape(y_true, (y_true.shape[0],1))
            y_pred= np.reshape(y_pred, (y_pred.shape[0],1))
        else:
            if axis_samples==0:
                y_true= y_true.T
                y_pred= y_pred.T

        if verbose:
            print('shape of y_true, y_pred:', y_true.shape, y_pred.shape)        

        mse = mean_squared_error(y_true, y_pred, multioutput='raw_values').T #Mean Squared Error (MSE)
        rie = np.linalg.norm(y_true-y_pred,axis=0)/np.linalg.norm(y_true,axis=0) #Relative (Image) Error (RIE)
        icc_matrix = np.corrcoef(y_true, y_pred,rowvar=False) #(Image) Correlation Coefficient (ICC)
        

        nb_samples=y_true.shape[1]
        I=np.eye(nb_samples)
        icc= np.diag(icc_matrix[:nb_samples,nb_samples:]*I)

        # for idx in range(y_true.shape[1]):
        #     icc.append(icc_matrix[idx,idx+y_true.shape[1]])

        if verbose:

            print('ICC_matrix = ', icc_matrix, icc_matrix.shape)
            print('MSE = ',mse, mse.shape)
            print('RIE = ' , rie, rie.shape)
            print('ICC = ', icc, icc.shape)

    results= EvalResults()
    results.set_values(mse, rie, icc, info)
    return results

class EvalResults(object):
    def __init__(self) -> None:
        super().__init__()
        self.indicators=dict()
        self.info=None

    def set_values(self, mse, rie, icc, info='values set')-> None:
        self.indicators['mse']=mse
        self.indicators['rie']=rie
        self.indicators['icc']=icc
        self.info = info



if __name__ == "__main__":
    a= np.array([[1 ,2 ,3 ,5, 5, 3], [1 ,2 ,3 ,4, 4, 4],[1 ,2 ,3 ,6, 6, 3]])
    b= np.array([[1 ,2 ,3 ,3, 3, 3], [1 ,2 ,3 ,3, 4, 3],[1 ,2 ,3 ,3, 6, 3]])
    print(a.shape, b.shape)

    error_eval(a,b,True, axis_samples=0)


    a= np.array([1 ,2 ,3 ,5, 5, 3])
    b= np.array([1 ,2 ,3 ,3, 3, 3])
    print(a.shape, b.shape)

    error_eval(a,b,True, axis_samples=1)

    a= np.array([1 ,2 ,3 ,4, 4, 4])
    b= np.array([1 ,2 ,3 ,3, 4, 3])
    print(a.shape, b.shape)

    error_eval(a,b,True)

    a= np.array([1 ,2 ,3 ,6, 6, 3])
    b= np.array([1 ,2 ,3 ,3, 6, 3])
    print(a.shape, b.shape)

    error_eval(a,b,True)








    