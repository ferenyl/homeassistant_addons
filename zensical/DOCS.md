# zensical Documentation Generator

Generate and serve beautiful documentation using zensical with support for local folders and Git repositories.

## Configuration

### Source Type: Local Folder

Use this option when your documentation files are stored locally in Home Assistant.

```yaml
source_type: "local"
local_path: "" (leave this empty for default folder)
```

**Setup Steps:**

1. Create a folder in your Home Assistant configuration directory
2. Create a `docs/` subfolder for your markdown files
3. Add your content to the `docs/` folder
4. Optionally create a custom `zensical.toml` configuration file

**Example folder structure:**

```
/config/zensical/
├── zensical.toml (optional)
├── docs/
│   ├── index.md
│   ├── about.md
│   └── assets/
│       └── images/
```

### Source Type: Git Repository

Use this option to automatically pull documentation from a Git repository.

```yaml
source_type: "git"
git_url: "git@github.com:username/docs-repo.git"
ssh_key_path: "/ssl/zensical_ssh_key"
```

**Setup Steps:**

1. Generate an SSH key pair for repository access
2. Add the public key to your Git repository as a deploy key
3. Copy the private key to Home Assistant (e.g., in `/ssl/` folder)
4. Configure the Git URL and SSH key path
5. The add-on will automatically clone/pull the latest changes

**Supported Git URLs:**

- SSH: `git@github.com:username/repo.git`
- SSH with custom port: `ssh://git@github.com:2222/username/repo.git`

## Advanced Configuration

### Ports and Access

- **Ingress**: Served via Home Assistant ingress on the add-on's configured ingress port (default 8000). This is automatic.
- **Direct access**: Exposed on container port 8080. Map `8080/tcp` to a host port in the add-on UI to access without ingress, e.g., `http://<ha-host>:<host-port>`.
- **API Access**: HTTP API available on container port 8084 for automation integration. Map `8084/tcp` to a host port if needed.

### SSH Keys

- Key types: Ed25519 (recommended) or RSA 4096
- Private key path: Configure `ssh_key_path` (default `/ssl/zensical_ssh_key`)
- Public key: Add the `.pub` as a Deploy Key in your Git host
- Passphrase: Leave empty (not supported interactively)
- Permissions: `chmod 600` on the private key

Generate keys in `/ssl`:

```bash
ssh-keygen -t ed25519 -C "homeassistant-zensical" -f /ssl/zensical_ssh_key -N ""
# or
ssh-keygen -t rsa -b 4096 -C "homeassistant-zensical" -f /ssl/zensical_ssh_key -N ""
cat /ssl/zensical_ssh_key.pub
```

## Pre-installed Features

### Plugins

- **Material Theme**: Modern, responsive design
- **Mermaid2**: Create diagrams with Mermaid syntax
- **Minify**: Optimize HTML, CSS, and JavaScript
- **Git Revision Date**: Show last modified dates
- **Awesome Pages**: Enhanced navigation control

### Markdown Extensions

- Admonitions (callout boxes)
- Code highlighting
- Table of contents
- Math expressions
- Emoji support
- Task lists
- And many more...

## Default Configuration

If no `zensical.toml` file exists in your source, the add-on will create one with sensible defaults:

- Material theme with light/dark mode toggle
- Search functionality
- Navigation tabs
- Mermaid diagram support
- Code syntax highlighting
- Social links section
- Optimized performance settings

## Using the Documentation

### Accessing Your Site

1. **Home Assistant Ingress**: Click "Open Web UI" in the add-on interface
2. **Direct Access**: Visit `http://homeassistant.local:<host-port>` (the port you mapped to container 8080)

### Writing Content

Create markdown files in the `docs/` folder:

**docs/index.md** (Homepage):

````markdown
# Welcome to My Documentation

This is the homepage of my documentation site.

## Features

- Easy to write in Markdown
- Beautiful Material Design theme
- Search functionality
- Mobile responsive

## Mermaid Diagrams

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Fix it]
    D --> B
```
````


## Automation Integration

The add-on includes a built-in HTTP API for triggering documentation rebuilds from Home Assistant automations and scripts.

### API Configuration

The API runs on port 8084 and provides these endpoints:

- `POST /rebuild` - Trigger documentation rebuild
- `POST /webhook` - Webhook endpoint (same as rebuild)
- `GET /status` - Check API status
- `GET /health` - Health check

### Home Assistant Integration

Add to your `configuration.yaml`:

1. Find the add-on hostname (inside Home Assistant OS):

```bash
ha addons info <addon_slug> | grep '^hostname:'
```

1. Use that hostname in your REST command URL:

```yaml
rest_command:
  zensical_rebuild:
    url: "http://<addon-hostname>:8084/rebuild"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: "{}"
    timeout: 30

script:
  rebuild_zensical:
    alias: "Rebuild zensical Documentation"
    icon: mdi:book-refresh
    sequence:
      - service: rest_command.zensical_rebuild
```

    Example from a local dev install where slug is `local_zensical`: `http://local-zensical:8084/rebuild`

### Usage in Scripts and Automations

**Manual Script (callable from UI):**

1. Create a script in Home Assistant UI
2. Add action: Call service `rest_command.zensical_rebuild`
3. The script will appear in your Scripts dashboard

**Automation Example:**

```yaml
automation:
  - alias: "Daily docs rebuild"
    trigger:
      - platform: time
        at: "02:00:00"
    action:
      - service: rest_command.zensical_rebuild
```

### External Integration

**From curl:**

```bash
curl -X POST http://<home-assistant-host>:<mapped-port>/rebuild
```

**From Node-RED:**
Use an HTTP request node with POST method to `http://<addon-hostname>:8084/rebuild`

**Webhook Integration:**
Configure your Git repository to send webhooks to `http://<home-assistant-host>:<mapped-port>/webhook` on push events.

## Support

For questions and issues:

1. Check the add-on logs for error messages
2. Verify your configuration matches the examples
3. Consult the [zensical documentation](https://zensical.org/docs/)
4. Open an issue on the GitHub repository
