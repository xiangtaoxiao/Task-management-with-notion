import { ClawSkill, SkillContext } from 'openclaw-sdk';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

class NotionIntegrationSkill extends ClawSkill {
  async execute(context: SkillContext): Promise<any> {
    try {
      const { feature, parameters } = context;
      
      switch (feature) {
        case 'notion-init':
          return await this.handleNotionInit(parameters);
        case 'task-manager':
          return await this.handleTaskManager(parameters);
        case 'task-query':
          return await this.handleTaskQuery(parameters);
        default:
          throw new Error(`Unknown feature: ${feature}`);
      }
    } catch (error) {
      this.log.error(`Error executing Notion integration: ${(error as Error).message}`);
      return {
        success: false,
        message: `Error: ${(error as Error).message}`
      };
    }
  }

  private async handleNotionInit(parameters: any): Promise<any> {
    try {
      const { api_key } = parameters;
      
      if (!api_key) {
        throw new Error('API key is required');
      }

      // Execute Python script for Notion initialization
      const scriptPath = path.join(__dirname, 'scripts', 'notion_client.py');
      const result = execSync(`python3 ${scriptPath} init ${api_key}`, {
        encoding: 'utf8'
      });

      const output = JSON.parse(result);
      return {
        success: output.status === 'success',
        message: output.message,
        data: {
          database_id: output.database_id,
          database_name: output.database_name
        }
      };
    } catch (error) {
      throw new Error(`Notion initialization failed: ${(error as Error).message}`);
    }
  }

  private async handleTaskManager(parameters: any): Promise<any> {
    try {
      const { action, task_data } = parameters;
      
      if (!action || !task_data) {
        throw new Error('Action and task data are required');
      }

      // Execute Python script for task management
      const scriptPath = path.join(__dirname, 'scripts', 'notion_client.py');
      const taskDataStr = JSON.stringify(task_data);
      const result = execSync(`python3 ${scriptPath} task ${action} '${taskDataStr}'`, {
        encoding: 'utf8'
      });

      const output = JSON.parse(result);
      return {
        success: output.status === 'success',
        message: output.message,
        data: output.data
      };
    } catch (error) {
      throw new Error(`Task management failed: ${(error as Error).message}`);
    }
  }

  private async handleTaskQuery(parameters: any): Promise<any> {
    try {
      const { filter, sort } = parameters;

      // Execute Python script for task query
      const scriptPath = path.join(__dirname, 'scripts', 'notion_client.py');
      const filterStr = filter ? JSON.stringify(filter) : '{}';
      const sortStr = sort ? JSON.stringify(sort) : '{}';
      const result = execSync(`python3 ${scriptPath} query '${filterStr}' '${sortStr}'`, {
        encoding: 'utf8'
      });

      const output = JSON.parse(result);
      return {
        success: output.status === 'success',
        message: output.message,
        data: output.tasks
      };
    } catch (error) {
      throw new Error(`Task query failed: ${(error as Error).message}`);
    }
  }
}

// Export plugin instance
module.exports = new NotionIntegrationSkill();
