# Руководство по использованию DEP Framework

## Содержание

1. [Установка](#установка)
2. [Настройка](#настройка)
3. [Использование Neuro-Solidity Auditor](#использование-neuro-solidity-auditor)
4. [Использование Proof-of-Humanism](#использование-proof-of-humanism)
5. [Использование Ethical Mirror Engine](#использование-ethical-mirror-engine)
6. [Примеры использования](#примеры-использования)
7. [Часто задаваемые вопросы](#часто-задаваемые-вопросы)

## Установка

### Требования

- Node.js 16.x или выше
- npm 8.x или выше
- TypeScript 4.5.x или выше
- Solana CLI (опционально, для работы с блокчейном Solana)

### Установка из npm

```bash
npm install dep-framework
```

### Установка из исходного кода

```bash
# Клонирование репозитория
git clone https://github.com/dep-framework/dep-framework.git
cd dep-framework

# Установка зависимостей
npm install

# Сборка проекта
npm run build
```

## Настройка

### Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Пример содержимого файла `.env`:

```
# Настройки Solana
SOLANA_NETWORK=devnet
SOLANA_RPC_URL=https://api.devnet.solana.com

# Ключи API
ETHERSCAN_API_KEY=your_etherscan_api_key_here
SOLSCAN_API_KEY=your_solscan_api_key_here

# Настройки NeuroSolidityAuditor
MODEL_PATH=./models/neuro_auditor_model
CONTRACTS_DB_PATH=./data/verified_contracts

# Настройки ProofOfHumanism
ETHICAL_THRESHOLD=75
DAO_CONTRACT_ADDRESS=your_dao_contract_address_here
```

### Инициализация фреймворка

```typescript
import { DEPFramework } from 'dep-framework';

// Создание экземпляра фреймворка
const framework = new DEPFramework();

// Инициализация и запуск
await framework.start();

// Получение компонентов
const neuroAuditor = framework.getNeuroAuditor();
const proofOfHumanism = framework.getProofOfHumanism();
const ethicalMirror = framework.getEthicalMirror();
```

## Использование Neuro-Solidity Auditor

### Аудит смарт-контракта

```typescript
import { NeuroSolidityAuditor } from 'dep-framework';

// Создание экземпляра аудитора
const auditor = new NeuroSolidityAuditor();
await auditor.initialize();

// Путь к файлу контракта
const contractPath = './contracts/MyContract.sol';

// Аудит контракта
const auditResult = await auditor.auditContract(contractPath);

// Вывод результатов
console.log(`Общий скор безопасности: ${auditResult.score}/100`);
console.log(`Найдено уязвимостей: ${auditResult.vulnerabilities.length}`);

// Вывод найденных уязвимостей
for (const vuln of auditResult.vulnerabilities) {
  console.log(`[${vuln.severity.toUpperCase()}] ${vuln.name}`);
  console.log(`Строки: ${vuln.lineStart}-${vuln.lineEnd}`);
  console.log(`Описание: ${vuln.description}`);
  console.log(`Рекомендация: ${vuln.recommendation}`);
}
```

### Генерация тест-кейсов

```typescript
// Генерация тест-кейсов для контракта
const testCases = await auditor.generateTestCases(contractPath);

// Вывод тест-кейсов
for (const test of testCases) {
  console.log(`Тест: ${test.description}`);
  console.log(`Входные данные: ${JSON.stringify(test.inputs)}`);
  console.log(`Ожидаемый результат: ${JSON.stringify(test.expectedOutputs)}`);
  console.log(`Edge-case: ${test.edgeCase ? 'Да' : 'Нет'}`);
}
```

### Генерация патчей для уязвимостей

```typescript
// Генерация патча для первой найденной уязвимости
if (auditResult.vulnerabilities.length > 0) {
  const vulnerability = auditResult.vulnerabilities[0];
  const patch = await auditor.generatePatch(vulnerability, contractPath);
  
  console.log(`Патч для уязвимости ${vulnerability.name}:`);
  console.log(patch);
}
```

## Использование Proof-of-Humanism

### Валидация транзакции

```typescript
import { ProofOfHumanism } from 'dep-framework';
import * as web3 from '@solana/web3.js';

// Создание экземпляра ProofOfHumanism
const poh = new ProofOfHumanism();
await poh.initialize();

// Создание транзакции Solana
const transaction = new web3.Transaction().add(
  web3.SystemProgram.transfer({
    fromPubkey: new web3.PublicKey('senderPublicKey'),
    toPubkey: new web3.PublicKey('recipientPublicKey'),
    lamports: 1000000000,
  })
);

// Валидация транзакции
const validationResult = poh.validateTransaction(transaction);

console.log(`Этический скор: ${validationResult.ethicalScore}/100`);
console.log(`Результат валидации: ${validationResult.validationResult ? 'ПРИНЯТА' : 'ОТКЛОНЕНА'}`);
console.log(`Причина: ${validationResult.validationReason}`);
```

### Получение и обновление порога этичности

```typescript
// Получение текущего порога этичности
const threshold = poh.getEthicalThreshold();
console.log(`Текущий порог этичности: ${threshold.value}`);

// Предложение нового порога этичности
const proposerId = 'validator123';
const newThresholdValue = 80;
const proposal = await poh.proposeNewThreshold(proposerId, newThresholdValue);

// Обновление порога этичности
poh.updateEthicalThreshold(proposal);
```

### Голосование валидаторов

```typescript
// Голосование валидатора за транзакцию
const validatorId = 'validator123';
const vote = true; // За транзакцию
const ethicalScore = 85; // Оценка этичности от валидатора

const voteResult = await poh.submitValidatorVote(validatorId, transaction, vote, ethicalScore);
console.log(`Валидатор ${voteResult.validatorId} проголосовал ${voteResult.vote ? 'за' : 'против'}`);
```

## Использование Ethical Mirror Engine

### Анализ этичности кода

```typescript
import { EthicalMirrorEngine } from 'dep-framework';
import * as fs from 'fs';

// Создание экземпляра EthicalMirrorEngine
const mirror = new EthicalMirrorEngine();
await mirror.initialize();

// Чтение кода контракта
const contractPath = './contracts/MyContract.sol';
const contractCode = fs.readFileSync(contractPath, 'utf-8');

// Анализ этичности кода
const ethicsAnalysis = mirror.analyzeEthics(contractCode);

console.log(`Этический скор: ${ethicsAnalysis.ethicalScore}/100`);
console.log(`Найдено проблем: ${ethicsAnalysis.issues.length}`);

// Вывод найденных проблем
for (const issue of ethicsAnalysis.issues) {
  console.log(`[${issue.severity.toUpperCase()}] ${issue.term}: ${issue.description}`);
}
```

### Создание этического двойника кода

```typescript
// Создание этического двойника кода
const transformResult = mirror.ethicalMirror(contractCode);

console.log(`Выполнено ${transformResult.transformations.length} трансформаций`);

// Вывод трансформаций
for (const transform of transformResult.transformations) {
  console.log(`${transform.type}: "${transform.original}" -> "${transform.transformed}"`);
}

// Сохранение трансформированного кода
const outputPath = './contracts/EthicalMyContract.sol';
mirror.saveTransformedCode(transformResult, outputPath);
```

### Добавление новых паттернов трансформации

```typescript
// Добавление нового этического паттерна
mirror.addTransformationPattern('malicious', 'benevolent', 'ethical');

// Добавление нового паттерна безопасности
mirror.addTransformationPattern('unsafe', 'safe', 'security');
```

## Примеры использования

В директории `examples` находятся примеры использования DEP Framework:

- `demo.ts` - демонстрация основных возможностей фреймворка
- `DrainContract.sol` - пример контракта с уязвимостями для тестирования

Запуск демонстрационного примера:

```bash
npm run example
```

## Часто задаваемые вопросы

### Как обновить модель нейросети?

Модель нейросети для Neuro-Solidity Auditor хранится в директории, указанной в переменной окружения `MODEL_PATH`. Для обновления модели замените файлы в этой директории на новые.

### Как настроить порог этичности?

Порог этичности для Proof-of-Humanism можно настроить через DAO голосование или напрямую через метод `updateEthicalThreshold()`.

### Как добавить новые паттерны трансформации?

Новые паттерны трансформации для Ethical Mirror Engine можно добавить через метод `addTransformationPattern()` или через файл конфигурации, указанный в переменной окружения `TRANSFORMATION_PATTERNS_PATH`.

### Как интегрировать DEP Framework с существующим проектом?

DEP Framework можно интегрировать с существующим проектом через npm-пакет или напрямую из исходного кода. Для интеграции с CI/CD пайплайном можно использовать CLI-интерфейс фреймворка.
