from pathlib import Path
import pytest


@pytest.fixture(autouse=True)
def monkey_patch_sys_paths(monkeypatch: pytest.MonkeyPatch):
    root_pkg = Path(__file__).parent
    monkeypatch.syspath_prepend(str(root_pkg))
