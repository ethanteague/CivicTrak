const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureScreenshots() {
  // Create screenshots directory
  const screenshotsDir = './screenshots';
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  // Launch browser
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    ignoreHTTPSErrors: true
  });
  
  const page = await context.newPage();

  // Define all pages to capture
  const pagesToCapture = [
    {
      name: 'homepage',
      url: 'http://govt.ddev.site/',
      description: 'Main homepage'
    },
    {
      name: 'case-studies',
      url: 'http://govt.ddev.site/government/case-studies',
      description: 'Success stories page'
    },
    {
      name: 'services',
      url: 'http://govt.ddev.site/government/service',
      description: 'Services listing'
    },
    {
      name: 'events',
      url: 'http://govt.ddev.site/government/event',
      description: 'Events listing'
    },
    {
      name: 'news',
      url: 'http://govt.ddev.site/government/news-and-announcements',
      description: 'News and announcements'
    },
    {
      name: 'staff',
      url: 'http://govt.ddev.site/government/person',
      description: 'Staff directory'
    },
    {
      name: 'meetings',
      url: 'http://govt.ddev.site/government/meeting-minute-agenda',
      description: 'Meeting minutes and agendas'
    },
    {
      name: 'ordinances',
      url: 'http://govt.ddev.site/government/ordinances',
      description: 'Ordinances page'
    },
    {
      name: 'search',
      url: 'http://govt.ddev.site/search',
      description: 'Search functionality'
    },
    {
      name: 'contact',
      url: 'http://govt.ddev.site/webform/contact',
      description: 'Contact form'
    }
  ];

  console.log(`Starting screenshot capture for ${pagesToCapture.length} pages...`);

  for (const pageInfo of pagesToCapture) {
    try {
      console.log(`Capturing: ${pageInfo.description} (${pageInfo.name})`);
      
      // Navigate to page
      await page.goto(pageInfo.url, { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });
      
      // Wait a bit for any animations/dynamic content
      await page.waitForTimeout(2000);
      
      // Take full page screenshot
      await page.screenshot({
        path: path.join(screenshotsDir, `${pageInfo.name}.png`),
        fullPage: true,
        type: 'png'
      });
      
      // Also take viewport screenshot for above-the-fold view
      await page.screenshot({
        path: path.join(screenshotsDir, `${pageInfo.name}-viewport.png`),
        type: 'png'
      });
      
      console.log(`✓ Captured ${pageInfo.name}`);
      
    } catch (error) {
      console.log(`✗ Error capturing ${pageInfo.name}: ${error.message}`);
      
      // Try to capture what we can even if there's an error
      try {
        await page.screenshot({
          path: path.join(screenshotsDir, `${pageInfo.name}-error.png`),
          type: 'png'
        });
      } catch (e) {
        console.log(`  Could not capture error screenshot: ${e.message}`);
      }
    }
  }

  // Capture mobile view of homepage
  try {
    console.log('Capturing mobile view of homepage...');
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('http://govt.ddev.site/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: path.join(screenshotsDir, 'homepage-mobile.png'),
      fullPage: true,
      type: 'png'
    });
    console.log('✓ Captured mobile homepage');
  } catch (error) {
    console.log(`✗ Error capturing mobile homepage: ${error.message}`);
  }

  await browser.close();
  
  console.log(`\nScreenshot capture complete!`);
  console.log(`Screenshots saved to: ${path.resolve(screenshotsDir)}`);
  
  // List captured files
  const files = fs.readdirSync(screenshotsDir);
  console.log(`\nCaptured files (${files.length}):`);
  files.forEach(file => console.log(`  - ${file}`));
}

// Run the screenshot capture
captureScreenshots().catch(console.error);