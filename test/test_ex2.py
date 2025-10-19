import os
import sys
import subprocess
import tempfile

SCRIPT = os.path.abspath("lab2ex2.py")
PY = sys.executable

def run_args(args, input_bytes=None):
    proc = subprocess.run([PY, SCRIPT] + args, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode('utf-8', errors='replace'), proc.stderr.decode('utf-8', errors='replace')

def make_temp_file(content):
    fd, path = tempfile.mkstemp(text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def test_help_exits_without_filepath():
    code, out, err = run_args(["--help"])
    assert code == 0
    assert "usage" in out.lower() or "usage" in err.lower()

def test_basic_unique_collapses_duplicates_nonadjacent():
    content = "a\nb\na\nc\nb\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args([path])
        assert code == 0
        lines = out.strip().splitlines()
        assert set(lines) == {"a", "b", "c"}
        assert len(lines) == 3
    finally:
        os.remove(path)

def test_count_prefix_shows_frequencies():
    content = "x\nx\ny\nx\nz\nz\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-c", path])
        assert code == 0
        lines = out.strip().splitlines()
        mapping = {}
        for line in lines:
            parts = line.strip().split(maxsplit=1)
            mapping[parts[1]] = int(parts[0])
        assert mapping.get("x") == 3
        assert mapping.get("y") == 1
        assert mapping.get("z") == 2
    finally:
        os.remove(path)

def test_duplicates_flag_only_prints_duplicates():
    content = "a\nb\na\nc\nb\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-d", path])
        assert code == 0
        lines = out.strip().splitlines()
        assert set(lines) == {"a", "b"}
        assert "c" not in lines
    finally:
        os.remove(path)

def test_unique_flag_only_prints_unique_lines():
    content = "a\nb\na\nc\nb\nd\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-u", path])
        assert code == 0
        lines = out.strip().splitlines()
        assert set(lines) == {"c", "d"}
        assert "a" not in lines
        assert "b" not in lines
    finally:
        os.remove(path)

def test_verbose_shows_header_and_path():
    content = "one\ntwo\none\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-v", path])
        assert code == 0
        assert "==>" in out
        assert os.path.basename(path) in out or path in out
    finally:
        os.remove(path)

def test_reads_from_stdin_when_piped():
    content = "m\nn\nm\n"
    proc = subprocess.run([PY, SCRIPT], input=content.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = proc.stdout.decode("utf-8", errors="replace")
    assert proc.returncode == 0
    lines = out.strip().splitlines()
    assert set(lines) == {"m", "n"}

def test_error_when_filepath_missing_and_no_stdin_shows_usage():
    proc = subprocess.run([PY, SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = proc.stdout.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace")
    assert proc.returncode == 0 or proc.returncode == 2
    assert ("usage" in out.lower()) or ("usage" in err.lower()) or ("the following arguments are required" in err.lower())
