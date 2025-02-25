/**
 * DEP Framework - Демонстрационный пример использования
 * 
 * Этот пример показывает, как использовать DEP Framework для:
 * 1. Аудита смарт-контракта с помощью NeuroSolidityAuditor
 * 2. Валидации транзакций с помощью ProofOfHumanism
 * 3. Создания этического двойника кода с помощью EthicalMirrorEngine
 * 
 * @author DEP Framework Team
 */

import * as path from 'path';
import * as fs from 'fs';
import * as web3 from '@solana/web3.js';
import { DEPFramework, NeuroSolidityAuditor, ProofOfHumanism, EthicalMirrorEngine } from '../src';

// Путь к примеру контракта
const CONTRACT_PATH = path.join(__dirname, 'DrainContract.sol');

/**
 * Основная функция демонстрации
 */
async function runDemo() {
  console.log('=== DEP Framework Demo ===');
  console.log('Инициализация DEP Framework...');
  
  // Инициализация фреймворка
  const framework = new DEPFramework();
  await framework.start();
  
  // Получение компонентов
  const neuroAuditor = framework.getNeuroAuditor();
  const proofOfHumanism = framework.getProofOfHumanism();
  const ethicalMirror = framework.getEthicalMirror();
  
  // Демонстрация NeuroSolidityAuditor
  await demoNeuroAuditor(neuroAuditor);
  
  // Демонстрация ProofOfHumanism
  await demoProofOfHumanism(proofOfHumanism);
  
  // Демонстрация EthicalMirrorEngine
  await demoEthicalMirror(ethicalMirror);
  
  console.log('\n=== Демонстрация завершена ===');
}

/**
 * Демонстрация NeuroSolidityAuditor
 */
async function demoNeuroAuditor(auditor: NeuroSolidityAuditor) {
  console.log('\n=== Демонстрация NeuroSolidityAuditor ===');
  
  // Чтение контракта
  console.log(`Аудит контракта: ${CONTRACT_PATH}`);
  
  // Аудит контракта
  const auditResult = await auditor.auditContract(CONTRACT_PATH);
  
  // Вывод результатов аудита
  console.log(`\nРезультаты аудита для ${auditResult.contractName}:`);
  console.log(`Общий скор безопасности: ${auditResult.score}/100`);
  console.log(`Найдено уязвимостей: ${auditResult.vulnerabilities.length}`);
  
  // Вывод найденных уязвимостей
  if (auditResult.vulnerabilities.length > 0) {
    console.log('\nСписок уязвимостей:');
    
    for (const vuln of auditResult.vulnerabilities) {
      console.log(`\n[${vuln.severity.toUpperCase()}] ${vuln.name}`);
      console.log(`Строки: ${vuln.lineStart}-${vuln.lineEnd}`);
      console.log(`Описание: ${vuln.description}`);
      console.log(`Рекомендация: ${vuln.recommendation}`);
      console.log('Фрагмент кода:');
      console.log(vuln.codeSnippet);
    }
  }
  
  // Генерация тест-кейсов
  console.log('\nГенерация тест-кейсов для контракта...');
  const testCases = await auditor.generateTestCases(CONTRACT_PATH, true);
  
  console.log(`Сгенерировано ${testCases.length} тест-кейсов:`);
  for (const test of testCases) {
    console.log(`- ${test.description}`);
  }
}

/**
 * Демонстрация ProofOfHumanism
 */
async function demoProofOfHumanism(poh: ProofOfHumanism) {
  console.log('\n=== Демонстрация ProofOfHumanism ===');
  
  // Получение текущего порога этичности
  const threshold = poh.getEthicalThreshold();
  console.log(`Текущий порог этичности: ${threshold.value}`);
  console.log(`Последнее обновление: ${threshold.lastUpdated}`);
  console.log(`Предложено: ${threshold.proposedBy}`);
  
  // Создание примера транзакции
  console.log('\nСоздание примеров транзакций...');
  
  // Этичная транзакция (пожертвование)
  const ethicalTx = new web3.Transaction().add(
    web3.SystemProgram.transfer({
      fromPubkey: new web3.PublicKey('CharityWallet123'),
      toPubkey: new web3.PublicKey('DonationAddress456'),
      lamports: 1000000000,
    })
  );
  
  // Неэтичная транзакция (drain)
  const unethicalTx = new web3.Transaction().add(
    web3.SystemProgram.transfer({
      fromPubkey: new web3.PublicKey('HackerWallet789'),
      toPubkey: new web3.PublicKey('DrainAddress000'),
      lamports: 9999999999,
    })
  );
  
  // Валидация транзакций
  console.log('\nВалидация этичной транзакции:');
  const ethicalResult = poh.validateTransaction(ethicalTx);
  console.log(`Этический скор: ${ethicalResult.ethicalScore}/100`);
  console.log(`Результат валидации: ${ethicalResult.validationResult ? 'ПРИНЯТА' : 'ОТКЛОНЕНА'}`);
  console.log(`Причина: ${ethicalResult.validationReason}`);
  
  console.log('\nВалидация неэтичной транзакции:');
  const unethicalResult = poh.validateTransaction(unethicalTx);
  console.log(`Этический скор: ${unethicalResult.ethicalScore}/100`);
  console.log(`Результат валидации: ${unethicalResult.validationResult ? 'ПРИНЯТА' : 'ОТКЛОНЕНА'}`);
  console.log(`Причина: ${unethicalResult.validationReason}`);
  
  // Голосование валидаторов
  console.log('\nГолосование валидаторов:');
  const vote = await poh.submitValidatorVote('validator5', ethicalTx, true, 85);
  console.log(`Валидатор ${vote.validatorId} проголосовал ${vote.vote ? 'за' : 'против'} с оценкой ${vote.ethicalScore}`);
}

/**
 * Демонстрация EthicalMirrorEngine
 */
async function demoEthicalMirror(mirror: EthicalMirrorEngine) {
  console.log('\n=== Демонстрация EthicalMirrorEngine ===');
  
  // Чтение контракта
  const contractCode = fs.readFileSync(CONTRACT_PATH, 'utf-8');
  
  // Анализ этичности кода
  console.log('\nАнализ этичности кода:');
  const ethicsAnalysis = mirror.analyzeEthics(contractCode);
  
  console.log(`Этический скор: ${ethicsAnalysis.ethicalScore}/100`);
  console.log(`Найдено проблем: ${ethicsAnalysis.issues.length}`);
  
  if (ethicsAnalysis.issues.length > 0) {
    console.log('\nСписок проблем:');
    
    for (const issue of ethicsAnalysis.issues) {
      console.log(`- [${issue.severity.toUpperCase()}] ${issue.term}: ${issue.description}`);
    }
  }
  
  // Создание этического двойника
  console.log('\nСоздание этического двойника кода...');
  const transformResult = mirror.ethicalMirror(contractCode);
  
  console.log(`Выполнено ${transformResult.transformations.length} трансформаций за ${transformResult.executionTime} мс`);
  
  if (transformResult.transformations.length > 0) {
    console.log('\nСписок трансформаций:');
    
    for (const transform of transformResult.transformations) {
      console.log(`- ${transform.type}: "${transform.original}" -> "${transform.transformed}" (${transform.confidence}%)`);
    }
  }
  
  // Сохранение трансформированного кода
  const outputPath = path.join(__dirname, 'EthicalDrainContract.sol');
  mirror.saveTransformedCode(transformResult, outputPath);
  
  console.log(`\nЭтический двойник сохранен в: ${outputPath}`);
  
  // Пример из технического предложения
  console.log('\nПример из технического предложения:');
  const exampleCode = 'function drainWallet() { steal(funds); }';
  const transformedExample = mirror.ethicalMirror(exampleCode);
  
  console.log('Исходный код:');
  console.log(exampleCode);
  console.log('Трансформированный код:');
  console.log(transformedExample.transformedCode);
}

// Запуск демонстрации
runDemo().catch(error => {
  console.error('Ошибка при выполнении демонстрации:', error);
  process.exit(1);
});
