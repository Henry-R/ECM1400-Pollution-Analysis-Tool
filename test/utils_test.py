import pytest

import sys
sys.path.insert(0,'..')

from math import pi
import utils

import numpy as np

# The test data
A = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
Af = np.array([-5.42, -4.13, -3.242, -2.21, -1.351, 0, 1, 2.0001, pi, 4.123, 5.9999])
A_err = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 'hello']

def test_utils_sum():
    output = utils.sumvalues(A)
    assert output == sum(A)

    output = utils.sumvalues(Af)
    assert output == sum(Af)

    with pytest.raises(Exception):
        output = utils.sumvalues(A_err)

def test_utils_max():
    output = utils.maxvalue(A)
    assert output == max(A)

    output = utils.maxvalue(Af)
    assert output == max(Af)

    with pytest.raises(Exception):
        output = utils.maxvalue(A_err)

def test_utils_min():
    output = utils.minvalue(A)
    assert output == min(A)

    output = utils.minvalue(Af)
    assert output == min(Af)

    with pytest.raises(Exception):
        output = utils.min(A_err)

def test_utils_mean():
    output = utils.meannvalue(A)
    assert output == sum(A) / len(A)

    output = utils.meannvalue(Af)
    assert output == sum(Af) / len(Af)

    with pytest.raises(Exception):
        output = utils.meannvalue(A_err)

def test_utils_count():
    output = utils.countvalue(A, -3)
    assert output == len([i for i in A if i == -3])

    output = utils.countvalue(Af, -3)
    assert output == len([i for i in Af if i == -3])

    with pytest.raises(Exception):
        output = utils.countvalue(A_err, -3)