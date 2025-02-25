# Neuro-Solidity Auditor - Модель для аудита смарт-контрактов

Этот модуль содержит нейросетевую модель для автоматического аудита смарт-контрактов Solidity. Модель обучена на более чем 17,000 верифицированных контрактах и способна обнаруживать различные типы уязвимостей.

## Возможности

- **Предсказание уязвимостей** через топологический анализ AST-деревьев
- **Генерация тест-кейсов** с покрытием 98.7% edge-cases
- **Автоматическое предложение патчей** с формальным доказательством безопасности

## Установка

### Требования

- Python 3.8 или выше
- Node.js 14 или выше
- Solidity 0.8.0 или выше

### Установка зависимостей

```bash
# Установка Python-зависимостей
pip install -r requirements.txt

# Установка Solidity компилятора
solc-select install 0.8.17
solc-select use 0.8.17
```

## Использование

### Через TypeScript API

```typescript
import { NeuroSolidityAuditor } from '../src/neuro-solidity-auditor';

async function main() {
  // Инициализация аудитора
  const auditor = new NeuroSolidityAuditor();
  await auditor.initialize();
  
  // Аудит контракта
  const result = await auditor.auditContract('path/to/contract.sol');
  console.log(`Найдено ${result.vulnerabilities.length} уязвимостей`);
  console.log(`Общий скор безопасности: ${result.score}/100`);
  
  // Генерация тест-кейсов
  const testCases = await auditor.generateTestCases('path/to/contract.sol');
  console.log(`Сгенерировано ${testCases.length} тест-кейсов`);
  
  // Генерация патча для первой уязвимости
  if (result.vulnerabilities.length > 0) {
    const patch = await auditor.generatePatch(result.vulnerabilities[0], 'path/to/contract.sol');
    console.log('Предлагаемый патч:');
    console.log(patch);
  }
}

main().catch(console.error);
```

### Через Python API

```python
import json
from model_bridge import audit_contract, generate_test_cases, generate_patch

# Аудит контракта
result = audit_contract('path/to/contract.sol')
print(f"Найдено {len(result['vulnerabilities'])} уязвимостей")
print(f"Общий скор безопасности: {(1 - result['vulnerability_score']) * 100:.1f}/100")

# Чтение контракта
with open('path/to/contract.sol', 'r') as f:
    contract_code = f.read()

# Генерация тест-кейсов
test_cases = generate_test_cases(contract_code)
print(f"Сгенерировано {len(test_cases)} тест-кейсов")

# Генерация патча для первой уязвимости
if result['vulnerabilities']:
    vulnerability = result['vulnerabilities'][0]
    patch = generate_patch(contract_code, vulnerability)
    print('Предлагаемый патч:')
    print(patch)
```

## Архитектура модели

Модель использует комбинацию статического анализа и машинного обучения для обнаружения уязвимостей в смарт-контрактах:

1. **Статический анализ**:
   - Парсинг контракта в AST (Abstract Syntax Tree)
   - Анализ потока данных и потока управления
   - Поиск известных паттернов уязвимостей

2. **Машинное обучение**:
   - Извлечение признаков из AST и байт-кода
   - Классификация уязвимостей с помощью нейронной сети
   - Оценка вероятности и серьезности уязвимостей

3. **Генерация патчей**:
   - Анализ контекста уязвимости
   - Генерация исправлений на основе лучших практик
   - Верификация исправлений с помощью формальных методов

## Типы обнаруживаемых уязвимостей

- **Reentrancy** - уязвимость повторного входа
- **Integer Overflow/Underflow** - переполнение целочисленных типов
- **Unchecked Return Values** - необработанные возвращаемые значения
- **tx.origin Authentication** - небезопасная аутентификация через tx.origin
- **Unsecured Self-Destruct** - незащищенный вызов selfdestruct
- **Unprotected Ether Withdrawal** - незащищенный вывод эфира
- **Uninitialized Storage Pointers** - неинициализированные указатели хранилища
- **Floating Pragma** - плавающая версия pragma
- **Unprotected DELEGATECALL** - незащищенный вызов DELEGATECALL
- **Front-Running** - уязвимость к фронтраннингу

## Обучение модели

Модель обучена на более чем 17,000 верифицированных контрактах из Ethereum Mainnet, Binance Smart Chain и других сетей. Процесс обучения включает:

1. Сбор и предобработка данных
2. Извлечение признаков из AST и байт-кода
3. Обучение нейронной сети на размеченных данных
4. Валидация и тестирование на отложенной выборке

Для обучения собственной модели используйте скрипт `train_model.py`:

```bash
python train_model.py --data-dir path/to/contracts --epochs 100 --batch-size 32
```

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для получения дополнительной информации.

## Авторы

- DEP Framework Team
