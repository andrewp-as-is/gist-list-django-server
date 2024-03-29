from http.client import parse_headers
import io
import json


class HeadersMixin:
    def get_headers(self):
        if self.headers:
            if self.headers[0] == "{":  # json
                return json.loads(self.headers)
            else:  # plain text
                fp = io.BytesIO(self.headers.encode())
                return dict(parse_headers(fp)) if fp else {}
        return {}
