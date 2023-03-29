from ..constants import ROOT, LOGGER

def check_cls_dataset(dataset: str):
    data_dir = (ROOT / 'data' / dataset).resolve()
    if not data_dir.is_dir():
        LOGGER.info(f'\nDataset not found ⚠️, missing path {data_dir}')
    train_set = data_dir / "train"
    test_set = data_dir / 'test' if (data_dir / 'test').exists() else data_dir / 'val'  # data/test or data/val
    nc = len([x for x in (data_dir / 'train').glob('*') if x.is_dir()])  # number of classes
    names = [x.name for x in (data_dir / 'train').iterdir() if x.is_dir()]  # class names list
    names = dict(enumerate(sorted(names)))
    return {"train": train_set, "val": test_set, "nc": nc, "names": names}
