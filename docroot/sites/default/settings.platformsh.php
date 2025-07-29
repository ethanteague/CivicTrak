<?php

use Platformsh\ConfigReader\Config;
use Drupal\redis\Cache\PhpRedis;

if (file_exists(__DIR__ . '/settings.platformsh.generated.php')) {
  include __DIR__ . '/settings.platformsh.generated.php';
}

if (isset($_SERVER['HTTP_HOST'])) {
  $settings['trusted_host_patterns'] = [
    '^' . preg_quote($_SERVER['HTTP_HOST']) . '$',
  ];
}

$relationships = getenv('PLATFORM_RELATIONSHIPS') ? json_decode(base64_decode(getenv('PLATFORM_RELATIONSHIPS')), TRUE) : [];

if (!empty($relationships)) {

  // Redis config.
  if (!empty($relationships['redis'][0]) && extension_loaded('redis') && class_exists(PhpRedis::class)) {
    $redis = $relationships['redis'][0];

    $settings['redis.connection']['interface'] = 'PhpRedis';
    $settings['redis.connection']['host'] = $redis['host'];
    $settings['redis.connection']['port'] = $redis['port'];

    // Delay setting the default cache backend until the module is available.
    if (is_dir(__DIR__ . '/../modules/contrib/redis')) {
      $settings['cache']['default'] = 'cache.backend.redis';

      // Optional bins.
      $settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
      $settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
      $settings['cache']['bins']['config'] = 'cache.backend.chainedfast';
    }
  }

  // DB config.
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
  }
}
