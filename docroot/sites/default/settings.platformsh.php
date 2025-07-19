<?php

/**
 * @file
 * Platform.sh settings.
 */

use Drupal\redis\Cache\PhpRedis;

// Always include the generated settings first.
if (file_exists(__DIR__ . '/settings.platformsh.generated.php')) {
  include __DIR__ . '/settings.platformsh.generated.php';
}

// Safely decode PLATFORM_RELATIONSHIPS manually.
$relationships = getenv('PLATFORM_RELATIONSHIPS') ? json_decode(base64_decode(getenv('PLATFORM_RELATIONSHIPS')), TRUE) : [];

if (!empty($relationships)) {

  // Configure Redis if available.
  if (
    !empty($relationships['redis'][0]) &&
    extension_loaded('redis') &&
    class_exists(PhpRedis::class)
  ) {
    $redis = $relationships['redis'][0];

    $settings['redis.connection']['interface'] = 'PhpRedis';
    $settings['redis.connection']['host'] = $redis['host'];
    $settings['redis.connection']['port'] = $redis['port'];

    // Only override default cache if Redis module is present.
    $settings['cache']['default'] = 'cache.backend.redis';

    // Optional: speed up other bins.
    $settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['config'] = 'cache.backend.chainedfast';
  }

  // Configure database.
  if (!empty($relationships['database'][0])) {
    $db = $relationships['database'][0];

    $databases['default']['default'] = [
      'driver' => 'mysql',
      'database' => $db['path'],
      'username' => $db['username'],
      'password' => $db['password'],
      'host' => $db['host'],
      'port' => $db['port'],
      'pdo' => [PDO::MYSQL_ATTR_COMPRESS => TRUE],
    ];

    // Debug output for deploy logging.
    error_log('DB host: ' . $db['host']);
  }
}
