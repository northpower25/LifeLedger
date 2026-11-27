import json
from pathlib import Path

from lifeledger.app import create_app

contract = create_app(":memory:").openapi()
destination = Path(__file__).resolve().parents[2] / "docs" / "implementation" / "openapi.json"
destination.write_text(
    json.dumps(contract, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
