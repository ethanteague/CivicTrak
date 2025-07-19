<?php

/**
 * @file
 * Platform.sh settings.
 */

use Platformsh\ConfigReader\Config;

if (file_exists(__DIR__ . '/settings.platformsh.generated.php')) {
  include __DIR__ . '/settings.platformsh.generated.php';
}

if (getenv('PLATFORM_RELATIONSHIPS') && class_exists(Config::class)) {
  $plat_config = new Config();

  // Redis configuration.
  if ($plat_config->hasRelationship('redis') && extension_loaded('redis')) {
    $redis = $plat_config->credentials('redis')[0]; // ✅ FIXED

    $settings['redis.connection']['interface'] = 'PhpRedis';
    $settings['redis.connection']['host'] = $redis['host'];
    $settings['redis.connection']['port'] = $redis['port'];

    $settings['cache']['default'] = 'cache.backend.redis';
    $settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
    $settings['cache']['bins']['config'] = 'cache.backend.chainedfast';
  }

  // Database configuration.
  if ($plat_config->hasRelationship('database')) {
    $database = $plat_config->credentials('database')[0]; // ✅ FIXED

    $databases['default']['default'] = [
      'driver' => 'mysql',
      'database' => $database['path'],
      'username' => $database['username'],
      'password' => $database['password'],
      'host' => $database['host'],
      'port' => $database['port'],
      'pdo' => [PDO::MYSQL_ATTR_COMPRESS => TRUE],
    ];
  }
}
