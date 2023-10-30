import numpy as np
import torch
import random


class AttrPredictor(object):

    def __init__(self, cfg = None, tops_type=[3, 5, 10]):
        """Create the empty array to count true positive(tp),
            true negative(tn), false positive(fp) and false negative(fn).

        Args:
            class_num : number of classes in the dataset
            tops_type : default calculate top3, top5 and top10
        """
        attr_cloth_file = open(cfg.attr_cloth_file).readlines()
        self.attr_idx2name = {}
        for i, line in enumerate(attr_cloth_file[2:]):
            self.attr_idx2name[i] = line.strip('\n').split()[0]
        self.tops_type = tops_type

    def get_attr_name(self, pred_idx):
        return [self.attr_idx2name[idx] for idx in pred_idx]
    
    def get_random(self):
        result = {}
        for topk in self.tops_type:
            idxes = []
            for _ in range(topk):
                random_index = random.randint(0, len(self.attr_idx2name) - 1)
                idxes.append(random_index)

            top_result = {
                f"top {topk}": self.get_attr_name(idxes),
            }
            result.update(top_result)
        return result

    def show_prediction(self, pred):
        if isinstance(pred, torch.Tensor):
            data = pred.data.cpu().numpy()
        elif isinstance(pred, np.ndarray):
            data = pred
        else:
            raise TypeError('type {} cannot be calculated.'.format(type(pred)))

        result = {}
        for i in range(pred.size(0)):
            indexes = np.argsort(data[i])[::-1]
            for topk in self.tops_type:
                idxes = indexes[:topk]
                top_result = {
                    f"top {topk}": self.get_attr_name(idxes),
                }
                result.update(top_result)
        return result
