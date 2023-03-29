from pathlib import Path
import os
from ..utils import set_logging

CFG_FLOAT_KEYS = {
    'warmup_epochs', 'degrees', 'shear'
}
CFG_FRACTION_KEYS = {
    'dropout', 'lr0', 'lrf', 'momentum', 'weight_decay', 'warmup_momentum', 'warmup_bias_lr', 'fl_gamma',
    'hsv_h', 'hsv_s', 'hsv_v', 'translate', 'scale', 'perspective', 'flipud', 'fliplr', 
    'mixup', 'copy_paste', 'conf',
}
CFG_INT_KEYS = {
    'epochs', 'patience', 'batchsz', 'workers', 'seed', 'workspace', 'save_period',
}
CFG_BOOL_KEYS = {
    'save', 'verbose', 'save_json', 'fp16', 'plots', 'keras', 'optimize', 'int8', 'dynamic', 'simplify', 
}

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # training
LOGGING_NAME = "chatbot"
LOGGER = set_logging(LOGGING_NAME)
RANK = int(os.getenv('RANK', -1))
