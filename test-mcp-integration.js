#!/usr/bin/env node
/**
 * MCP Integration Test Suite for CivicTrak Drupal Project
 * 
 * Tests all MCP servers, subagent configurations, and automation workflows
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class MCPIntegrationTester {
  constructor() {
    this.results = {
      mcp_servers: {},
      configurations: {},
      automations: {},
      overall: 'pending'
    };
  }

  log(message, type = 'info') {
    const colors = {
      info: '\x1b[36m',
      success: '\x1b[32m',
      error: '\x1b[31m',
      warning: '\x1b[33m',
      reset: '\x1b[0m'
    };
    
    console.log(`${colors[type]}${message}${colors.reset}`);
  }

  async runTest(name, testFunction) {
    this.log(`\n🧪 Testing: ${name}`, 'info');
    try {
      const result = await testFunction();
      this.log(`✅ ${name}: PASSED`, 'success');
      return { status: 'passed', result };
    } catch (error) {
      this.log(`❌ ${name}: FAILED - ${error.message}`, 'error');
      return { status: 'failed', error: error.message };
    }
  }

  testPlaywrightMCP() {
    return new Promise((resolve, reject) => {
      try {
        const output = execSync('npx @playwright/mcp --version', { encoding: 'utf8' });
        resolve(output.trim());
      } catch (error) {
        reject(new Error(`Playwright MCP not accessible: ${error.message}`));
      }
    });
  }

  testContext7MCP() {
    return new Promise((resolve, reject) => {
      try {
        const output = execSync('npx -y @upstash/context7-mcp@latest --help', { 
          encoding: 'utf8',
          timeout: 10000 
        });
        resolve('Context7 MCP accessible');
      } catch (error) {
        reject(new Error(`Context7 MCP not accessible: ${error.message}`));
      }
    });
  }

  testVSCodeConfiguration() {
    return new Promise((resolve, reject) => {
      const settingsPath = '.vscode/settings.json';
      
      if (!fs.existsSync(settingsPath)) {
        reject(new Error('VS Code settings.json not found'));
        return;
      }

      try {
        const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
        
        // Check for MCP configurations
        const hasMCP = settings.mcp && settings.mcp.mcpServers;
        const hasClaudeMCP = settings['claude.mcpServers'];
        const hasDrupalConfig = settings.drupal;
        
        if (!hasMCP && !hasClaudeMCP) {
          reject(new Error('No MCP server configurations found in VS Code settings'));
          return;
        }

        const mcpServers = Object.keys(settings.mcp?.mcpServers || {});
        const claudeServers = Object.keys(settings['claude.mcpServers'] || {});
        
        resolve({
          mcp_servers: mcpServers,
          claude_servers: claudeServers,
          drupal_config: !!hasDrupalConfig,
          php_config: !!settings['php.validate.executablePath']
        });
      } catch (error) {
        reject(new Error(`Invalid VS Code configuration: ${error.message}`));
      }
    });
  }

  testMCPConfigFile() {
    return new Promise((resolve, reject) => {
      const configPath = '.mcp-config.json';
      
      if (!fs.existsSync(configPath)) {
        reject(new Error('MCP configuration file not found'));
        return;
      }

      try {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        
        if (!config.mcpServers) {
          reject(new Error('Invalid MCP configuration structure'));
          return;
        }

        const servers = Object.keys(config.mcpServers);
        resolve({
          servers,
          playwright_configured: servers.includes('playwright'),
          context7_configured: servers.includes('context7')
        });
      } catch (error) {
        reject(new Error(`Invalid MCP configuration: ${error.message}`));
      }
    });
  }

  testSubagentConfiguration() {
    return new Promise((resolve, reject) => {
      const configPath = '.claude-subagents.json';
      
      if (!fs.existsSync(configPath)) {
        reject(new Error('Subagent configuration file not found'));
        return;
      }

      try {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        
        const requiredSections = ['subagents', 'auto_selection_rules', 'integration_settings'];
        const missingSections = requiredSections.filter(section => !config[section]);
        
        if (missingSections.length > 0) {
          reject(new Error(`Missing configuration sections: ${missingSections.join(', ')}`));
          return;
        }

        const agents = Object.keys(config.subagents);
        const expectedAgents = [
          'drupal-developer',
          'content-manager', 
          'frontend-developer',
          'devops-automation',
          'testing-qa',
          'data-migration'
        ];

        const missingAgents = expectedAgents.filter(agent => !agents.includes(agent));
        
        resolve({
          total_agents: agents.length,
          configured_agents: agents,
          missing_agents: missingAgents,
          has_auto_selection: !!config.auto_selection_rules,
          has_integrations: !!config.integration_settings
        });
      } catch (error) {
        reject(new Error(`Invalid subagent configuration: ${error.message}`));
      }
    });
  }

  testAutomationScript() {
    return new Promise((resolve, reject) => {
      const scriptPath = '.claude-automation.js';
      
      if (!fs.existsSync(scriptPath)) {
        reject(new Error('Automation script not found'));
        return;
      }

      try {
        // Test the automation script with a sample task
        const output = execSync(
          'node .claude-automation.js "test task for validation" test.php',
          { encoding: 'utf8', timeout: 5000 }
        );
        
        // Check if output contains expected sections
        const hasRecommendation = output.includes('🎯 Recommendation:');
        const hasReasoning = output.includes('💡 Reasoning:');
        const hasAgent = output.includes('Primary Agent:');
        
        if (!hasRecommendation || !hasReasoning || !hasAgent) {
          reject(new Error('Automation script output missing required sections'));
          return;
        }

        resolve({
          script_executable: true,
          output_format_valid: true,
          sample_output: output.split('\n').slice(0, 10).join('\n') + '...'
        });
      } catch (error) {
        reject(new Error(`Automation script execution failed: ${error.message}`));
      }
    });
  }

  testProjectReference() {
    return new Promise((resolve, reject) => {
      const refPath = 'PROJECT_REFERENCE.md';
      
      if (!fs.existsSync(refPath)) {
        reject(new Error('Project reference file not found'));
        return;
      }

      const content = fs.readFileSync(refPath, 'utf8');
      
      // Check for key sections
      const requiredSections = [
        'Quick Reference Commands',
        'File Locations',
        'Content Types Quick Reference',
        'Development Patterns',
        'Custom Components'
      ];

      const missingSections = requiredSections.filter(section => 
        !content.includes(section)
      );

      if (missingSections.length > 0) {
        reject(new Error(`Missing reference sections: ${missingSections.join(', ')}`));
        return;
      }

      resolve({
        file_size: content.length,
        sections_present: requiredSections.length - missingSections.length,
        has_commands: content.includes('ddev drush'),
        has_file_paths: content.includes('docroot/themes/custom/gov')
      });
    });
  }

  testDrupalEnvironment() {
    return new Promise((resolve, reject) => {
      try {
        // Test DDEV availability
        const ddevStatus = execSync('ddev --version', { encoding: 'utf8' });
        
        // Test if project is running
        let projectStatus = 'stopped';
        try {
          execSync('ddev status', { encoding: 'utf8' });
          projectStatus = 'running';
        } catch (e) {
          // Project might be stopped, which is okay
        }

        // Test Drush availability through DDEV
        let drushAvailable = false;
        try {
          execSync('ddev drush --version', { encoding: 'utf8', timeout: 10000 });
          drushAvailable = true;
        } catch (e) {
          // Drush might not be available if project is stopped
        }

        resolve({
          ddev_version: ddevStatus.trim(),
          project_status: projectStatus,
          drush_available: drushAvailable
        });
      } catch (error) {
        reject(new Error(`Drupal environment not properly configured: ${error.message}`));
      }
    });
  }

  async runAllTests() {
    this.log('🚀 Starting MCP Integration Test Suite for CivicTrak', 'info');
    this.log('=' .repeat(60), 'info');

    // Test MCP Servers
    this.results.mcp_servers.playwright = await this.runTest(
      'Playwright MCP Server',
      () => this.testPlaywrightMCP()
    );

    this.results.mcp_servers.context7 = await this.runTest(
      'Context7 MCP Server', 
      () => this.testContext7MCP()
    );

    // Test Configurations
    this.results.configurations.vscode = await this.runTest(
      'VS Code MCP Configuration',
      () => this.testVSCodeConfiguration()
    );

    this.results.configurations.mcp_config = await this.runTest(
      'MCP Configuration File',
      () => this.testMCPConfigFile()
    );

    this.results.configurations.subagents = await this.runTest(
      'Subagent Configuration',
      () => this.testSubagentConfiguration()
    );

    // Test Automation
    this.results.automations.script = await this.runTest(
      'Automation Script',
      () => this.testAutomationScript()
    );

    this.results.automations.reference = await this.runTest(
      'Project Reference File',
      () => this.testProjectReference()
    );

    // Test Environment
    this.results.automations.drupal_env = await this.runTest(
      'Drupal Development Environment',
      () => this.testDrupalEnvironment()
    );

    // Generate Summary
    this.generateSummary();
  }

  generateSummary() {
    this.log('\n📊 Test Results Summary', 'info');
    this.log('=' .repeat(60), 'info');

    let totalTests = 0;
    let passedTests = 0;

    // Count results
    const countResults = (section) => {
      Object.values(section).forEach(result => {
        totalTests++;
        if (result.status === 'passed') passedTests++;
      });
    };

    countResults(this.results.mcp_servers);
    countResults(this.results.configurations);
    countResults(this.results.automations);

    const successRate = Math.round((passedTests / totalTests) * 100);

    this.log(`\n📈 Overall Results:`, 'info');
    this.log(`   Tests Run: ${totalTests}`, 'info');
    this.log(`   Passed: ${passedTests}`, passedTests === totalTests ? 'success' : 'warning');
    this.log(`   Failed: ${totalTests - passedTests}`, totalTests - passedTests === 0 ? 'success' : 'error');
    this.log(`   Success Rate: ${successRate}%`, successRate >= 80 ? 'success' : 'warning');

    // Detailed breakdown
    this.log(`\n📋 Detailed Results:`, 'info');
    
    this.log(`   MCP Servers:`, 'info');
    Object.entries(this.results.mcp_servers).forEach(([name, result]) => {
      const status = result.status === 'passed' ? '✅' : '❌';
      this.log(`     ${status} ${name}`, result.status === 'passed' ? 'success' : 'error');
    });

    this.log(`   Configurations:`, 'info');
    Object.entries(this.results.configurations).forEach(([name, result]) => {
      const status = result.status === 'passed' ? '✅' : '❌';
      this.log(`     ${status} ${name}`, result.status === 'passed' ? 'success' : 'error');
    });

    this.log(`   Automation:`, 'info');
    Object.entries(this.results.automations).forEach(([name, result]) => {
      const status = result.status === 'passed' ? '✅' : '❌';
      this.log(`     ${status} ${name}`, result.status === 'passed' ? 'success' : 'error');
    });

    // Recommendations
    this.log(`\n💡 Recommendations:`, 'info');
    
    if (successRate >= 90) {
      this.log('   🎉 Excellent! Your MCP integration is fully operational.', 'success');
      this.log('   🚀 You can now use automated workflows and specialized agents.', 'success');
    } else if (successRate >= 70) {
      this.log('   ⚠️  Good setup, but some components need attention.', 'warning');
      this.log('   🔧 Check the failed tests above and resolve issues.', 'warning');
    } else {
      this.log('   🚨 Several components are not working properly.', 'error');
      this.log('   🔧 Please review and fix the configuration issues.', 'error');
    }

    this.log(`\n📚 Next Steps:`, 'info');
    this.log('   1. Use "node .claude-automation.js" for task automation', 'info');
    this.log('   2. Reference PROJECT_REFERENCE.md for quick lookups', 'info');
    this.log('   3. Leverage specialized agents for different task types', 'info');
    this.log('   4. Use MCP servers (Playwright, Context7) when appropriate', 'info');

    this.results.overall = successRate >= 80 ? 'success' : 'needs_attention';
    
    return this.results;
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new MCPIntegrationTester();
  tester.runAllTests().catch(error => {
    console.error('Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = MCPIntegrationTester;