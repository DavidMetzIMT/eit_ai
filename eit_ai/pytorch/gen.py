
from logging import getLogger


from eit_ai.train_utils.gen import Generators


logger = getLogger(__name__)

################################################################################
# Keras Models
################################################################################

class GeneratorPyTorch(Generators):
    """ Generator class for keras models """

if __name__ == "__main__":
    from eit_ai.utils.log import change_level, main_log
    import logging
    main_log()
    change_level(logging.DEBUG)
    

    