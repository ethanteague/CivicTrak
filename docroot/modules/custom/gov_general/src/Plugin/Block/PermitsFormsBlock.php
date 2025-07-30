<?php

namespace Drupal\gov_general\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Cache\Cache;

/**
 * Provides a 'Permits and Forms' Block.
 *
 * @Block(
 *   id = "permits_forms_block",
 *   admin_label = @Translation("Permits and Forms"),
 *   category = @Translation("Government"),
 * )
 */
class PermitsFormsBlock extends BlockBase {

  /**
   * {@inheritdoc}
   */
  public function build() {
    $forms = [
      [
        'title' => 'Building Permit Application',
        'description' => 'Apply for permits for new construction, additions, renovations, or repairs. Required for most construction work over $500.',
        'icon' => '🏗️',
        'url' => '/form/building-permit-application',
        'category' => 'Permits',
        'processing_time' => '3-5 business days',
        'fee' => '$50-$200',
        'requirements' => ['Building plans', 'Property survey', 'Contractor license'],
      ],
      [
        'title' => 'Business License Application',
        'description' => 'Apply for a business license to operate within city limits. Required for all commercial activities.',
        'icon' => '🏪',
        'url' => '/form/business-license-application',
        'category' => 'Permits',
        'processing_time' => '5-7 business days',
        'fee' => '$75-$150',
        'requirements' => ['Business registration', 'Insurance certificate', 'Tax permit'],
      ],
      [
        'title' => 'Citizen Service Request',
        'description' => 'Report issues or request city services. Track your request online and receive updates via email.',
        'icon' => '🛠️',
        'url' => '/form/service-request',
        'category' => 'Services',
        'processing_time' => '1-5 business days',
        'fee' => 'Free',
        'requirements' => ['Location details', 'Description of issue'],
      ],
      [
        'title' => 'Special Event Permit',
        'description' => 'Apply for permits for festivals, parades, street closures, and public gatherings.',
        'icon' => '🎪',
        'url' => '/form/special-event-permit',
        'category' => 'Permits',
        'processing_time' => '14-21 business days',
        'fee' => '$100-$500',
        'requirements' => ['Event plan', 'Insurance certificate', 'Safety plan'],
      ],
      [
        'title' => 'Residential Parking Permit',
        'description' => 'Apply for residential parking permits for restricted parking zones near downtown and universities.',
        'icon' => '🅿️',
        'url' => '/form/parking-permit',
        'category' => 'Permits',
        'processing_time' => '3-5 business days',
        'fee' => '$25/year',
        'requirements' => ['Proof of residency', 'Vehicle registration', 'Driver\'s license'],
      ],
      [
        'title' => 'Tree Removal Permit',
        'description' => 'Required for removing trees on public property or protected trees on private property.',
        'icon' => '🌳',
        'url' => '/form/tree-removal-permit',
        'category' => 'Permits',
        'processing_time' => '7-10 business days',
        'fee' => '$25-$100',
        'requirements' => ['Arborist report', 'Property survey', 'Replacement plan'],
      ],
      [
        'title' => 'Noise Variance Request',
        'description' => 'Request permission for activities that exceed normal noise limits (construction, events, etc.).',
        'icon' => '🔊',
        'url' => '/form/noise-variance',
        'category' => 'Permits',
        'processing_time' => '5-7 business days',
        'fee' => '$50',
        'requirements' => ['Activity details', 'Mitigation plan', 'Neighbor notification'],
      ],
      [
        'title' => 'Sidewalk Café Permit',
        'description' => 'Apply for permits to operate outdoor dining areas on public sidewalks.',
        'icon' => '☕',
        'url' => '/form/sidewalk-cafe-permit',
        'category' => 'Permits',
        'processing_time' => '10-14 business days',
        'fee' => '$200/year',
        'requirements' => ['Site plan', 'Insurance certificate', 'ADA compliance plan'],
      ],
      [
        'title' => 'Property Tax Appeal',
        'description' => 'Appeal your property tax assessment if you believe it\'s incorrect or unfair.',
        'icon' => '🏠',
        'url' => '/form/property-tax-appeal',
        'category' => 'Forms',
        'processing_time' => '30-45 business days',
        'fee' => '$100',
        'requirements' => ['Property appraisal', 'Tax assessment notice', 'Supporting documentation'],
      ],
      [
        'title' => 'FOIA Request',
        'description' => 'Request public records and documents under the Freedom of Information Act.',
        'icon' => '📄',
        'url' => '/form/foia-request',
        'category' => 'Forms',
        'processing_time' => '10-20 business days',
        'fee' => 'Varies by request',
        'requirements' => ['Specific record description', 'Contact information'],
      ],
      [
        'title' => 'Veteran\'s Benefits Application',
        'description' => 'Apply for local veteran benefits including property tax exemptions and discounts.',
        'icon' => '🎖️',
        'url' => '/form/veterans-benefits',
        'category' => 'Forms',
        'processing_time' => '15-20 business days',
        'fee' => 'Free',
        'requirements' => ['DD-214 form', 'Proof of residency', 'Property documents'],
      ],
      [
        'title' => 'Senior Citizen Services',
        'description' => 'Apply for senior citizen programs including transportation, meals, and activities.',
        'icon' => '👴',
        'url' => '/form/senior-services',
        'category' => 'Forms',
        'processing_time' => '5-10 business days',
        'fee' => 'Free',
        'requirements' => ['Age verification', 'Income documentation', 'Medical needs assessment'],
      ],
    ];

    return [
      '#theme' => 'permits_forms_block',
      '#forms' => $forms,
      '#cache' => [
        'contexts' => ['route'],
      ],
    ];
  }

  /**
   * {@inheritdoc}
   */
  public function getCacheTags() {
    return Cache::mergeTags(parent::getCacheTags(), ['webform_list']);
  }

}