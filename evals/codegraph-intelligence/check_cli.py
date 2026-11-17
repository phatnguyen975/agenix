"""Exercise CodeGraph 1.6.2 query contracts in disposable fixtures, not a real project.

Run from any working directory: python <path-to-this-file>
Requires the existing CLI on PATH; never downloads or installs dependencies.
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def main():
    cli = shutil.which("codegraph")
    if not cli:
        raise RuntimeError("CodeGraph CLI unavailable; integration checks unrun")
    env = dict(
        os.environ,
        CODEGRAPH_TELEMETRY="0",
        CODEGRAPH_NO_DOWNLOAD="1",
        CODEGRAPH_NO_DAEMON="1",
    )

    def run(*args, ok=True):
        result = subprocess.run(
            [cli, *args],
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
            check=False,
        )
        if ok and result.returncode:
            raise RuntimeError(f"CLI failed: {args}: {result.stderr}")
        return result

    if run("--version").stdout.strip() != "1.6.2":
        raise RuntimeError(
            "These interface assertions target 1.6.2; other versions unrun"
        )

    with tempfile.TemporaryDirectory(prefix="cg-query-check-") as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "tests").mkdir()
        sources = {
            "src/math.js": "export function addTax(value) { return value * 1.1; }\n",
            "src/service.js": "import { addTax } from './math.js';\n"
            "export function total(value) { return addTax(value); }\n",
            "tests/service.test.js": "import { total } from '../src/service.js';\n"
            "export function testTotal() { return total(10); }\n",
        }
        for name, content in sources.items():
            (root / name).write_text(content, encoding="utf-8")
        # Build the fixture index only; runtime skill use assumes a prepared index.
        run("init", str(root), "--yes")

        def query(command, *args):
            return run(command, *args, "--path", str(root))

        def data(command, *args):
            return json.loads(query(command, *args, "--json").stdout)

        status = json.loads(run("status", str(root), "--json").stdout)
        assert status["initialized"] and status["fileCount"] == 3
        assert status["index"]["state"] == "complete"
        assert any(x["node"]["name"] == "addTax" for x in data("query", "addTax"))
        assert any(x["name"] == "total" for x in data("callers", "addTax")["callers"])
        assert any(x["name"] == "addTax" for x in data("callees", "total")["callees"])
        impact = data("impact", "addTax", "--depth", "3")
        assert impact["depth"] == 3
        assert any(x["name"] == "testTotal" for x in impact["affected"])
        assert (
            "tests/service.test.js" in data("affected", "src/math.js")["affectedTests"]
        )
        assert {x["path"] for x in data("files", "--filter", "src")} == {
            "src/math.js",
            "src/service.js",
        }
        assert "addTax" in query("node", "--file", "src/math.js").stdout
        assert "src/math.js" in query("explore", "addTax", "--max-files", "3").stdout
        context = json.loads(
            query("context", "change addTax", "--format", "json").stdout
        )
        assert any(x["name"] == "addTax" for x in context["nodes"])
        assert data("query", "NoSuchSymbolInThisFixture") == []
        invalid = run("impact", "addTax", "--not-a-real-option", ok=False)
        assert invalid.returncode != 0
        unindexed = root / "unindexed"
        unindexed.mkdir()
        inherited = json.loads(run("status", str(unindexed), "--json").stdout)
        assert Path(inherited["projectPath"]).resolve() == root.resolve()
        assert not (unindexed / ".codegraph").exists()
        with tempfile.TemporaryDirectory(prefix="cg-no-index-") as missing_directory:
            missing = run("status", missing_directory, "--json", ok=False)
            assert (
                missing.returncode != 0 or not json.loads(missing.stdout)["initialized"]
            )
            assert not (Path(missing_directory) / ".codegraph").exists()
        (root / "src/math.js").write_text(
            sources["src/math.js"] + "// changed\n", encoding="utf-8"
        )
        stale = json.loads(run("status", str(root), "--json").stdout)
        assert stale["pendingChanges"]["modified"] >= 1
        for name, content in sources.items():
            expected = content + ("// changed\n" if name == "src/math.js" else "")
            assert (root / name).read_text(encoding="utf-8") == expected
    print(
        "PASS: 1.6.2 query contracts, missing index/symbol, invalid flag and stale-file detection"
    )


if __name__ == "__main__":
    main()
