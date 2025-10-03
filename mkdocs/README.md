# MkDocs Home Assistant Add-on

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

A Home Assistant add-on that generates and serves beautiful documentation using MkDocs. Supports both local folders and Git repositories as source.

## Features

- **MkDocs with Material Theme**: Beautiful, responsive documentation
- **Plugin Support**: Includes Mermaid2 and Minify plugins with ability to add more
- **Multiple Source Types**:

  - Local Home Assistant folders
  - Git repositories (with SSH key support)

- **Default Configuration**: Provides sensible defaults if no mkdocs.yml exists
- **Nginx Serving**: Optimized static file serving with caching
- **Home Assistant Ingress**: Seamless integration with Home Assistant UI
- **Automation API**: HTTP API for rebuilding docs from automations and scripts
- **RESTful Integration**: Easy integration with Home Assistant automations via REST commands

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "MkDocs" add-on
3. Configure the add-on (see Configuration section)
4. Start the add-on

## Configuration

### Basic Configuration

```yaml
source_type: "local"
local_path: "/config/mkdocs"
```

### Git Repository Configuration

```yaml
source_type: "git"
git_url: "git@github.com:username/docs-repo.git"
ssh_key_path: "/ssl/mkdocs_ssh_key"
```

### Ports and Access

- Managed in Supervisor → Add-on → Configuration → Network.
- Ingress: Handled automatically by Home Assistant using the add-on's internal port.
- Direct access: Map container port `8080/tcp` to any host port to access without ingress, e.g., `http://<home-assistant-host>:<host-port>`.

### SSH Keys

The add-on supports authenticating to private Git repositories over SSH.

- Key types: Ed25519 (recommended) or RSA (4096-bit). Both work.
- Private key path: Set via `ssh_key_path` (default: `/ssl/mkdocs_ssh_key`).
- File names: You can name the private key file anything on the host. The add-on copies it to `/root/.ssh/id_rsa` internally; the name does not have to be `id_rsa`.
- Public key: Not used by the add-on directly, but you must add the corresponding `.pub` key as a Deploy Key (read-only) in your Git hosting service.
- Passphrase: Use an empty passphrase; interactive passphrases are not supported.
- Permissions: Ensure the private key is readable by Home Assistant; `chmod 600` is recommended.

Generate a new key (no passphrase) and place it in `/ssl`:

```bash
# Recommended: Ed25519
ssh-keygen -t ed25519 -C "homeassistant-mkdocs" -f /ssl/mkdocs_ssh_key -N ""

# Alternative: RSA 4096
ssh-keygen -t rsa -b 4096 -C "homeassistant-mkdocs" -f /ssl/mkdocs_ssh_key -N ""

# Show the public key to copy into your Git host (Deploy Key)
cat /ssl/mkdocs_ssh_key.pub
```

Use an SSH `git_url`, for example:

```yaml
git_url: "git@github.com:username/docs-repo.git"
ssh_key_path: "/ssl/mkdocs_ssh_key"
```

Known hosts: GitHub, GitLab, and Bitbucket host keys are pre-added automatically. If you use a different SSH host, you may need to extend the add-on to add it to `known_hosts`.

### Advanced Configuration

```yaml
source_type: "local"
local_path: "/config/mkdocs"
```

## Configuration Options

| Option         | Type   | Default                 | Description                                                                  |
| -------------- | ------ | ----------------------- | ---------------------------------------------------------------------------- |
| `source_type`  | string | `"local"`               | Source type: `"local"` or `"git"`                                            |
| `local_path`   | string | `"/config/mkdocs"`      | Path to local documentation folder                                           |
| `git_url`      | string | `""`                    | Git repository URL (required if source_type is "git")                        |
| `ssh_key_path` | string | `"/ssl/mkdocs_ssh_key"` | Path to SSH private key for Git access                                       |
| `enable_api`   | bool   | `true`                  | Enable HTTP API for automation integration                                   |
| `ports`        | map    | `8080/tcp: null`        | Map container port 8080 to a host port for direct access (set under Network) |

## Usage

### Using Local Files

1. Create a folder in your Home Assistant config directory (e.g., `/config/mkdocs`)
2. Add your markdown files to the `docs/` subfolder
3. Optionally add a custom `mkdocs.yml` configuration
4. Set `source_type` to `"local"` and `local_path` to your folder path
5. Start the add-on

### Using Git Repository

1. Create an SSH key pair for accessing your Git repository
2. Add the public key to your Git repository (GitHub/GitLab deploy keys)
3. Copy the private key to Home Assistant (e.g., `/ssl/mkdocs_ssh_key`)
4. Set `source_type` to `"git"` and configure `git_url` and `ssh_key_path`
5. Start the add-on

### Default Files

If no `mkdocs.yml` exists in your source, a default configuration will be created with:

- Material theme
- Mermaid2 plugin for diagrams
- Minify plugin for optimization
- Common markdown extensions
- Responsive design

## Supported Plugins

### Pre-installed Plugins

- mkdocs-material: Material Design theme
- mkdocs-mermaid2-plugin: Mermaid diagram support
- mkdocs-minify-plugin: HTML/CSS/JS minification
- mkdocs-awesome-pages-plugin: Enhanced navigation

### Adding Custom Plugins

Add plugins by updating `mkdocs.yml` and installing Python packages via `requirements.txt`.

Example `mkdocs.yml`:

```yaml
plugins:
  - search
  - mermaid2
  - minify
  - awesome-pages
  - macros
```

## Folder Structure

### Local Source Structure

```
/config/mkdocs/
├── mkdocs.yml          # MkDocs configuration (optional)
├── docs/               # Documentation files
│   ├── index.md        # Homepage
│   ├── about.md        # About page
│   └── assets/         # Images, CSS, JS
│       └── icon.png    # Site icon (optional)
└── requirements.txt    # Additional Python packages (optional)
```

### Git Repository Structure

```
your-repo/
├── mkdocs.yml          # MkDocs configuration (optional)
├── docs/               # Documentation files
│   ├── index.md        # Homepage
│   ├── about.md        # About page
│   └── assets/         # Images, CSS, JS
│       └── icon.png    # Site icon (optional)
└── requirements.txt    # Additional Python packages (optional)
```

## Accessing Your Documentation

Once the add-on is running, you can access your documentation:

1. **Via Home Assistant Ingress**: Click "Open Web UI" in the add-on panel
2. **Direct Access**: Visit `http://homeassistant:<host-port>` (the host port you mapped under Network)

## Automation Integration

The add-on provides a built-in HTTP API for triggering documentation rebuilds from Home Assistant automations, scripts, or external systems.

### API Endpoints

- **POST /rebuild**: Trigger a documentation rebuild
- **POST /webhook**: Same as /rebuild (for webhook use)
- **GET /status**: Check API status
- **GET /health**: Health check endpoint

### Home Assistant Integration

Add this to your `configuration.yaml` to enable REST commands:

```yaml
rest_command:
  mkdocs_rebuild:
    url: "http://localhost:8081/rebuild"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: '{}'
    timeout: 30

script:
  rebuild_mkdocs:
    alias: "Rebuild MkDocs Documentation"
    description: "Manually rebuild the MkDocs documentation"
    icon: mdi:book-refresh
    sequence:
      - service: rest_command.mkdocs_rebuild
      - service: notify.persistent_notification
        data:
          title: "MkDocs Rebuild"
          message: "Documentation rebuild started"
```

### Usage Examples

**From Home Assistant Script (via UI):**
1. Go to Settings → Automations & Scenes → Scripts
2. Create a new script with the `rest_command.mkdocs_rebuild` service call
3. Run the script manually or trigger it from automations

**From Automation:**
```yaml
automation:
  - alias: "Rebuild docs on file change"
    trigger:
      - platform: event
        event_type: folder_watcher
        event_data:
          path: "/config/mkdocs"
    action:
      - service: rest_command.mkdocs_rebuild
```

**Via HTTP (external systems):**
```bash
curl -X POST http://homeassistant:8081/rebuild
```

**From Node-RED:**
Use an HTTP request node with:
- Method: POST
- URL: `http://localhost:8081/rebuild`
- Payload: `{}`

Complete Node-RED flow examples are available in the `examples/` folder.

## Troubleshooting

### Common Issues

1. **Git Clone Failed**: Check SSH key permissions and repository access
2. **Build Failed**: Verify mkdocs.yml syntax and required files exist
3. **Plugin Installation Failed**: Check plugin name and availability on PyPI

### Logs

Check the add-on logs for detailed error messages and build output.

## Support

For issues and feature requests, please open an issue on the GitHub repository.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

```

```
