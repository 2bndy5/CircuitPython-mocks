from pathlib import Path
import pytest


@pytest.fixture(autouse=True)
def monkey_patch_sys_paths(monkeypatch: pytest.MonkeyPatch):
    """A pytest fixture that monkey patches the Python runtime's import paths, such
    that this package's mock modules can be imported first (instead from the
    adafruit-blinka package).

    .. important::

        This fixture is automatically used once imported into the test module.
    """
    root_pkg = Path(__file__).parent
    monkeypatch.syspath_prepend(str(root_pkg))
