from .mot_reid_wrapper import MOTreIDWrapper
from .mot_wrapper import MOT17Wrapper

_sets = {}

# Fill all available datasets, change here to modify / add new datasets.


# AQUI HE QUITADO TEST

# for split in ['train']:
#     #for dets in ['train']:
#         #name = f'mot17_{split}_{dets}'
#         #_sets[name] = (lambda *args, split=split,dets=dets: MOT17Wrapper(split, dets, *args))
#
#     name = f'mot17_{split}'
#     #_sets[name] = (lambda *args, split=split: MOT17Wrapper(split,*args))
#     _sets[name] = (lambda *args, split=split: MOT17Wrapper(split, *args))

for split in ['train', 'test']:
    #for dets in ['']:
    name = f'mot17_{split}'
    _sets[name] = (lambda *args, split=split: MOT17Wrapper(split, *args))

for split in ['train', 'small_val', 'small_train']:
    name = f'mot_reid_{split}'
    _sets[name] = (lambda *args, split=split: MOTreIDWrapper(split, *args))

class Datasets(object):
    """A central class to manage the individual dataset loaders.

    This class contains the datasets. Once initialized the individual parts (e.g. sequences)
    can be accessed.
    """

    def __init__(self, dataset, *args):
        """Initialize the corresponding dataloader.

        Keyword arguments:
        dataset --  the name of the dataset
        args -- arguments used to call the dataloader
        """

        '''
        dets = ''
        _sets['mot17_train'] = (lambda *args, split="train",dets=dets: MOT17Wrapper(split, dets, *args))
        #_sets['mot17_train'] = MOT17Wrapper("train",'', *args)
        
        '''
        assert dataset in _sets, "[!] Dataset not found: {}".format(dataset)

        if len(args) == 0:
            args = [{}]

        self._data = _sets[dataset](*args)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        return self._data[idx]
