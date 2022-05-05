import os

from enum import Enum
from dataclasses import dataclass

import numpy as np
import cv2
import pandas as pd

class XRayLabel(Enum):

    Normal  = 'Normal'
    Lung_Opacity = 'Lung_Opacity'
    COVID = 'COVID'
    Viral_Pneumonia = 'Viral Pneumonia'

@dataclass
class XRayStudy:

    scan: np.ndarray = None
    mask: np.ndarray = None
    label: XRayLabel = None

class DatasetReader:

    def __init__(self, dataset_directory):
        self.dataset_directory = dataset_directory

    def load_file(self, name, mask=False):
        subdir = 'scans' if not mask else 'masks'
        filename = os.path.join(self.dataset_directory, subdir, name)
        return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)[...,None]

    def load_study(self, name):
        scan = self.load_file(name, False)
        mask = self.load_file(name, True)
        return scan, mask

    def load_cases(self, metadata: pd.DataFrame):
        for row in metadata.iterrows():
            index, series = row
            scan, mask = self.load_study(series['id'])
            yield XRayStudy(scan, mask, XRayLabel(series['label']))