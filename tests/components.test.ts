/**
 * DEP Framework - Тесты компонентов
 * 
 * Этот файл содержит тесты для основных компонентов DEP Framework:
 * 1. NeuroSolidityAuditor
 * 2. ProofOfHumanism
 * 3. EthicalMirrorEngine
 * 
 * @author DEP Framework Team
 */

import * as path from 'path';
import * as fs from 'fs';
import { NeuroSolidityAuditor } from '../src/neuro-solidity-auditor';
import { ProofOfHumanism } from '../src/proof-of-humanism';
import { EthicalMirrorEngine } from '../src/ethical-mirror-engine';
import { DEPFramework } from '../src';

// Путь к тестовому контракту
const TEST_CONTRACT_PATH = path.join(__dirname, '../examples/DrainContract.sol');

/**
 * Тесты для NeuroSolidityAuditor
 */
describe('NeuroSolidityAuditor', () => {
  let auditor: NeuroSolidityAuditor;
  
  beforeAll(async () => {
    auditor = new NeuroSolidityAuditor();
    await auditor.initialize();
  });
  
  test('должен успешно инициализироваться', () => {
    expect(auditor).toBeDefined();
  });
  
  test('должен находить уязвимости в контракте', async () => {
    const result = await auditor.auditContract(TEST_CONTRACT_PATH);
    
    expect(result).toBeDefined();
    expect(result.contractName).toBe('DrainContract.sol');
    expect(result.vulnerabilities.length).toBeGreaterThan(0);
    expect(result.score).toBeLessThan(100); // Контракт должен иметь уязвимости
  });
  
  test('должен генерировать тест-кейсы для контракта', async () => {
    const testCases = await auditor.generateTestCases(TEST_CONTRACT_PATH);
    
    expect(testCases).toBeDefined();
    expect(testCases.length).toBeGreaterThan(0);
  });
  
  test('должен генерировать патчи для уязвимостей', async () => {
    const result = await auditor.auditContract(TEST_CONTRACT_PATH);
    
    if (result.vulnerabilities.length > 0) {
      const patch = await auditor.generatePatch(result.vulnerabilities[0], TEST_CONTRACT_PATH);
      
      expect(patch).toBeDefined();
      expect(patch.length).toBeGreaterThan(0);
    }
  });
});

/**
 * Тесты для ProofOfHumanism
 */
describe('ProofOfHumanism', () => {
  let poh: ProofOfHumanism;
  
  beforeAll(async () => {
    poh = new ProofOfHumanism();
    await poh.initialize();
  });
  
  test('должен успешно инициализироваться', () => {
    expect(poh).toBeDefined();
  });
  
  test('должен возвращать текущий порог этичности', () => {
    const threshold = poh.getEthicalThreshold();
    
    expect(threshold).toBeDefined();
    expect(threshold.value).toBeGreaterThan(0);
    expect(threshold.value).toBeLessThanOrEqual(100);
  });
  
  test('должен обновлять порог этичности', () => {
    const newThreshold = {
      value: 80,
      lastUpdated: new Date(),
      proposedBy: 'Test',
      votes: []
    };
    
    poh.updateEthicalThreshold(newThreshold);
    const threshold = poh.getEthicalThreshold();
    
    expect(threshold.value).toBe(80);
  });
  
  test('должен предлагать новый порог этичности', async () => {
    const proposal = await poh.proposeNewThreshold('TestProposer', 85);
    
    expect(proposal).toBeDefined();
    expect(proposal.value).toBe(85);
    expect(proposal.proposedBy).toBe('TestProposer');
  });
});

/**
 * Тесты для EthicalMirrorEngine
 */
describe('EthicalMirrorEngine', () => {
  let mirror: EthicalMirrorEngine;
  let contractCode: string;
  
  beforeAll(async () => {
    mirror = new EthicalMirrorEngine();
    await mirror.initialize();
    
    // Чтение тестового контракта
    contractCode = fs.readFileSync(TEST_CONTRACT_PATH, 'utf-8');
  });
  
  test('должен успешно инициализироваться', () => {
    expect(mirror).toBeDefined();
  });
  
  test('должен анализировать этичность кода', () => {
    const analysis = mirror.analyzeEthics(contractCode);
    
    expect(analysis).toBeDefined();
    expect(analysis.ethicalScore).toBeLessThan(100); // Контракт должен иметь этические проблемы
    expect(analysis.issues.length).toBeGreaterThan(0);
  });
  
  test('должен создавать этический двойник кода', () => {
    const result = mirror.ethicalMirror(contractCode);
    
    expect(result).toBeDefined();
    expect(result.transformedCode).not.toBe(contractCode); // Код должен быть изменен
    expect(result.transformations.length).toBeGreaterThan(0);
  });
  
  test('должен добавлять новые паттерны трансформации', () => {
    mirror.addTransformationPattern('testPattern', 'testReplacement');
    
    const testCode = 'function testPattern() {}';
    const result = mirror.ethicalMirror(testCode);
    
    expect(result.transformedCode).toContain('testReplacement');
  });
  
  test('должен трансформировать пример из технического предложения', () => {
    const exampleCode = 'function drainWallet() { steal(funds); }';
    const result = mirror.ethicalMirror(exampleCode);
    
    expect(result.transformedCode).toContain('protect');
    expect(result.transformedCode).toContain('audit');
  });
});

/**
 * Тесты для DEPFramework
 */
describe('DEPFramework', () => {
  let framework: DEPFramework;
  
  beforeAll(async () => {
    framework = new DEPFramework();
    await framework.start();
  });
  
  test('должен успешно инициализироваться', () => {
    expect(framework).toBeDefined();
  });
  
  test('должен предоставлять доступ к NeuroSolidityAuditor', () => {
    const auditor = framework.getNeuroAuditor();
    
    expect(auditor).toBeDefined();
    expect(auditor).toBeInstanceOf(NeuroSolidityAuditor);
  });
  
  test('должен предоставлять доступ к ProofOfHumanism', () => {
    const poh = framework.getProofOfHumanism();
    
    expect(poh).toBeDefined();
    expect(poh).toBeInstanceOf(ProofOfHumanism);
  });
  
  test('должен предоставлять доступ к EthicalMirrorEngine', () => {
    const mirror = framework.getEthicalMirror();
    
    expect(mirror).toBeDefined();
    expect(mirror).toBeInstanceOf(EthicalMirrorEngine);
  });
});
