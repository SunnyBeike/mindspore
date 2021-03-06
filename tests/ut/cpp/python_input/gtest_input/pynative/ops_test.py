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
""" ops_test """
import numpy as np
from mindspore.ops import operations as P
from mindspore.ops.vm_impl_registry import vm_impl_registry as vm_impl_getters
from mindspore.common.tensor import Tensor

def im2col(img, filter_h, filter_w, stride=1, pad=0, dilation=1):
    """Rearranges an image to row vector"""
    batch_num, channel, height, width = img.shape
    out_h = (height + 2*pad - filter_h - (filter_h - 1) * (dilation - 1))//stride + 1
    out_w = (width + 2*pad - filter_w - (filter_w - 1) * (dilation - 1))//stride + 1

    img = np.pad(img, [(0, 0), (0, 0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((batch_num, channel, filter_h, filter_w, out_h, out_w)).astype(img.dtype)

    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(batch_num*out_h*out_w, -1)
    return col

# pylint: disable=unused-argument
def conv2d(x, weight, bias=None, stride=1, pad=0,
           dilation=1, groups=1, padding_mode='zeros'):
    """Convolution 2D"""
    batch_num, _, x_h, x_w = x.shape
    filter_num, _, filter_h, filter_w = weight.shape
    out_h = 1 + int((x_h + 2 * pad - filter_h - (filter_h - 1) * (dilation - 1)) / stride)
    out_w = 1 + int((x_w + 2 * pad - filter_w - (filter_w - 1) * (dilation - 1)) / stride)
    col = im2col(x, filter_h, filter_w, stride, pad, dilation)
    col_w = np.reshape(weight, (filter_num, -1)).T
    out = np.dot(col, col_w)
    out = out.reshape(batch_num, out_h, out_w, -1).transpose(0, 3, 1, 2)
    if bias is not None:
        out += bias
    return out


@vm_impl_getters.register(P.Conv2D)
def vm_impl_conv2d(self):
    """Generate vm_impl function for Conv2D"""
    def vm_impl(x, w):
        x = x.asnumpy()
        weight = w.asnumpy()
        bias = None
        out = conv2d(x, weight, bias, self.stride, self.pad, self.dilation)
        return Tensor(out)
    return vm_impl


conv2d_prim = P.Conv2D(64, (3, 3), pad_mode='pad', pad=1, stride=2)
