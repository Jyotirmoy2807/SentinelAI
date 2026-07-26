import json
from typing import Any


def json_safe(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))
