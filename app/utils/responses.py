import json
from fastapi.responses import Response

class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=True,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode("utf-8")
