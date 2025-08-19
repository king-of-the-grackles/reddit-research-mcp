import json
import base64
from urllib.parse import parse_qs, unquote


class SmitheryConfigMiddleware:
    """ASGI middleware to extract Smithery configuration from query parameters."""
    
    def __init__(self, app, config_callback):
        self.app = app
        self.config_callback = config_callback
    
    async def __call__(self, scope, receive, send):
        if scope.get('type') == 'http':
            query = scope.get('query_string', b'').decode()
            
            if 'config=' in query:
                try:
                    config_b64 = unquote(parse_qs(query)['config'][0])
                    config = json.loads(base64.b64decode(config_b64))
                    self.config_callback(config)
                    print(f"SmitheryConfigMiddleware: Extracted config: {list(config.keys())}")
                except Exception as e:
                    print(f"SmitheryConfigMiddleware: Error parsing config: {e}")
        
        await self.app(scope, receive, send)