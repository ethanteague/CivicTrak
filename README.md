# Government Website

A Drupal 11-based government website platform providing essential municipal services and information to citizens.

## Features

- **Content Management**: News, events, job listings, ordinances, meeting minutes
- **Staff Directory**: Departmental organization with contact information
- **Service Directory**: Government services with location mapping
- **Document Management**: Public notices, forms, and official documents
- **Event Calendar**: Community events with location integration
- **Contact Forms**: Webform-powered citizen communication

## Technology Stack

- **CMS**: Drupal 11
- **Theme**: Custom government theme with accessibility focus
- **Hosting**: Platform.sh
- **Local Development**: DDEV
- **Database**: MySQL/MariaDB

## Development Setup

### Prerequisites
- DDEV installed
- Composer
- Git

### Local Installation
```bash
# Clone repository
git clone [repository-url]
cd govt

# Start DDEV environment
ddev start

# Install dependencies
ddev composer install

# Import database
ddev import-db --file=dev.sql.gz

# Import configuration
ddev drush cim
```

### Common Commands
```bash
# Clear cache
ddev drush cr

# Export configuration
ddev drush cex

# Update database
ddev drush updb
```

## Deployment

Deployment to Platform.sh is handled via the custom script:
```bash
./scripts/push-all.sh
```

## Content Structure

### Content Types
- **Page**: Basic pages with Layout Builder
- **Event**: Events with dates and location mapping
- **Job Listing**: Employment opportunities
- **News & Announcements**: News content
- **Service**: Government services with contact info
- **Person**: Staff directory entries
- **Meeting Minutes/Agenda**: Official meeting documents
- **Notices**: Public notices with attachments
- **Ordinances**: Legal documents

### Key Modules
- Layout Builder - Flexible page layouts
- Webform - Contact and application forms
- Geofield/Geocoder - Location services
- Media Library - File management
- Pathauto - SEO-friendly URLs
- Metatag - SEO optimization

## Custom Development

### Theme
Location: `themes/custom/gov/`
- SCSS compilation with Gulp
- Government accessibility standards
- Mobile-responsive design

### Custom Module
Location: `modules/custom/gov_general/`
- Government-specific functionality
- Integration customizations

[Drupal.org]: https://www.drupal.org
[Drupal community]: https://www.drupal.org/community
[GitLab repository]: https://git.drupalcode.org/project/drupal
[issue queue]: https://www.drupal.org/project/issues/drupal
[issue forks]: https://www.drupal.org/drupalorg/docs/gitlab-integration/issue-forks-merge-requests
[documentation]: https://www.drupal.org/documentation
[changelog]: https://www.drupal.org/list-changes/drupal
[modules]: https://www.drupal.org/project/project_module
[security advisories]: https://www.drupal.org/security
[security RSS]: https://www.drupal.org/security/rss.xml
[security team]: https://www.drupal.org/drupal-security-team
[service providers]: https://www.drupal.org/drupal-services
[support]: https://www.drupal.org/support
[trademark]: https://www.drupal.com/trademark
