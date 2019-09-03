import numpy
from chainer.dataset.convert import _concat_arrays


def padding(name, batch, device=None, pad=0):
    feat = _concat_arrays(
        [getattr(example, name) for example in batch], pad)
    return device.send(feat)


def concat(name, batch, device=None, axis=0):
    feat = numpy.concatenate([getattr(data, name) for data in batch],
                             axis=axis)
    return device.send(feat)


def shift_concat(name, batch, device=None, shift_attr='x', shift_axis=0):
    shift_index_array = numpy.cumsum(
        numpy.array([0] + [getattr(data, shift_attr).shape[shift_axis] for data in batch]))
    feat = numpy.concatenate([
        getattr(data, name) + shift_index_array[i]
        for i, data in enumerate(batch)], axis=0)
    return device.send(feat)


def create_index(name, batch, device=None, shift_attr='x', shift_axis=0):
    # name is not used.
    batch_index = numpy.array([
        numpy.ones(getattr(data, shift_attr).shape[shift_axis],
                   dtype=numpy.int32) * i for i, data in enumerate(batch)])
    return device.send(batch_index)
