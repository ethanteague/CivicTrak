# Locations

This recipe creates a content type and related configuration (including views)
for managing and displaying location information. The intended use is to use a
geocoding service (such as Google Maps or Mapbox) so that content creators can
simply provide the address information, and then the latitude and longitude will
be determined automatically, and displayed on a map.

For a full description of the recipe, visit the
[project page](https://www.drupal.org/project/locations).

Submit bug reports and feature suggestions, or track changes in the
[issue queue](https://www.drupal.org/project/issues/locations).


## Table of contents (optional)

- Requirements
- Installation
- Configuration
- Maintainers


## Requirements (required)

This recipe makes use of the following modules:

- [Add Content by Bundle](https://www.drupal.org/project/add_content_by_bundle)
- [Address](https://www.drupal.org/project/address)
- [Geocoder](https://www.drupal.org/project/geocoder)
- [Geofield](https://www.drupal.org/project/geofield)
- [Leaflet](https://www.drupal.org/project/leaflet)
- [Metatag](https://www.drupal.org/project/metatag)
- [Pathauto](https://www.drupal.org/project/pathauto)


## Installation

- Install the Quick Links recipe as you would normally install a contributed
  Drupal recipe. See the Recipes [Getting Started Guide](https://git.drupalcode.org/project/distributions_recipes/-/blob/1.0.x/docs/getting_started.md) for further information. We strongly recommend using
  composer to ensure all dependencies will be handled automatically.



## Configuration

1. Enable the module at Administration > Extend.
1. If the locations being managed for your site are typically within a single
   country, you can make content creation easier by setting a default country in
   the form by going to `/admin/structure/types/manage/location/fields/node.location.field_location_address`
   and then enabling the "Set default value" checkbox, and providing whatever
   default values make sense for your website.
1. If you want to capture and display other information for locations, you can
   add additional fields to the content type at `/admin/structure/types/manage/location/fields`.


## Maintainers

- Martin Anderson-Clutz - [mandclu](https://www.drupal.org/u/mandclu)
