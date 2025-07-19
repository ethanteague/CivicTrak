<?php

/**
 * @file
 */

use Platformsh\ConfigReader\Config;

if (file_exists(__DIR__ . '/settings.platformsh.generated.php')) {
  include __DIR__ . '/settings.platformsh.generated.php';
}

if (getenv('PLATFORM_RELATIONSHIPS') && extension_loaded('redis')) {
  $config = new Config();
  $redis = $config->credentials('redis');
  $settings['redis.connection']['interface'] = 'PhpRedis';
  $settings['redis.connection']['host'] = $redis['host'];
  $settings['redis.connection']['port'] = $redis['port'];

  $settings['cache']['default'] = 'cache.backend.redis';
  $settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
  $settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
  $settings['cache']['bins']['config'] = 'cache.backend.chainedfast';
}


if (getenv('PLATFORM_RELATIONSHIPS') && class_exists(Config::class) && (new Config())->isValidPlatform()) {
  $config = new Config();

  if ($config->hasRelationship('database')) {
    $credentials = $config->credentials('database');

    $databases['default']['default'] = [
      'driver' => 'mysql',
      'database' => $credentials['path'],
      'username' => $credentials['username'],
      'password' => $credentials['password'],
      'host' => $credentials['host'],
      'port' => $credentials['port'],
      'pdo' => [PDO::MYSQL_ATTR_COMPRESS => TRUE],
    ];
  }
}
