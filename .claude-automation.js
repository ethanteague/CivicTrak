/**
 * Claude Code Automation Script for CivicTrak Drupal Project
 * 
 * This script provides intelligent agent selection and MCP integration
 * based on task context, file paths, and keywords.
 */

class CivicTrakAutomation {
  constructor() {
    this.config = null;
    this.loadConfig();
  }

  /**
   * Load subagent configuration
   */
  loadConfig() {
    try {
      const fs = require('fs');
      const configPath = './.claude-subagents.json';
      this.config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch (error) {
      console.error('Failed to load subagent configuration:', error.message);
      this.config = { subagents: {}, auto_selection_rules: {} };
    }
  }

  /**
   * Analyze task context and recommend appropriate agent/MCP combination
   * @param {string} task - Description of the task to perform
   * @param {string[]} filePaths - Array of file paths involved
   * @param {string} projectContext - Additional project context
   * @returns {Object} Recommendation object
   */
  analyzeTask(task, filePaths = [], projectContext = '') {
    const recommendation = {
      primaryAgent: null,
      secondaryAgents: [],
      mcpServers: [],
      automationLevel: 'manual',
      confidence: 0,
      reasoning: []
    };

    // Analyze task text for keywords
    const taskKeywords = this.extractKeywords(task.toLowerCase());
    
    // Analyze file paths
    const fileContext = this.analyzeFilePaths(filePaths);
    
    // Determine primary agent
    const agentScores = this.scoreAgents(taskKeywords, fileContext, projectContext);
    
    if (agentScores.length > 0) {
      recommendation.primaryAgent = agentScores[0].agent;
      recommendation.confidence = agentScores[0].score;
      recommendation.reasoning.push(`Selected ${agentScores[0].agent} (confidence: ${agentScores[0].score}%)`);
      
      // Add secondary agents if scores are close
      recommendation.secondaryAgents = agentScores
        .slice(1, 3)
        .filter(item => item.score > 60)
        .map(item => item.agent);
    }

    // Determine MCP integrations
    recommendation.mcpServers = this.recommendMCPs(taskKeywords, fileContext, recommendation.primaryAgent);
    
    // Determine automation level
    recommendation.automationLevel = this.determineAutomationLevel(taskKeywords, fileContext);

    return recommendation;
  }

  /**
   * Extract relevant keywords from task description
   */
  extractKeywords(text) {
    const keywords = [];
    const rules = this.config.auto_selection_rules?.keyword_triggers || {};
    
    // Check high priority keywords
    Object.keys(rules.high_priority || {}).forEach(keyword => {
      if (text.includes(keyword)) {
        keywords.push({ keyword, priority: 'high', agent: rules.high_priority[keyword] });
      }
    });
    
    // Check medium priority keywords
    Object.keys(rules.medium_priority || {}).forEach(keyword => {
      if (text.includes(keyword)) {
        keywords.push({ keyword, priority: 'medium', agent: rules.medium_priority[keyword] });
      }
    });

    return keywords;
  }

  /**
   * Analyze file paths to determine context
   */
  analyzeFilePaths(filePaths) {
    const context = {
      directories: new Set(),
      fileTypes: new Set(),
      suggestedAgents: new Set()
    };

    const pathRules = this.config.auto_selection_rules?.file_path_patterns || {};

    filePaths.forEach(path => {
      // Extract directory and file type
      const parts = path.split('/');
      context.directories.add(parts.slice(0, -1).join('/'));
      
      const extension = path.split('.').pop();
      if (extension) context.fileTypes.add(extension);

      // Check path patterns
      Object.keys(pathRules).forEach(pattern => {
        if (path.includes(pattern) || path.endsWith(pattern)) {
          context.suggestedAgents.add(pathRules[pattern]);
        }
      });
    });

    return context;
  }

  /**
   * Score agents based on task analysis
   */
  scoreAgents(keywords, fileContext, projectContext) {
    const scores = {};
    const agents = this.config.subagents || {};

    Object.keys(agents).forEach(agentKey => {
      const agent = agents[agentKey];
      let score = 0;

      // Score based on keywords
      keywords.forEach(keywordData => {
        if (agent.triggers?.some(trigger => 
          trigger.toLowerCase().includes(keywordData.keyword) ||
          keywordData.keyword.includes(trigger.toLowerCase())
        )) {
          score += keywordData.priority === 'high' ? 40 : 20;
        }
      });

      // Score based on file context
      if (fileContext.suggestedAgents.has(agentKey)) {
        score += 30;
      }

      // Score based on agent expertise matching
      const expertiseMatch = this.matchExpertise(agent.expertise || [], keywords, fileContext);
      score += expertiseMatch;

      if (score > 0) {
        scores[agentKey] = score;
      }
    });

    return Object.entries(scores)
      .map(([agent, score]) => ({ agent, score: Math.min(score, 100) }))
      .sort((a, b) => b.score - a.score);
  }

  /**
   * Match agent expertise with task requirements
   */
  matchExpertise(expertise, keywords, fileContext) {
    let score = 0;
    
    expertise.forEach(skill => {
      const skillLower = skill.toLowerCase();
      
      // Check if expertise matches keywords
      keywords.forEach(keywordData => {
        if (skillLower.includes(keywordData.keyword) || 
            keywordData.keyword.includes(skillLower)) {
          score += 10;
        }
      });

      // Check if expertise matches file types
      fileContext.fileTypes.forEach(fileType => {
        if (skillLower.includes(fileType) || fileType.includes(skillLower)) {
          score += 5;
        }
      });
    });

    return Math.min(score, 30);
  }

  /**
   * Recommend MCP servers based on context
   */
  recommendMCPs(keywords, fileContext, primaryAgent) {
    const mcps = [];
    const integrationSettings = this.config.integration_settings?.mcp_servers || {};

    // Check if testing-related
    if (keywords.some(k => ['test', 'testing', 'browser', 'accessibility'].includes(k.keyword))) {
      mcps.push('playwright');
    }

    // Check if documentation/context needed
    if (keywords.some(k => ['documentation', 'context', 'example'].includes(k.keyword))) {
      mcps.push('context7');
    }

    // Check agent preferences
    Object.entries(integrationSettings).forEach(([mcpName, settings]) => {
      if (settings.preferred_agents?.includes(primaryAgent) && settings.auto_enable) {
        if (!mcps.includes(mcpName)) {
          mcps.push(mcpName);
        }
      }
    });

    return mcps;
  }

  /**
   * Determine appropriate automation level
   */
  determineAutomationLevel(keywords, fileContext) {
    // High automation for safe operations
    const safeOperations = ['cache clear', 'scss compile', 'config export'];
    if (keywords.some(k => safeOperations.some(op => k.keyword.includes(op)))) {
      return 'full';
    }

    // Medium automation for development tasks
    if (fileContext.directories.has('docroot/themes/custom/gov') ||
        fileContext.directories.has('docroot/modules/custom/gov_general')) {
      return 'guided';
    }

    // Manual for configuration changes
    if (fileContext.directories.has('config/sync') ||
        keywords.some(k => ['deployment', 'security', 'production'].includes(k.keyword))) {
      return 'manual';
    }

    return 'guided';
  }

  /**
   * Generate automation command suggestions
   */
  generateCommands(task, recommendation) {
    const commands = {
      preparation: [],
      execution: [],
      validation: [],
      cleanup: []
    };

    // Add preparation commands based on agent
    switch (recommendation.primaryAgent) {
      case 'frontend-developer':
        commands.preparation.push('cd docroot/themes/custom/gov');
        if (task.includes('scss') || task.includes('style')) {
          commands.execution.push('npx gulp styles');
          commands.validation.push('Check CSS output in css/ directory');
        }
        break;

      case 'content-manager':
        commands.preparation.push('ddev drush cr');
        if (task.includes('config')) {
          commands.execution.push('ddev drush cex');
          commands.validation.push('git diff config/sync/');
        }
        break;

      case 'drupal-developer':
        commands.preparation.push('ddev drush cr');
        commands.validation.push('ddev drush status');
        commands.cleanup.push('ddev drush cr');
        break;

      case 'testing-qa':
        if (recommendation.mcpServers.includes('playwright')) {
          commands.execution.push('npx @playwright/mcp');
        }
        commands.validation.push('Review test results');
        break;
    }

    return commands;
  }

  /**
   * Main automation interface
   */
  automate(task, filePaths = [], options = {}) {
    console.log('🤖 CivicTrak Automation Analysis');
    console.log('================================');
    
    const recommendation = this.analyzeTask(task, filePaths, options.context || '');
    const commands = this.generateCommands(task, recommendation);

    console.log('📋 Task:', task);
    console.log('📁 Files:', filePaths.length > 0 ? filePaths.join(', ') : 'None specified');
    console.log('');
    console.log('🎯 Recommendation:');
    console.log('  Primary Agent:', recommendation.primaryAgent || 'General Purpose');
    console.log('  Confidence:', recommendation.confidence + '%');
    console.log('  MCP Servers:', recommendation.mcpServers.join(', ') || 'None');
    console.log('  Automation Level:', recommendation.automationLevel);
    
    if (recommendation.secondaryAgents.length > 0) {
      console.log('  Secondary Agents:', recommendation.secondaryAgents.join(', '));
    }

    console.log('');
    console.log('💡 Reasoning:');
    recommendation.reasoning.forEach(reason => console.log('  -', reason));

    if (Object.values(commands).some(arr => arr.length > 0)) {
      console.log('');
      console.log('⚡ Suggested Commands:');
      Object.entries(commands).forEach(([phase, cmds]) => {
        if (cmds.length > 0) {
          console.log(`  ${phase.charAt(0).toUpperCase() + phase.slice(1)}:`);
          cmds.forEach(cmd => console.log(`    ${cmd}`));
        }
      });
    }

    return {
      recommendation,
      commands,
      shouldProceed: recommendation.confidence > 70
    };
  }
}

// Export for Node.js usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CivicTrakAutomation;
}

// Browser/CLI usage
if (typeof window !== 'undefined') {
  window.CivicTrakAutomation = CivicTrakAutomation;
}

// CLI interface
if (require.main === module) {
  const automation = new CivicTrakAutomation();
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: node .claude-automation.js "task description" [file1] [file2] ...');
    console.log('Example: node .claude-automation.js "compile SCSS for homepage" docroot/themes/custom/gov/scss/style.scss');
    process.exit(1);
  }

  const task = args[0];
  const files = args.slice(1);
  
  automation.automate(task, files);
}