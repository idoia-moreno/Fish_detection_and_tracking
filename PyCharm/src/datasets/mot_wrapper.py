import torch
from torch.utils.data import Dataset

from .mot_sequence import MOT17Sequence


class MOT17Wrapper(Dataset):
	"""A Wrapper for the MOT_Sequence class to return multiple sequences."""

	#def __init__(self, split, dets, dataloader):
	def __init__(self, split, dataloader):
		"""Initliazes all subset of the dataset.

		Keyword arguments:
		split -- the split of the dataset to use
		dataloader -- args for the MOT_Sequence dataloader
		"""

		train_sequences = ['MOT17-02']

		test_sequences = ['MOT17-01']

		if "train" == split:
			sequences = train_sequences
		elif "test" == split:
			sequences = test_sequences
		else:
			raise NotImplementedError("MOT split not available.")

		self._data = []
		for s in sequences:
			self._data.append(MOT17Sequence(seq_name=s))  ##QUITAMOS DATALOADER
		print(dataloader)
		#self._data.append(MOT17Sequence(seq_name=sequences, dets=dets, **dataloader))


	def __len__(self):
		return len(self._data)

	def __getitem__(self, idx):
		return self._data[idx]


