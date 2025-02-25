/**
 * DEP Framework - Настройка тестового окружения Jest
 * 
 * Этот файл выполняется перед запуском тестов и настраивает тестовое окружение.
 * 
 * @author DEP Framework Team
 */

// Загрузка переменных окружения из .env.test, если файл существует
const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');

const envTestPath = path.join(__dirname, '..', '.env.test');
const envPath = path.join(__dirname, '..', '.env');

// Приоритет: .env.test > .env
if (fs.existsSync(envTestPath)) {
  console.log('Загрузка переменных окружения из .env.test');
  dotenv.config({ path: envTestPath });
} else if (fs.existsSync(envPath)) {
  console.log('Загрузка переменных окружения из .env');
  dotenv.config({ path: envPath });
} else {
  console.log('Файлы .env.test и .env не найдены. Используются значения по умолчанию.');
}

// Увеличение таймаута для тестов
jest.setTimeout(30000);

// Мокирование внешних зависимостей
jest.mock('@solana/web3.js', () => {
  const originalModule = jest.requireActual('@solana/web3.js');
  
  // Мок для Connection
  class MockConnection {
    constructor() {
      this.rpcEndpoint = 'mock-endpoint';
    }
    
    async getBalance() {
      return 1000000000;
    }
    
    async getRecentBlockhash() {
      return {
        blockhash: 'mock-blockhash',
        feeCalculator: {
          lamportsPerSignature: 5000
        }
      };
    }
  }
  
  // Мок для Transaction
  class MockTransaction {
    constructor() {
      this.signatures = [];
      this.instructions = [];
    }
    
    add(instruction) {
      this.instructions.push(instruction);
      return this;
    }
    
    sign() {
      this.signatures.push({
        signature: Buffer.from('mock-signature')
      });
      return this;
    }
  }
  
  // Мок для PublicKey
  class MockPublicKey {
    constructor(value) {
      this.value = value;
    }
    
    toString() {
      return this.value;
    }
    
    toBuffer() {
      return Buffer.from(this.value);
    }
  }
  
  return {
    ...originalModule,
    Connection: MockConnection,
    Transaction: MockTransaction,
    PublicKey: MockPublicKey,
    clusterApiUrl: (network) => `https://api.${network}.solana.com`,
    SystemProgram: {
      transfer: ({ fromPubkey, toPubkey, lamports }) => ({
        fromPubkey,
        toPubkey,
        lamports
      })
    }
  };
});

// Глобальные моки
global.console = {
  ...console,
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  info: jest.fn(),
  debug: jest.fn(),
};

// Очистка моков после каждого теста
afterEach(() => {
  jest.clearAllMocks();
});
