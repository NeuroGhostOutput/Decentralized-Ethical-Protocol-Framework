/**
 * DEP Framework - Decentralized Ethical Protocol Framework
 * 
 * Основной файл приложения, объединяющий все компоненты фреймворка.
 * 
 * @module DEPFramework
 * @author DEP Framework Team
 * @version 0.1.0
 */

import { NeuroSolidityAuditor } from './neuro-solidity-auditor';
import { ProofOfHumanism } from './proof-of-humanism';
import { EthicalMirrorEngine } from './ethical-mirror-engine';
import dotenv from 'dotenv';

// Загрузка переменных окружения
dotenv.config();

/**
 * Класс DEPFramework - основной класс фреймворка, объединяющий все компоненты
 */
export class DEPFramework {
  private neuroAuditor: NeuroSolidityAuditor;
  private proofOfHumanism: ProofOfHumanism;
  private ethicalMirror: EthicalMirrorEngine;

  /**
   * Конструктор класса DEPFramework
   */
  constructor() {
    console.log('Инициализация DEP Framework...');
    
    // Инициализация компонентов
    this.neuroAuditor = new NeuroSolidityAuditor();
    this.proofOfHumanism = new ProofOfHumanism();
    this.ethicalMirror = new EthicalMirrorEngine();
    
    console.log('DEP Framework успешно инициализирован');
  }

  /**
   * Запуск всех компонентов фреймворка
   */
  public async start(): Promise<void> {
    console.log('Запуск DEP Framework...');
    
    try {
      // Запуск компонентов
      await this.neuroAuditor.initialize();
      await this.proofOfHumanism.initialize();
      await this.ethicalMirror.initialize();
      
      console.log('Все компоненты DEP Framework успешно запущены');
    } catch (error) {
      console.error('Ошибка при запуске DEP Framework:', error);
      throw error;
    }
  }

  /**
   * Получение экземпляра NeuroSolidityAuditor
   */
  public getNeuroAuditor(): NeuroSolidityAuditor {
    return this.neuroAuditor;
  }

  /**
   * Получение экземпляра ProofOfHumanism
   */
  public getProofOfHumanism(): ProofOfHumanism {
    return this.proofOfHumanism;
  }

  /**
   * Получение экземпляра EthicalMirrorEngine
   */
  public getEthicalMirror(): EthicalMirrorEngine {
    return this.ethicalMirror;
  }
}

// Если файл запущен напрямую, а не импортирован
if (require.main === module) {
  const framework = new DEPFramework();
  framework.start().catch(err => {
    console.error('Критическая ошибка при запуске DEP Framework:', err);
    process.exit(1);
  });
}

// Экспорт всех компонентов для использования в других модулях
export { NeuroSolidityAuditor, ProofOfHumanism, EthicalMirrorEngine };
