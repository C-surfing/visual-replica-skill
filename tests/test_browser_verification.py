"""Real browser smoke test, skipped only when node/playwright are unavailable locally."""
import functools
import http.server
import shutil
import subprocess
import threading
from pathlib import Path

import pytest
import yaml

from visual_replica.verify import verify_contract


def test_real_browser_state_and_dom_evidence(tmp_path):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    repo = Path(__file__).resolve().parents[1]
    exists = subprocess.run(
        ["node", "-e", "import('playwright').catch(() => process.exit(1))"],
        cwd=repo, capture_output=True, check=False,
    )
    if exists.returncode:
        pytest.skip("Playwright not installed; run npm install")
    page = tmp_path / "web"
    page.mkdir()
    (page / "index.html").write_text(
        '<html><main id="hero"><button id="open" onclick="document.getElementById('
        "'menu').style.display='block'\">Open</button>"
        '<div id="menu" style="display:none">Navigation ready</div></main></html>',
        encoding="utf-8",
    )
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(page))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/"
        doc = {
            "version": 1, "mode": "transfer", "source": {"approved": True},
            "checks": {"scenarios": [{
                "id": "menu-open", "url": url,
                "viewport": {"width": 390, "height": 844, "dpr": 1},
                "ready_selector": "#hero",
                "actions": [{"type": "click", "selector": "#open"}],
                "assertions": [{"selector": "#menu", "condition": "visible"},
                               {"selector": "#menu", "condition": "text_contains",
                                "value": "Navigation ready"}],
                "inspect_selectors": ["#hero", "#menu"],
            }]},
        }
        spec = tmp_path / "intent.yaml"
        spec.write_text(yaml.safe_dump(doc), encoding="utf-8")
        result = verify_contract(spec, tmp_path / "verification")
        assert result["status"] == "REVIEW_REQUIRED"  # No visual baseline; never false-pass.
        evidence = result["scenarios"][0]["browser"]
        assert evidence["status"] == "PASS", evidence.get("error")
        assert all(x["passed"] for x in evidence["assertions"])
        assert evidence["dom"][0]["bounds"]["width"] > 0
        assert (tmp_path / "verification" / "menu-open" / "screenshot.png").is_file()
    finally:
        server.shutdown()
        server.server_close()
