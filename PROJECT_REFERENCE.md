# CivicTrak Drupal 11 Government Website - Project Reference

## Quick Reference Commands

```bash
# Essential Development Commands
ddev drush cr                    # Clear cache
ddev drush cex                   # Export config  
ddev drush cim                   # Import config
ddev drush uli                   # Admin login
npx gulp styles                  # Compile SCSS
npx gulp                         # Full build + watch
```

## File Locations (Token-Saving Shortcuts)

```bash
# Theme Files
THEME_ROOT="/docroot/themes/custom/gov"
SCSS_DIR="$THEME_ROOT/scss"
CSS_DIR="$THEME_ROOT/css"
TEMPLATES_DIR="$THEME_ROOT/templates"
JS_DIR="$THEME_ROOT/js"

# Custom Module
MODULE_ROOT="/docroot/modules/custom/gov_general"

# Configuration
CONFIG_DIR="/config/sync"

# Scripts & Tools
SCRIPTS_DIR="/scripts"
WEBFORMS_DIR="/webforms"
```

## Content Types Quick Reference

| Type | Machine Name | Key Fields | Layout Builder |
|------|--------------|------------|----------------|
| Page | `page` | body, layout_builder__layout | ✅ |
| Event | `event` | body, field_date, field_geofield, field_address | ❌ |
| Service | `service` | body, field_geofield, field_type_of_service | ❌ |
| Person | `person` | field_first_name, field_last_name, field_department | ✅ |
| Job Listing | `job_listing` | body, field_job_category | ❌ |
| News | `news_and_announcements` | body, field_date | ❌ |
| Notice | `notices` | body, field_notice_date, field_upload_document | ❌ |

## Development Patterns

### Theme Development Workflow
```bash
cd docroot/themes/custom/gov
npm install                      # If package.json updated
npx gulp styles                  # Quick SCSS compile
npx gulp                         # Full development server
```

### Configuration Management
```bash
ddev drush cex                   # After making config changes
git add config/sync/             # Stage configuration
git commit -m "Config: [description]"
ddev drush cim                   # Import on other environments
```

### Content Updates via Drush
```bash
ddev drush en module_name        # Enable module
ddev drush pmu module_name       # Uninstall module
ddev drush updb                  # Run database updates
ddev drush cr                    # Always clear cache after changes
```

## Key Module Dependencies

### Core Functionality
- `layout_builder` - Page layout management
- `media_library` - File/image management  
- `webform` - Government forms (12 preconfigured)
- `paragraphs` - Flexible content components

### Geographic Features
- `geofield` - Location mapping for events/services
- `geocoder` - Address to coordinates conversion
- `address` - Address field handling

### Development Tools
- `devel` - Development utilities
- `gin` - Modern admin theme
- `masquerade` - User switching for testing

## Custom Components

### Permits & Forms Block (`gov_general` module)
**Location**: `/docroot/modules/custom/gov_general/src/Plugin/Block/PermitsFormsBlock.php`
**Template**: `/docroot/modules/custom/gov_general/templates/permits-forms-block.html.twig`
**Purpose**: Displays 12 government forms with metadata (fees, processing times)

### Custom Theme Structure
```
docroot/themes/custom/gov/
├── scss/
│   ├── style.scss           # Main SCSS entry point
│   ├── variables.scss       # Bootstrap overrides
│   ├── general.scss         # General styling
│   └── typography.scss      # Font and text styling
├── css/                     # Compiled CSS output
├── js/                      # JavaScript files
├── templates/               # Twig template overrides
└── gulpfile.js             # Build configuration
```

## Database & Content Structure

### User Roles
- `anonymous` - Public users
- `authenticated` - Registered users  
- `content_editor` - Content management
- `site_manager` - Site administration
- `administrator` - Full access

### Taxonomies
- `department` - Government departments (with contact info)
- `service_type` - Service categorization
- `alert_severity` - Alert color coding

## Debugging & Troubleshooting

### Common Issues & Solutions
```bash
# Memory/performance issues
ddev drush cr                    # Clear all caches
ddev drush php-eval "drupal_flush_all_caches();"

# Module conflicts
ddev drush pmu problem_module    # Uninstall problematic module
ddev drush en -y module_name     # Reinstall module

# Configuration sync issues
ddev drush cim --partial         # Partial config import
ddev drush config-delete config.name  # Delete specific config

# Database issues
ddev drush updb                  # Run pending updates
ddev drush entity:updates        # Entity schema updates
```

### Development Environment Checks
```bash
# Check Drupal status
ddev drush status

# Check enabled modules
ddev drush pml --status=enabled

# Check configuration status
ddev drush config:status

# Performance monitoring
ddev drush watchdog:show
```

## Performance Optimization

### Caching Strategy
- **Redis**: External caching (configured)
- **Internal caches**: Page, block, render arrays
- **CSS/JS aggregation**: Enabled in production

### Image Optimization
- **Image styles**: thumbnail, medium, large, optimize
- **Responsive images**: Configured for content images
- **WebP support**: Available through image optimization

## Security & Compliance

### Security Measures
- **Honeypot**: Spam protection on forms
- **Secure email**: SMTP configuration
- **File security**: Upload restrictions configured
- **User permissions**: Role-based access control  

### Government Compliance
- **FOIA requests**: Dedicated content type and webform
- **Accessibility**: Semantic HTML, ARIA labels
- **Document management**: Official meeting minutes, ordinances
- **Public notices**: Structured notice publication system

## Automated Workflows

### Git Hooks (if configured)
```bash
# Pre-commit: Configuration export
ddev drush cex --yes

# Post-merge: Configuration import
ddev drush cim --yes
ddev drush cr
```

### Deployment Process
```bash
# Local to Platform.sh
./scripts/push-all.sh            # Custom deployment script
```

## Testing & Quality Assurance

### Manual Testing Checklist
- [ ] Homepage Layout Builder functionality
- [ ] Event creation with geocoding
- [ ] Service listings with maps
- [ ] Webform submissions
- [ ] Document uploads (notices, ordinances)
- [ ] Search functionality
- [ ] Mobile responsiveness
- [ ] Admin interface (Gin theme)

### Automated Testing Setup
```bash
# Install Playwright for browser testing
npm install playwright
npx playwright install
npx @playwright/mcp              # Run via MCP integration
```

## API Integrations

### External Services
- **Geocoding**: OpenStreetMap/Nominatim
- **Email**: SMTP server configuration
- **Search**: Internal Drupal search (can be enhanced with Solr)

### Internal APIs
- **REST API**: Drupal core REST module (if needed)
- **JSON:API**: Available for decoupled applications
- **GraphQL**: Can be added via contrib module

## Backup & Recovery

### Database Backups
```bash
ddev export-db --file=backup.sql.gz    # Create backup
ddev import-db --file=backup.sql.gz    # Restore backup
```

### Code & Configuration Backups
```bash
git tag v1.0.0                          # Tag releases
tar -czf site-backup.tar.gz docroot/sites/default/files/  # Files backup
```

## Environment Variables & Settings

### DDEV Configuration
- **Site URL**: `https://govt.ddev.site`
- **PHP Version**: 8.1+
- **Database**: MariaDB
- **Web Server**: Apache

### Platform.sh Configuration
- **Production URL**: [Configure in Platform.sh]
- **Environment variables**: Set in Platform.sh dashboard
- **Build process**: Automated via `.platform.app.yaml`

## Useful Drupal Console Commands

```bash
# Generate content for testing
ddev drush devel:generate-content 50

# User management
ddev drush user:create testuser --mail="test@example.com"
ddev drush user:password admin newpassword

# Module development
ddev drush generate:module
ddev drush generate:block
ddev drush generate:form
```

## Performance Monitoring

### Key Metrics to Monitor
- Page load times
- Database query performance  
- Cache hit rates
- Server resource usage
- Form submission rates
- Search query performance

### Monitoring Tools
- Drupal's internal statistics
- DDEV performance monitoring
- Platform.sh metrics (production)
- Google Analytics/Search Console

---

**Last Updated**: 2025-07-31  
**Project Version**: Drupal 11.x  
**Environment**: DDEV + Platform.sh  
**Theme**: Bootstrap 5 based government theme