#!/usr/bin/env python3
"""Validate mcp-registry.json against the Kiro MCP Registry JSON Schema."""

import json
import sys

try:
    import jsonschema
except ImportError:
    print("Installing jsonschema...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "-q"])
    import jsonschema

SCHEMA = {
    "$schema": "https://json-schema.org/draft-07/schema",
    "properties": {
        "servers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "server": {"$ref": "#/definitions/ServerDetail"}
                },
                "required": ["server"],
            },
        }
    },
    "definitions": {
        "ServerDetail": {
            "properties": {
                "name": {
                    "description": "Server name. Must be unique within a given registry file.",
                    "maxLength": 200,
                    "minLength": 3,
                    "pattern": "^[a-zA-Z0-9._-]+$",
                    "type": "string",
                },
                "title": {
                    "maxLength": 100,
                    "minLength": 1,
                    "type": "string",
                },
                "description": {
                    "maxLength": 100,
                    "minLength": 1,
                    "type": "string",
                },
                "version": {
                    "maxLength": 255,
                    "type": "string",
                },
                "packages": {
                    "items": {"$ref": "#/definitions/Package"},
                    "type": "array",
                    "minItems": 0,
                    "maxItems": 1,
                },
                "remotes": {
                    "items": {
                        "anyOf": [
                            {"$ref": "#/definitions/StreamableHttpTransport"},
                            {"$ref": "#/definitions/SseTransport"},
                        ]
                    },
                    "type": "array",
                    "minItems": 0,
                    "maxItems": 1,
                },
            },
            "required": ["name", "description", "version"],
            "type": "object",
        },
        "Package": {
            "properties": {
                "registryType": {
                    "enum": ["npm", "pypi", "oci"],
                    "type": "string",
                },
                "registryBaseUrl": {
                    "format": "uri",
                    "type": "string",
                },
                "identifier": {"type": "string"},
                "transport": {
                    "anyOf": [
                        {"$ref": "#/definitions/StdioTransport"},
                        {"$ref": "#/definitions/StreamableHttpTransport"},
                        {"$ref": "#/definitions/SseTransport"},
                    ]
                },
                "runtimeArguments": {
                    "items": {"$ref": "#/definitions/PositionalArgument"},
                    "type": "array",
                },
                "packageArguments": {
                    "items": {"$ref": "#/definitions/PositionalArgument"},
                    "type": "array",
                },
                "environmentVariables": {
                    "items": {"$ref": "#/definitions/KeyValueInput"},
                    "type": "array",
                },
            },
            "required": ["registryType", "identifier", "transport"],
            "type": "object",
        },
        "StdioTransport": {
            "properties": {"type": {"enum": ["stdio"], "type": "string"}},
            "required": ["type"],
            "type": "object",
        },
        "StreamableHttpTransport": {
            "properties": {
                "type": {"enum": ["streamable-http"], "type": "string"},
                "url": {"type": "string"},
                "headers": {
                    "items": {"$ref": "#/definitions/KeyValueInput"},
                    "type": "array",
                },
            },
            "required": ["type", "url"],
            "type": "object",
        },
        "SseTransport": {
            "properties": {
                "type": {"enum": ["sse"], "type": "string"},
                "url": {"format": "uri", "type": "string"},
                "headers": {
                    "items": {"$ref": "#/definitions/KeyValueInput"},
                    "type": "array",
                },
            },
            "required": ["type", "url"],
            "type": "object",
        },
        "PositionalArgument": {
            "properties": {
                "type": {"enum": ["positional"], "type": "string"},
                "value": {"type": "string"},
            },
            "required": ["type", "value"],
            "type": "object",
        },
        "KeyValueInput": {
            "properties": {
                "name": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["name"],
            "type": "object",
        },
    },
    "required": ["servers"],
    "type": "object",
}


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "mcp-registry.json"
    with open(filepath) as f:
        data = json.load(f)
    try:
        jsonschema.validate(instance=data, schema=SCHEMA)
        print(f"PASSED - {filepath} is valid.")
    except jsonschema.ValidationError as e:
        print(f"FAILED: {e.message}")
        print(f"  Path: {' > '.join(str(p) for p in e.absolute_path)}")
        sys.exit(1)
