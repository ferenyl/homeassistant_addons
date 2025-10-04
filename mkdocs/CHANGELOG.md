# Changelog

## [1.2.0] - 2025-10-3

### Added
- **HTTP API for Automation Integration**: Built-in API server on port 8081
- **RESTful Commands**: Easy integration with Home Assistant automations and scripts
- **Webhook Support**: Direct webhook endpoint for Git repository integration
- **Home Assistant Examples**: Complete configuration examples for automations and scripts
- **Node-RED Integration**: Pre-built flow examples for Node-RED users
- **API Status Monitoring**: Health check and status endpoints
- **Background Rebuild Process**: Non-blocking documentation rebuilds

### Changed
- Improved logging with timestamp and structured output
- Enhanced error handling in rebuild process
- API can be disabled via configuration if not needed

## [1.1.7] - 2025-10-1

### Added
- Material theme now displays light or dark theme based on OS settings

## [1.1.6] - 2025-09-18

### Fixed

- Change icon

## [1.1.7] - 2025-09-19

### Fixed

- nginx did not start

## [1.0.0] - 2025-09-18

### Added

- Initial release of MkDocs Home Assistant Add-on
- Support for local folder and Git repository sources
- Pre-installed plugins: Material theme, Mermaid2, Minify
- SSH key support for private Git repositories
- Automatic default configuration and content generation
- Nginx web server with Home Assistant ingress support
- Configurable port settings
- Comprehensive documentation and examples

### Features

- **Multiple Source Types**: Local folders or Git repositories
- **Default Templates**: Automatic setup with sensible defaults
- **Plugin Ecosystem**: Pre-installed popular plugins with extensibility
- **Security**: SSH key support for private repositories
- **Performance**: Nginx serving with caching and compression
- **Integration**: Seamless Home Assistant ingress support
- **Customization**: Flexible configuration options
