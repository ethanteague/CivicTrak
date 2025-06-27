<?php

namespace Drupal\govt_migrations;

/**
 * Migration utility helper.
 */
class MigrateHelper {

  /**
   * Decode JSON into associative array.
   *
   * @param string $json
   *   The JSON string.
   *
   * @return array
   *   The decoded array.
   */
  public static function jsonDecodeToArray(string $json): array {
    return json_decode($json, TRUE) ?? [];
  }

}
