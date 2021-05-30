import pandas as pd
from torch.utils import data


class Dataset(data.Dataset):
    """Face Landmarks dataset."""

    def __init__(self, csv_file):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.landmarks_frame = pd.read_excel(csv_file)

    def __len__(self):
        # print len(self.landmarks_frame)
        return len(self.landmarks_frame)
        # return 1800000

    def __getitem__(self, idx):
        landmarks = self.landmarks_frame.get_chunk(128).as_matrix().astype('float')
        return landmarks


