# Kiro MCP Registry

MCP server allow-list for Kiro enterprise governance. Host this over HTTPS and configure the URL in the Kiro admin console to control which MCP servers your users can access.

**Schema reference:** [Kiro MCP Registry JSON Schema](https://kiro.dev/docs/enterprise/governance/mcp/#mcp-registry-json-schema)

---

## Files

| File | Purpose |
|---|---|
| `mcp-registry.json` | The registry file — host this over HTTPS |
| `validate-registry.py` | Validates the registry against the Kiro schema |

---

## Prerequisites for Users

Remote servers (using `remotes`) connect over HTTPS — no local tooling needed.

Local servers (using `packages`) require a package runner on user machines:

| registryType | Runner needed | Install |
|---|---|---|
| `pypi` | `uv` (`uvx` on Mac/Linux, `uv tool run` on Windows) | [uv](https://docs.astral.sh/uv/getting-started/installation/) |
| `npm` | `npx` | [Node.js](https://nodejs.org/) |
| `oci` | `docker` | [Docker](https://docs.docker.com/get-docker/) |

---

## Validate

```bash
# Using a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows
pip install jsonschema
python validate-registry.py mcp-registry.json
```

Or with uv:

```bash
uv run --with jsonschema validate-registry.py mcp-registry.json
```

Expected: `PASSED - mcp-registry.json is valid.`

---

## Deploy

1. Validate the registry (see above).
2. Host `mcp-registry.json` on any HTTPS endpoint with a valid CA-signed certificate.
3. In the [Kiro console](https://app.kiro.dev) → Settings → Shared settings, set MCP to On and paste the URL in MCP Registry URL.

Kiro fetches the registry at startup and re-syncs every 24 hours.

---

## Add a Server

### Remote (HTTP)

```json
{
  "server": {
    "name": "my-remote-server",
    "title": "My Server",
    "description": "What this server does (max 100 chars).",
    "version": "1.0.0",
    "remotes": [
      {
        "type": "streamable-http",
        "url": "https://example.com/mcp"
      }
    ]
  }
}
```

### Local (stdio)

```json
{
  "server": {
    "name": "my-local-server",
    "title": "My Server",
    "description": "What this server does (max 100 chars).",
    "version": "2.0.0",
    "packages": [
      {
        "registryType": "npm",
        "identifier": "@scope/my-mcp-server",
        "transport": { "type": "stdio" },
        "environmentVariables": [
          { "name": "MY_VAR", "value": "${MY_VAR}" }
        ]
      }
    ]
  }
}
```

### Rules

- `name`: unique, 3-200 chars, `a-zA-Z0-9._-` only
- `description`: max 100 chars
- `version`: semver recommended (e.g., `1.0.0`)
- Each server has either `remotes` or `packages`, not both
- `${VAR}` placeholders let users supply their own values
- Always validate after editing

---

## Update a Server Version

1. Update the `version` field in `mcp-registry.json`.
2. Validate and redeploy.

Kiro relaunches with the new version within 24 hours or on next startup.

---

## What Users Can Override

- Environment variables and HTTP headers
- Request timeout
- Server scope (Global, Workspace, or Agent Configuration)
- Tool trust permissions

---

## References

### Kiro

- [Kiro MCP Governance Docs](https://kiro.dev/docs/enterprise/governance/mcp/)
- [Kiro MCP Registry JSON Schema](https://kiro.dev/docs/enterprise/governance/mcp/#mcp-registry-json-schema)
- [MCP Registry Open Standard](https://github.com/modelcontextprotocol/registry)

### Servers in this registry

| Server | Docs |
|---|---|
| AWS Documentation MCP | [awslabs.github.io](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server) · [PyPI](https://pypi.org/project/awslabs.aws-documentation-mcp-server/) |
| AWS Support MCP | [awslabs.github.io](https://awslabs.github.io/mcp/servers/aws-support-mcp-server) · [PyPI](https://pypi.org/project/awslabs.aws-support-mcp-server/) |
| Lucid | [Lucid Help Center](https://lucidco.zendesk.com/hc/en-us/articles/42578801807508) |
| GitHub | [GitHub Docs](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/set-up-the-github-mcp-server) |
| Figma | [Figma Learn](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) |
| Dynatrace | [npm](https://www.npmjs.com/package/@dynatrace-oss/dynatrace-mcp-server) · [GitHub](https://github.com/dynatrace-oss/dynatrace-mcp) |
