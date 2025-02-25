/**
 * DEP Framework - Интеграция Python-модели с TypeScript
 * 
 * Этот модуль предоставляет функции для взаимодействия с Python-моделью
 * Neuro-Solidity Auditor из TypeScript-кода.
 * 
 * @module ModelIntegration
 * @author DEP Framework Team
 * @version 0.1.0
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

// Промисифицированная версия exec
const execAsync = promisify(exec);

/**
 * Интерфейс для представления уязвимости
 */
export interface Vulnerability {
  name: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  confidence: number;
  lines: {
    line_number: number;
    line: string;
    context: string;
  }[];
}

/**
 * Интерфейс для представления результатов аудита
 */
export interface AuditResult {
  is_vulnerable: boolean;
  vulnerability_score: number;
  vulnerabilities: Vulnerability[];
  features: Record<string, any>;
  error?: string;
}

/**
 * Интерфейс для представления тест-кейса
 */
export interface TestCase {
  description: string;
  function: string;
  params: Record<string, any>;
  expected: string;
  edge_case: boolean;
  vulnerability?: string;
}

/**
 * Класс для интеграции с Python-моделью
 */
export class ModelIntegration {
  private pythonPath: string;
  private modelBridgePath: string;
  
  /**
   * Конструктор класса ModelIntegration
   * 
   * @param pythonPath Путь к интерпретатору Python
   * @param modelBridgePath Путь к скрипту model_bridge.py
   */
  constructor(
    pythonPath: string = 'python',
    modelBridgePath: string = path.join(__dirname, 'model_bridge.py')
  ) {
    this.pythonPath = pythonPath;
    this.modelBridgePath = modelBridgePath;
  }
  
  /**
   * Аудит смарт-контракта
   * 
   * @param contractPath Путь к файлу контракта
   * @returns Результаты аудита
   */
  public async auditContract(contractPath: string): Promise<AuditResult> {
    try {
      // Проверка существования файла
      if (!fs.existsSync(contractPath)) {
        throw new Error(`Файл не найден: ${contractPath}`);
      }
      
      // Вызов Python-скрипта
      const command = `${this.pythonPath} ${this.modelBridgePath} --action audit --contract-path "${contractPath}"`;
      const { stdout, stderr } = await execAsync(command);
      
      if (stderr) {
        console.error(`Ошибка при аудите контракта: ${stderr}`);
      }
      
      // Парсинг результата
      return JSON.parse(stdout) as AuditResult;
    } catch (error) {
      console.error(`Ошибка при аудите контракта: ${error}`);
      return {
        is_vulnerable: true,
        vulnerability_score: 1.0,
        vulnerabilities: [],
        features: {},
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }
  
  /**
   * Аудит исходного кода смарт-контракта
   * 
   * @param sourceCode Исходный код контракта
   * @returns Результаты аудита
   */
  public async auditContractCode(sourceCode: string): Promise<AuditResult> {
    try {
      // Создание временного файла
      const tempDir = path.join(__dirname, 'temp');
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
      }
      
      const tempFile = path.join(tempDir, `temp_${Date.now()}.sol`);
      fs.writeFileSync(tempFile, sourceCode, 'utf-8');
      
      try {
        // Аудит временного файла
        const result = await this.auditContract(tempFile);
        return result;
      } finally {
        // Удаление временного файла
        if (fs.existsSync(tempFile)) {
          fs.unlinkSync(tempFile);
        }
      }
    } catch (error) {
      console.error(`Ошибка при аудите исходного кода: ${error}`);
      return {
        is_vulnerable: true,
        vulnerability_score: 1.0,
        vulnerabilities: [],
        features: {},
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }
  
  /**
   * Генерация патча для исправления уязвимости
   * 
   * @param sourceCode Исходный код контракта
   * @param vulnerability Информация о уязвимости
   * @returns Патч для исправления уязвимости
   */
  public async generatePatch(sourceCode: string, vulnerability: Vulnerability): Promise<string> {
    try {
      // Создание временного файла для исходного кода
      const tempDir = path.join(__dirname, 'temp');
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
      }
      
      const tempFile = path.join(tempDir, `temp_${Date.now()}.sol`);
      fs.writeFileSync(tempFile, sourceCode, 'utf-8');
      
      // Создание временного файла для информации о уязвимости
      const vulnFile = path.join(tempDir, `vuln_${Date.now()}.json`);
      fs.writeFileSync(vulnFile, JSON.stringify(vulnerability), 'utf-8');
      
      try {
        // Вызов Python-скрипта
        const command = `${this.pythonPath} ${this.modelBridgePath} --action patch --contract-path "${tempFile}" --vulnerability "${vulnFile}"`;
        const { stdout, stderr } = await execAsync(command);
        
        if (stderr) {
          console.error(`Ошибка при генерации патча: ${stderr}`);
        }
        
        return stdout;
      } finally {
        // Удаление временных файлов
        if (fs.existsSync(tempFile)) {
          fs.unlinkSync(tempFile);
        }
        
        if (fs.existsSync(vulnFile)) {
          fs.unlinkSync(vulnFile);
        }
      }
    } catch (error) {
      console.error(`Ошибка при генерации патча: ${error}`);
      return `// Ошибка при генерации патча: ${error}`;
    }
  }
  
  /**
   * Генерация тест-кейсов для контракта
   * 
   * @param sourceCode Исходный код контракта
   * @returns Список тест-кейсов
   */
  public async generateTestCases(sourceCode: string): Promise<TestCase[]> {
    try {
      // Создание временного файла
      const tempDir = path.join(__dirname, 'temp');
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
      }
      
      const tempFile = path.join(tempDir, `temp_${Date.now()}.sol`);
      fs.writeFileSync(tempFile, sourceCode, 'utf-8');
      
      try {
        // Вызов Python-скрипта
        const command = `${this.pythonPath} ${this.modelBridgePath} --action test --contract-path "${tempFile}"`;
        const { stdout, stderr } = await execAsync(command);
        
        if (stderr) {
          console.error(`Ошибка при генерации тест-кейсов: ${stderr}`);
        }
        
        // Парсинг результата
        return JSON.parse(stdout) as TestCase[];
      } finally {
        // Удаление временного файла
        if (fs.existsSync(tempFile)) {
          fs.unlinkSync(tempFile);
        }
      }
    } catch (error) {
      console.error(`Ошибка при генерации тест-кейсов: ${error}`);
      return [];
    }
  }
}

/**
 * Пример использования:
 * 
 * ```typescript
 * import { ModelIntegration } from './model_integration';
 * 
 * async function main() {
 *   const modelIntegration = new ModelIntegration();
 *   
 *   // Аудит контракта
 *   const result = await modelIntegration.auditContract('path/to/contract.sol');
 *   console.log(result);
 *   
 *   // Генерация патча
 *   if (result.vulnerabilities.length > 0) {
 *     const patch = await modelIntegration.generatePatch(
 *       fs.readFileSync('path/to/contract.sol', 'utf-8'),
 *       result.vulnerabilities[0]
 *     );
 *     console.log(patch);
 *   }
 *   
 *   // Генерация тест-кейсов
 *   const testCases = await modelIntegration.generateTestCases(
 *     fs.readFileSync('path/to/contract.sol', 'utf-8')
 *   );
 *   console.log(testCases);
 * }
 * 
 * main().catch(console.error);
 * ```
 */

// Экспорт класса и интерфейсов
export default ModelIntegration;
