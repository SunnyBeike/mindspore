# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
""" test_backend """
import numpy as np
import pytest
from mindspore.ops import operations as P
import mindspore.nn as nn
from mindspore import context
from mindspore.common.initializer import initializer
from mindspore.common.parameter import Parameter
from mindspore._extends.pynative_helper import args_type_check
from mindspore.common.tensor import Tensor
from mindspore.common.api import ms_function


def setup_module(module):
    context.set_context(mode=context.PYNATIVE_MODE)


class Net(nn.Cell):
    """ Net definition """
    def __init__(self):
        super(Net, self).__init__()
        self.add = P.TensorAdd()
        self.x = Parameter(initializer('normal', [1, 3, 3, 4]), name='x')
        self.y = Parameter(initializer('normal', [1, 3, 3, 4]), name='y')

    @ms_function
    def construct(self):
        return self.add(self.x, self.y)


def test_vm_backend():
    """ test_vm_backend """
    context.set_context(mode=context.PYNATIVE_MODE)
    add = Net()
    output = add()
    assert output.asnumpy().shape == (1, 3, 3, 4)

def test_vm_set_context():
    """ test_vm_set_context """
    context.set_context(save_graphs=True, save_graphs_path="/home/mindspore", mode=context.GRAPH_MODE)
    assert context.get_context("save_graphs")
    assert context.get_context("mode") == context.GRAPH_MODE
    assert context.get_context("save_graphs_path") == "/home/mindspore"
    context.set_context(mode=context.PYNATIVE_MODE)

@args_type_check(v_str=str, v_int=int, v_tuple=tuple)
def check_input(v_str, v_int, v_tuple):
    """ check_input """
    print("v_str:", v_str)
    print("v_int:", v_int)
    print("v_tuple:", v_tuple)


def test_args_type_check():
    """ test_args_type_check """
    with pytest.raises(TypeError):
        check_input(100, 100, (10, 10))
    with pytest.raises(TypeError):
        check_input("name", "age", (10, 10))
    with pytest.raises(TypeError):
        check_input("name", 100, "age")
    check_input("name", 100, (10, 10))
