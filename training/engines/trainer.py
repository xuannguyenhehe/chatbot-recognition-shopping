from ..configs import get_cfg
from ..utils.torch_utils import select_device, init_seeds
from ..data.utils import check_cls_dataset
from ..constants import LOGGER, RANK
from pathlib import Path
from torch.cuda import amp
from collections import defaultdict
import torch

class Trainer:
    def __init__(self, cfg_name: str, override_config: bool=None):
        self.args = get_cfg(cfg_name)
        self.device = select_device(self.args.device, self.args.batch)
        self.console = LOGGER
        self.validator = None
        self.model = None
        self.metrics = None
        init_seeds(self.args.seed + 1 + RANK)

        project = self.args.project
        name = self.args.name
        self.save_dir = Path(self.args.save_dir)
        self.work_dir = self.save_dir / 'weights'
        if RANK in {-1, 0}:
            self.work_dir.mkdir(parents=True, exist_ok=True)  # make dir
            self.args.save_dir = str(self.save_dir)
        self.last, self.best = self.wdir / 'last.pt', self.wdir / 'best.pt'  # checkpoint paths
        self.save_period = self.args.save_period

        self.batch_size = self.args.batch
        self.epochs = self.args.epochs
        self.start_epoch = 0

        # Device
        self.amp = self.device.type != 'cpu'
        self.scaler = amp.GradScaler(enabled=self.amp)

        # Model and Dataloaders.
        self.model = self.args.model
        self.data = check_cls_dataset(self.args.data)
        self.trainset, self.testset = self.get_dataset(self.data)
        self.ema = None

        # Optimization utils init
        self.lf = None
        self.scheduler = None

        # Epoch level metrics
        self.best_fitness = None
        self.fitness = None
        self.loss = None
        self.tloss = None
        self.loss_names = ['Loss']
        self.csv = self.save_dir / 'results.csv'
        self.plot_idx = [0, 1, 2]

        # Callbacks
        self.callbacks = defaultdict(list)

    def get_dataset(self, data):
        """
        Get train, val path from data dict if it exists. Returns None if data format is not recognized.
        """
        return data["train"], data.get("val") or data.get("test")
    
    def add_callback(self, event: str, callback):
        """
        Appends the given callback.
        """
        self.callbacks[event].append(callback)

    def set_callback(self, event: str, callback):
        """
        Overrides the existing callbacks with the given callback.
        """
        self.callbacks[event] = [callback]

    def run_callbacks(self, event: str):
        for callback in self.callbacks.get(event, []):
            callback(self)

    def train(self):
        # Allow device='', device=None on Multi-GPU systems to default to device=0
        if isinstance(self.args.device, int) or self.args.device:  # i.e. device=0 or device=[0,1,2,3]
            world_size = torch.cuda.device_count()
        elif torch.cuda.is_available():  # i.e. device=None or device=''
            world_size = 1  # default to device 0
        else:  # i.e. device='cpu' or 'mps'
            world_size = 0

        # Run subprocess if DDP training, else train normally
