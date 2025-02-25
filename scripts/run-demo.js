#!/usr/bin/env node

/**
 * DEP Framework - Скрипт для запуска демонстрационного примера
 * 
 * Этот скрипт запускает демонстрационный пример использования DEP Framework.
 * 
 * @author DEP Framework Team
 */

const path = require('path');
const { execSync } = require('child_process');
const fs = require('fs');

// Проверка наличия файла .env
const envPath = path.join(__dirname, '..', '.env');
const envExamplePath = path.join(__dirname, '..', '.env.example');

if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
  console.log('Файл .env не найден. Копирование из .env.example...');
  fs.copyFileSync(envExamplePath, envPath);
  console.log('Файл .env создан. Пожалуйста, заполните необходимые значения перед запуском демонстрации.');
}

// Проверка наличия директорий для данных
const dataDir = path.join(__dirname, '..', 'data');
const modelsDir = path.join(__dirname, '..', 'models');
const contractsDir = path.join(dataDir, 'verified_contracts');

if (!fs.existsSync(dataDir)) {
  console.log('Создание директории для данных...');
  fs.mkdirSync(dataDir, { recursive: true });
}

if (!fs.existsSync(modelsDir)) {
  console.log('Создание директории для моделей...');
  fs.mkdirSync(modelsDir, { recursive: true });
}

if (!fs.existsSync(contractsDir)) {
  console.log('Создание директории для верифицированных контрактов...');
  fs.mkdirSync(contractsDir, { recursive: true });
}

// Копирование VulnerableContract.sol в DrainContract.sol для демонстрации
const vulnerableContractPath = path.join(contractsDir, 'VulnerableContract.sol');
const drainContractPath = path.join(__dirname, '..', 'examples', 'DrainContract.sol');

if (fs.existsSync(vulnerableContractPath)) {
  console.log(`Копирование ${vulnerableContractPath} в ${drainContractPath}...`);
  fs.copyFileSync(vulnerableContractPath, drainContractPath);
  console.log('Контракт успешно скопирован для демонстрации.');
} else {
  console.log(`Предупреждение: Файл ${vulnerableContractPath} не найден. Будет использован существующий DrainContract.sol.`);
}

// Запуск демонстрационного примера
console.log('Запуск демонстрационного примера DEP Framework...');

try {
  // Проверка наличия скомпилированных файлов
  const demoPath = path.join(__dirname, '..', 'dist', 'examples', 'demo.js');
  
  if (!fs.existsSync(demoPath)) {
    console.log('Компиляция проекта...');
    execSync('npm run build', { stdio: 'inherit' });
  }
  
  // Запуск демонстрации
  console.log('\n=== DEP Framework Demo ===\n');
  execSync('node dist/examples/demo.js', { stdio: 'inherit' });
} catch (error) {
  console.error('Ошибка при запуске демонстрации:', error.message);
  process.exit(1);
}
