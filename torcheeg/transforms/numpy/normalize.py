from typing import Union, Dict

import numpy as np

from ..base_transform import EEGTransform


class MeanStdNormalize(EEGTransform):
    r'''
    Perform z-score normalization on the input data. This class allows the user to define the dimension of normalization and the used statistic.

    .. code-block:: python

        transform = MeanStdNormalize(axis=0)
        # normalize along the first dimension (electrode dimension)
        transform(eeg=torch.randn(32, 128))['eeg'].shape
        >>> (32, 128)

        transform = MeanStdNormalize(axis=1)
        # normalize along the second dimension (temproal dimension)
        transform(eeg=torch.randn(32, 128))['eeg'].shape
        >>> (32, 128)

    Args:
        mean (np.array, optional): The mean used in the normalization process, allowing the user to provide mean statistics in :obj:`np.ndarray` format. When statistics are not provided, use the statistics of the current sample for normalization.
        std (np.array, optional): The standard deviation used in the normalization process, allowing the user to provide tandard deviation statistics in :obj:`np.ndarray` format. When statistics are not provided, use the statistics of the current sample for normalization.
        axis (int, optional): The dimension to normalize, when no dimension is specified, the entire data is normalized.
        apply_to_baseline: (bool): Whether to act on the baseline signal at the same time, if the baseline is passed in when calling. (defualt: :obj:`False`)
    
    .. automethod:: __call__
    '''
    def __init__(self,
                 mean: Union[np.ndarray, None] = None,
                 std: Union[np.ndarray, None] = None,
                 axis: Union[int, None] = None,
                 apply_to_baseline: bool = False):
        super(MeanStdNormalize,
              self).__init__(apply_to_baseline=apply_to_baseline)
        self.mean = mean
        self.std = std
        self.axis = axis

    def __call__(self,
                 *args,
                 eeg: np.ndarray,
                 baseline: Union[np.ndarray, None] = None,
                 **kwargs) -> Dict[str, np.ndarray]:
        r'''
        Args:
            eeg (np.ndarray): The input EEG signals or features.
            baseline (torch.Tensor, optional) : The corresponding baseline signal, if apply_to_baseline is set to True and baseline is passed, the baseline signal will be transformed with the same way as the experimental signal.

        Returns:
            np.ndarray: The normalized results.
        '''
        return super().__call__(*args, eeg=eeg, baseline=baseline, **kwargs)

    def apply(self, eeg: np.ndarray, **kwargs):
        if (self.mean is None) or (self.std is None):
            if self.axis is None:
                mean = eeg.mean()
                std = eeg.std()
            else:
                mean = eeg.mean(axis=self.axis, keepdims=True)
                std = eeg.std(axis=self.axis, keepdims=True)
        elif not self.axis is None:
            shape = [-1] * len(eeg.shape)
            shape[self.axis] = 1
            mean = self.mean.reshape(*shape)
            std = self.std.reshape(*shape)
        return (eeg - mean) / std

    @property
    def repr_body(self) -> Dict:
        return dict(super().repr_body, **{
            'mean': self.mean,
            'std': self.std,
            'axis': self.axis
        })

class MinMaxNormalize(EEGTransform):
    r'''
    Perform min-max normalization on the input data. This class allows the user to define the dimension of normalization and the used statistic.

    .. code-block:: python

        transform = MinMaxNormalize(axis=0)
        # normalize along the first dimension (electrode dimension)
        transform(eeg=torch.randn(32, 128))['eeg'].shape
        >>> (32, 128)

        transform = MinMaxNormalize(axis=1)
        # normalize along the second dimension (temproal dimension)
        transform(eeg=torch.randn(32, 128))['eeg'].shape
        >>> (32, 128)

    Args:
        min (np.array, optional): The minimum used in the normalization process, allowing the user to provide minimum statistics in :obj:`np.ndarray` format. When statistics are not provided, use the statistics of the current sample for normalization.
        max (np.array, optional): The maximum used in the normalization process, allowing the user to provide maximum statistics in :obj:`np.ndarray` format. When statistics are not provided, use the statistics of the current sample for normalization.
        axis (int, optional): The dimension to normalize, when no dimension is specified, the entire data is normalized.
        apply_to_baseline: (bool): Whether to act on the baseline signal at the same time, if the baseline is passed in when calling. (defualt: :obj:`False`)
    
    .. automethod:: __call__
    '''
    def __init__(self,
                 min: Union[np.ndarray, None, float] = None,
                 max: Union[np.ndarray, None, float] = None,
                 axis: Union[int, None] = None,
                 apply_to_baseline: bool = False):
        super(MinMaxNormalize,
              self).__init__(apply_to_baseline=apply_to_baseline)
        self.min = min
        self.max = max
        self.axis = axis

    def __call__(self,
                 *args,
                 eeg: np.ndarray,
                 baseline: Union[np.ndarray, None] = None,
                 **kwargs) -> Dict[str, np.ndarray]:
        r'''
        Args:
            eeg (np.ndarray): The input EEG signals or features.
            baseline (torch.Tensor, optional) : The corresponding baseline signal, if apply_to_baseline is set to True and baseline is passed, the baseline signal will be transformed with the same way as the experimental signal.
            
        Returns:
            np.ndarray: The normalized results.
        '''
        return super().__call__(*args, eeg=eeg, baseline=baseline, **kwargs)

    def apply(self, eeg: np.ndarray, **kwargs) -> np.ndarray:
        if (self.min is None) or (self.max is None):
            if self.axis is None:
                min = eeg.min()
                max = eeg.max()
            else:
                min = eeg.min(axis=self.axis, keepdims=True)
                max = eeg.max(axis=self.axis, keepdims=True)
        elif not self.axis is None:
            shape = [-1] * len(eeg.shape)
            shape[self.axis] = 1
            min = self.min.reshape(*shape)
            max = self.max.reshape(*shape)

        return (eeg - min) / (max - min)
    
    @property
    def repr_body(self) -> Dict:
        return dict(super().repr_body, **{
            'min': self.min,
            'max': self.max,
            'axis': self.axis
        })
