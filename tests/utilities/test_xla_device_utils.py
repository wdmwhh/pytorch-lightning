# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from pytorch_lightning.utilities.xla_device_utils import XLADeviceUtils as xdu
from tests.base.develop_utils import pl_multi_process_test

try:
    import torch_xla.core.xla_model as xm
    XLA_AVAILABLE = True
except ImportError as e:
    XLA_AVAILABLE = False


@pytest.mark.skipif(XLA_AVAILABLE, reason="test requires torch_xla to be absent")
def test_tpu_device_absence():
    """Check tpu_device_exists returns None when torch_xla is not available"""
    assert xdu.tpu_device_exists() is None


@pytest.mark.skipif(not XLA_AVAILABLE, reason="test requires torch_xla to be installed")
def test_tpu_device_presence():
    """Check tpu_device_exists returns True when TPU is available"""
    assert xdu.tpu_device_exists() is True


@pytest.mark.skipif(not XLA_AVAILABLE, reason="test requires torch_xla to be installed")
@pl_multi_process_test
def test_xla_device_is_a_tpu():
    """Check that the XLA device is a TPU"""
    device = xm.xla_device()
    device_type = xm.xla_device_hw(device)
    return device_type == "TPU"
