"""
Smithery configuration middleware for extracting config from URL parameters.
This middleware handles the base64-encoded configuration that Smithery sends
via URL query parameters when establishing HTTP connections.
"""

import json
import base64
from urllib.parse import parse_qs, unquote


class SmitheryConfigMiddleware:
    """
    Middleware to extract Smithery configuration from URL query parameters.
    
    Smithery sends configuration as a base64-encoded JSON object in the 
    'config' query parameter. This middleware extracts and decodes it,
    then passes it to a callback function for processing.
    """
    
    def __init__(self, app, config_callback):
        """
        Initialize the middleware.
        
        Args:
            app: The ASGI application to wrap
            config_callback: Function to call with extracted config dict
        """
        self.app = app
        self.config_callback = config_callback

    async def __call__(self, scope, receive, send):
        """
        Process incoming requests and extract config if present.
        
        Args:
            scope: ASGI scope dict
            receive: ASGI receive callable
            send: ASGI send callable
        """
        if scope.get('type') == 'http':
            # Extract query string from the request
            query_string = scope.get('query_string', b'').decode('utf-8')
            
            # Check if config parameter is present
            if 'config=' in query_string:
                try:
                    # Parse query parameters
                    parsed_query = parse_qs(query_string)
                    
                    if 'config' in parsed_query:
                        # Get the first config value (URL-decoded)
                        config_b64 = unquote(parsed_query['config'][0])
                        
                        # Decode base64 and parse JSON
                        config_json = base64.b64decode(config_b64).decode('utf-8')
                        config = json.loads(config_json)
                        
                        # Call the callback with extracted config
                        self.config_callback(config)
                        
                        print(f"SmitheryConfigMiddleware: Successfully extracted config with keys: {list(config.keys())}")
                    
                except json.JSONDecodeError as e:
                    print(f"SmitheryConfigMiddleware: Failed to parse config JSON: {e}")
                except base64.binascii.Error as e:
                    print(f"SmitheryConfigMiddleware: Failed to decode base64 config: {e}")
                except Exception as e:
                    print(f"SmitheryConfigMiddleware: Unexpected error parsing config: {e}")
        
        # Continue processing the request
        await self.app(scope, receive, send)