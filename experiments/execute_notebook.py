"""Execute the notebook with the active Python environment and retain real outputs."""
import os
import sys
from pathlib import Path
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="dsaa-jupyter-") as runtime:
    os.environ.setdefault("IPYTHONDIR", runtime)
    os.environ.setdefault("JUPYTER_RUNTIME_DIR", runtime)
    os.environ.setdefault("MPLCONFIGDIR", str(Path(runtime) / "matplotlib"))
    os.environ.setdefault("XDG_CACHE_HOME", str(Path(runtime) / "cache"))
    notebook = nbformat.read(root / "project.ipynb", as_version=4)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=180,
                            resources={"metadata": {"path": str(root)}},
                            record_timing=False)
    client.execute()
    nbformat.validate(notebook)
    nbformat.write(notebook, root / "project.ipynb")
    completed = [c for c in notebook.cells if c.cell_type == "code"]
    assert all(c.execution_count is not None for c in completed)
    assert not any(o.output_type == "error" for c in completed for o in c.outputs)
    print(f"Executed and validated {len(completed)} notebook code cells.")
