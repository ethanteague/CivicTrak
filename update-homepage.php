<?php

/**
 * Script to update homepage content with improved government messaging.
 */

use Drupal\node\Entity\Node;
use Drupal\Core\DrupalKernel;
use Symfony\Component\HttpFoundation\Request;

chdir('docroot');
require_once 'autoload.php';

$request = Request::createFromGlobals();
$kernel = DrupalKernel::createFromRequest($request);
$kernel->boot();

// Load the homepage node
$node = Node::load(172);

if ($node) {
  echo "Found homepage node: " . $node->getTitle() . "\n";
  
  // Update the body content with new hero section
  $new_content = '<div class="hero-section bg-primary text-white py-5 mb-4">
    <div class="container text-center">
      <h1 class="display-4 fw-bold mb-3">Complete Government Website Solution</h1>
      <p class="lead mb-4"><strong>$599/month • No Setup Fees • Ready in 5 Days</strong></p>
      <p class="h5 mb-4">Everything your municipality needs in one affordable package</p>
      <div class="d-flex justify-content-center gap-3 flex-wrap">
        <a href="/pricing" class="btn btn-light btn-lg px-4">View Pricing</a>
        <a href="/webform/contact" class="btn btn-outline-light btn-lg px-4">Start Your Trial</a>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="row">
      <div class="col-md-8 mx-auto text-center mb-5">
        <h2>Why Choose CivicTrak?</h2>
        <p class="lead">Traditional government website solutions cost $50K+ and take 6+ months. CivicTrak gets you online in 5 days for a fraction of the cost.</p>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-md-6">
        <div class="card border-danger h-100">
          <div class="card-body">
            <h4 class="card-title text-danger">❌ Traditional Vendors</h4>
            <ul class="list-unstyled">
              <li>• $25,000-$75,000 setup costs</li>
              <li>• 6-12 months to launch</li>
              <li>• Complex training required</li>
              <li>• Ongoing maintenance headaches</li>
              <li>• Limited support</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card border-success h-100">
          <div class="card-body">
            <h4 class="card-title text-success">✅ CivicTrak</h4>
            <ul class="list-unstyled">
              <li>• <strong>$0 setup fees</strong></li>
              <li>• <strong>5 days to launch</strong></li>
              <li>• <strong>2 hours training</strong></li>
              <li>• <strong>Everything managed for you</strong></li>
              <li>• <strong>24/7 support included</strong></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-12">
        <h2 class="text-center mb-4">What\'s Included in Your $599/month</h2>
        <div class="row">
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>🏛️ Professional Design</h5>
                <p>Government-focused website design that builds trust with citizens</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>📱 Citizen Portal</h5>
                <p>Online forms, service requests, and self-service options</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>📅 Event Management</h5>
                <p>Meeting calendars, agendas, and public notices</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>👥 Staff Directory</h5>
                <p>Department organization and contact information</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>📄 Document Center</h5>
                <p>Ordinances, permits, forms, and public records</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <h5>🔒 Security & Hosting</h5>
                <p>SSL certificates, backups, and 99.9% uptime guarantee</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-md-8 mx-auto">
        <div class="card bg-light">
          <div class="card-body text-center">
            <h3>5-Day Launch Process</h3>
            <div class="row">
              <div class="col-md-2 mb-2">
                <div class="fw-bold text-primary">Day 1</div>
                <small>Account setup</small>
              </div>
              <div class="col-md-2 mb-2">
                <div class="fw-bold text-primary">Day 2-3</div>
                <small>Site configuration</small>
              </div>
              <div class="col-md-2 mb-2">
                <div class="fw-bold text-primary">Day 4</div>
                <small>Staff training</small>
              </div>
              <div class="col-md-2 mb-2">
                <div class="fw-bold text-primary">Day 5</div>
                <small>Go live!</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-md-8 mx-auto text-center">
        <h2>Perfect for Small Governments</h2>
        <div class="row">
          <div class="col-md-3 mb-2">
            <div class="fw-bold">Cities</div>
            <small>Under 50K population</small>
          </div>
          <div class="col-md-3 mb-2">
            <div class="fw-bold">Townships</div>
            <small>Rural communities</small>
          </div>
          <div class="col-md-3 mb-2">
            <div class="fw-bold">Villages</div>
            <small>Small municipalities</small>
          </div>
          <div class="col-md-3 mb-2">
            <div class="fw-bold">Districts</div>
            <small>Special authorities</small>
          </div>
        </div>
      </div>
    </div>
  </div>';

  $node->set('body', [
    'value' => $new_content,
    'format' => 'full_html'
  ]);
  
  $node->save();
  echo "Homepage updated successfully!\n";
  echo "New content includes:\n";
  echo "- Hero section with $599/month pricing\n";
  echo "- Traditional vs CivicTrak comparison\n";
  echo "- What's included section\n";
  echo "- 5-day launch timeline\n";
  echo "- Target audience section\n";
} else {
  echo "Could not load homepage node 172\n";
}