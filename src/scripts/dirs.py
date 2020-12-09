from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_REPO = _this_file.parent.parent.parent.resolve()

DIR_IDEA = (DIR_REPO / ".idea").resolve()
DIR_SRC = (DIR_REPO / "src").resolve()
DIR_TESTS = (DIR_REPO / "tests").resolve()

DIR_SCRIPTS = (DIR_SRC / "scripts").resolve()
DIR_PROJECT = (DIR_SRC / "project").resolve()
DIR_APPS = (DIR_SRC / "applications").resolve()
