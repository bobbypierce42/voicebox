"""The frozen-app NumPy fallback must preserve the source tensor dtype."""

import runpy
import time
from pathlib import Path

import numpy as np
import pytest
import torch


@pytest.mark.parametrize("dtype", ["float16", "int64", "complex64"])
def test_runtime_hook_recovers_from_numpy_abi_error(monkeypatch, dtype):
    def unavailable(_array):
        raise RuntimeError("Numpy is not available")

    monkeypatch.setattr(torch, "from_numpy", unavailable)
    monkeypatch.setattr(torch, "_vb_from_numpy_patched", False, raising=False)
    hook = Path(__file__).resolve().parents[1] / "pyi_rth_numpy_compat.py"
    runpy.run_path(str(hook))

    deadline = time.monotonic() + 5
    while torch.from_numpy is unavailable and time.monotonic() < deadline:
        time.sleep(0.01)

    array = np.array([1, 2, 3], dtype=dtype)
    tensor = torch.from_numpy(array)
    assert tensor.dtype == getattr(torch, dtype)
    np.testing.assert_array_equal(tensor.numpy(), array)
