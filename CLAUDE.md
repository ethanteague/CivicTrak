# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a **Drupal 11 government website** using composer-based project structure with relocated document root.

### Key Directories
- `docroot/` - Web root containing Drupal core, modules, themes
- `config/sync/` - Drupal configuration management files
- `docroot/themes/custom/gov/` - Custom government theme
- `docroot/modules/custom/gov_general/` - Custom government module
- `recipes/` - Drupal recipes for common configurations
- `scripts/` - Deployment and utility scripts

### Custom Code
- **Theme**: `docroot/themes/custom/gov/` - Contains SCSS, templates, and JS for government site styling
- **Module**: `docroot/modules/custom/gov_general/` - Custom functionality for government features
- **Recipe**: `recipes/locations/` - Drupal recipe for location-based content

## Development Commands

### Composer
```bash
# Install dependencies
composer install

# Update dependencies
composer update

# Add new module
composer require drupal/module_name
```

### Drush (Drupal CLI)
```bash
# Clear cache
drush cr

# Database updates
drush updb

# Import configuration
drush cim

# Export configuration
drush cex

# Install module
drush en module_name

# Uninstall module
drush pmu module_name
```

### Deployment

**Full Deployment (Database + Files + Code):**
```bash
# Complete deployment with database/files sync
./scripts/push-all.sh
```

**Code-Only Deployment (Normal):**
```bash
# Just push code - triggers Platform.sh pipeline
git push origin
```

**Deployment Process:**
- `push-all.sh`: Does `git push origin` + `drush sql-sync` + `drush rsync` to civictrak.main
- `git push origin`: Just triggers Platform.sh pipeline to deploy code changes
- Use `push-all.sh` only when database/content changes need to be deployed
- Use `git push origin` for normal code deployments (theme, config, modules)

## Content Types
- **Page** - Basic pages with layout builder
- **Event** - Events with dates, locations, and geofield
- **Job Listing** - Employment opportunities
- **News and Announcements** - News content with dates
- **Service** - Government services with contact info
- **Person** - Staff directory with departments
- **Meeting Minutes/Agenda** - Official meeting documents
- **Notices** - Public notices with documents
- **Ordinances** - Legal documents

## Key Modules
- **Layout Builder** - Page layout management
- **Webform** - Contact and application forms
- **Geofield/Geocoder** - Location mapping
- **Media** - File and image management
- **Paragraphs** - Flexible content components
- **Pathauto** - Automatic URL generation
- **Metatag** - SEO metadata

## Development Environment
- Uses DDEV for local development
- Platform.sh for hosting
- Drupal 11 with PHP 8.1+
- MySQL/MariaDB database

## User Preferences & Permissions

**Ethan has granted autonomous permission for Claude to perform the following operations WITHOUT asking for confirmation:**

### ✅ Always Allowed Operations
- **DDEV/Drush Commands**: Run any `ddev drush` commands (cache clear, config import/export, database updates, module enable/disable, user login generation, etc.)
- **Database Operations**: Execute SQL queries, database imports/exports, content updates via SQL
- **Gulp/SCSS Compilation**: Run `npx gulp`, `npm install`, compile SCSS, and other front-end build processes
- **Content Updates**: Modify Drupal content via Layout Builder, node updates, block content changes
- **Configuration Changes**: Import/export Drupal config, enable/disable modules, update settings
- **File Operations**: Create, edit, delete files in the codebase (SCSS, templates, PHP, etc.)
- **Cache Operations**: Clear Drupal cache, rebuild cache, flush caches
- **Development Scripts**: Run any scripts in the `scripts/` directory
- **Git Operations**: Add, commit, push changes (but always include proper commit messages)
- **Screenshot/Testing**: Install and run tools like Playwright for testing and screenshots
- **Search Operations**: Use grep, find, and other search tools across the codebase

### 🚫 Operations That Still Require Permission
- **Production Deployment**: Pushing to Platform.sh production environment
- **Module Installation**: Installing new Drupal modules via Composer
- **Database Schema Changes**: Major structural database changes
- **User Account Modifications**: Creating/deleting user accounts (except temporary admin logins)
- **Security-Related Changes**: Modifying .htaccess, security configurations
- **Backup/Restore Operations**: Major database or file restores

### 💡 Development Guidelines
- Always clear cache after configuration or content changes
- Use DDEV for all local operations (`ddev drush` instead of just `drush`)
- Compile SCSS after making style changes (`npx gulp styles`)
- Export configuration after making structural changes (`ddev drush cex`)
- Test changes with screenshots when appropriate
- Follow existing code patterns and conventions
- Update this CLAUDE.md file when adding new features or changing architecture

### 🎯 Theme Development
- **SCSS Location**: `docroot/themes/custom/gov/scss/`
- **Build Process**: Uses Gulp with `npx gulp` or `npx gulp styles`
- **Template Location**: `docroot/themes/custom/gov/templates/`
- **Bootstrap**: Theme uses Bootstrap 5 with custom SCSS variables

### 🗃️ Content Management
- **Layout Builder**: Homepage and other pages use Layout Builder for content arrangement
- **Block Types**: Custom blocks for features, alerts, and content sections
- **Views**: Custom views for departments, events, jobs listings
- **Forms**: Webform module handles contact and application forms

This permission structure allows Claude to work efficiently while maintaining appropriate safeguards for critical operations.

## 🚀 Token Optimization Guidelines

**IMPORTANT: These settings help minimize token usage and maximize efficiency:**

### Response Length Settings
- **Default Response Mode**: ULTRA-CONCISE (1-2 lines max unless detail requested)
- **Code Comments**: NEVER add comments unless explicitly asked
- **Explanations**: Skip pre/post explanations unless user asks
- **Tool Descriptions**: Use minimal descriptions in bash commands
- **Status Updates**: Only report completion, skip progress details

### Efficient Workflow Patterns
1. **Batch Operations**: Always use parallel tool calls when possible
2. **Smart File Reading**: Only read files when absolutely necessary
3. **Targeted Searches**: Use specific patterns instead of broad searches
4. **Cache Awareness**: Don't re-read recently accessed files
5. **Direct Actions**: Skip planning tools for simple tasks

### File Access Shortcuts
- **SCSS**: `docroot/themes/custom/gov/scss/`
- **Templates**: `docroot/themes/custom/gov/templates/`
- **Config**: `config/sync/`
- **Module**: `docroot/modules/custom/gov_general/`

### Common Task Shortcuts
```bash
# Essential commands (use these shortcuts)
ddev drush cr                    # Clear cache
ddev drush cex                   # Export config
ddev drush cim                   # Import config
npx gulp styles                  # Compile SCSS
ddev drush uli                   # Admin login
```

### Token-Saving Strategies
- Use `head_limit` parameter in Grep tool to limit results
- Use `limit` parameter in Read tool for large files
- Batch multiple file operations in single responses
- Use MultiEdit instead of multiple Edit calls
- Skip TodoWrite for simple single-step tasks
- Use direct file paths instead of search when location is known

### Automated Responses
For these common requests, respond with minimal tokens:
- **"clear cache"** → Run `ddev drush cr`, respond: "Cache cleared"
- **"compile scss"** → Run `npx gulp styles`, respond: "SCSS compiled"
- **"export config"** → Run `ddev drush cex`, respond: "Config exported"

### File Pattern Recognition
- **Theme files**: Always in `docroot/themes/custom/gov/`
- **SCSS imports**: Look in `scss/imports/` subdirectory
- **Twig templates**: Look in `templates/` subdirectory
- **Drupal config**: Always in `config/sync/`

**Claude: Follow these guidelines religiously to minimize token usage while maintaining effectiveness.**