<?php

/**
 * @file
 * Platform.sh settings.
 */

use Drupal\redis\Cache\PhpRedis;
use Platformsh\ConfigReader\Config;

if (file_exists(__DIR__ . '/settings.platformsh.generated.php')) {
  include __DIR__ . '/settings.platformsh.generated.php';
}

if (getenv('PLATFORM_RELATIONSHIPS') && class_exists(Config::class)) {
  $plat_config = new Config();

  // Redis configuration.
  if (
    $plat_config->hasRelationship('redis') &&
    extension_loaded('redis') &&
    class_exists(PhpRedis::class)
  ) {
    $redis = $plat_config->credentials('redis')[0];

    $settings['redis.connection']['interface'] = 'PhpRedis';
    $settings['redis.connection']['host'] = $redis['host'];
    $settings['redis.connection']['port'] = $redis['port'];

    // Only override default cache if redis module is installed.
    $settings['cache']['default'] = 'cache.backend.redis';

    // Optional: improve performance of other bins.
    $settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['config'] = 'cache.backend.chainedfast';
  }

  // Database configuration.
  if ($plat_config->hasRelationship('database')) {
    $database = $plat_config->credentials('database')[0];

    $databases['default']['default'] = [
      'driver' => 'mysql',
      'database' => $database['path'],
      'username' => $database['username'],
      'password' => $database['password'],
      'host' => $database['host'],
      'port' => $database['port'],
      'pdo' => [PDO::MYSQL_ATTR_COMPRESS => TRUE],
    ];

    error_log('DB host: ' . $database['host']);
  }
}
