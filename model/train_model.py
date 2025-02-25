#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
train_model.py - Скрипт для обучения модели Neuro-Solidity Auditor

Этот скрипт обучает нейронную сеть для обнаружения уязвимостей в смарт-контрактах Solidity.
"""

import os
import sys
import json
import argparse
import glob
import re
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple, Optional
from moonlight_ai import MoonlightOptimizer  # Импорт оптимизатора Moonlight

# Константы
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = os.path.join(MODEL_DIR, '..', 'data', 'verified_contracts')
DEFAULT_OUTPUT_DIR = os.path.join(MODEL_DIR, 'neuro_auditor_model')
DEFAULT_EPOCHS = 100
DEFAULT_BATCH_SIZE = 32
DEFAULT_LEARNING_RATE = 0.001
DEFAULT_VALIDATION_SPLIT = 0.2
DEFAULT_TEST_SPLIT = 0.1

# Паттерны для поиска уязвимостей
VULNERABILITY_PATTERNS = {
    "reentrancy": r"(\.\s*call\s*{.*value\s*:.*})(?!.*_mutex)",
    "integer_overflow": r"(\+\+|\+=|=\s*\+)(?!.*SafeMath)",
    "unchecked_return": r"\.call\s*{.*}(?!.*require\s*\()",
    "tx_origin": r"tx\.origin(?!.*!=)",
    "unsecured_selfdestruct": r"selfdestruct|suicide"
}

def setup_argparse() -> argparse.Namespace:
    """Настройка аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Обучение модели Neuro-Solidity Auditor')
    parser.add_argument('--data-dir', type=str, default=DEFAULT_DATA_DIR,
                        help=f'Директория с верифицированными контрактами (по умолчанию: {DEFAULT_DATA_DIR})')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help=f'Директория для сохранения модели (по умолчанию: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--epochs', type=int, default=DEFAULT_EPOCHS,
                        help=f'Количество эпох обучения (по умолчанию: {DEFAULT_EPOCHS})')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE,
                        help=f'Размер батча (по умолчанию: {DEFAULT_BATCH_SIZE})')
    parser.add_argument('--learning-rate', type=float, default=DEFAULT_LEARNING_RATE,
                        help=f'Скорость обучения (по умолчанию: {DEFAULT_LEARNING_RATE})')
    parser.add_argument('--validation-split', type=float, default=DEFAULT_VALIDATION_SPLIT,
                        help=f'Доля данных для валидации (по умолчанию: {DEFAULT_VALIDATION_SPLIT})')
    parser.add_argument('--test-split', type=float, default=DEFAULT_TEST_SPLIT,
                        help=f'Доля данных для тестирования (по умолчанию: {DEFAULT_TEST_SPLIT})')
    parser.add_argument('--no-gpu', action='store_true',
                        help='Отключить использование GPU')
    parser.add_argument('--use-moonlight', action='store_true',
                        help='Использовать оптимизатор Moonlight вместо Adam')
    parser.add_argument('--moonlight-warmup', type=int, default=1000,
                        help='Количество шагов разогрева для Moonlight (по умолчанию: 1000)')
    
    return parser.parse_args()

def configure_gpu(use_gpu: bool = True) -> None:
    """Настройка GPU"""
    if not use_gpu:
        print("Отключение GPU...")
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        return
    
    # Проверка доступности GPU
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        print("GPU не обнаружен, используется CPU")
        return
    
    print(f"Обнаружено {len(gpus)} GPU устройств")
    
    # Настройка памяти GPU
    for gpu in gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
            print(f"Динамическое выделение памяти включено для {gpu}")
        except RuntimeError as e:
            print(f"Ошибка при настройке GPU: {e}")

def load_contracts(data_dir: str) -> List[str]:
    """Загрузка контрактов из директории"""
    contract_files = glob.glob(os.path.join(data_dir, '*.sol'))
    print(f"Найдено {len(contract_files)} контрактов в {data_dir}")
    
    contracts = []
    for file_path in contract_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contracts.append(f.read())
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")
    
    print(f"Загружено {len(contracts)} контрактов")
    return contracts

def extract_features(contract: str) -> Dict[str, Any]:
    """Извлечение признаков из контракта"""
    features = {}
    
    # Базовые статистические признаки
    features['length'] = len(contract)
    features['line_count'] = contract.count('\n') + 1
    
    # Подсчет ключевых слов
    keywords = ['function', 'contract', 'modifier', 'event', 'struct', 'enum',
                'mapping', 'address', 'uint', 'int', 'bool', 'string', 'bytes',
                'public', 'private', 'internal', 'external', 'view', 'pure',
                'payable', 'virtual', 'override', 'abstract', 'interface']
    
    for keyword in keywords:
        pattern = r'\b' + keyword + r'\b'
        features[f'count_{keyword}'] = len(re.findall(pattern, contract))
    
    # Подсчет операторов
    operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=',
                 '&&', '||', '!', '++', '--', '+=', '-=', '*=', '/=']
    
    for operator in operators:
        # Экранирование специальных символов в регулярных выражениях
        escaped_operator = re.escape(operator)
        features[f'count_op_{operator}'] = len(re.findall(escaped_operator, contract))
    
    # Подсчет вызовов функций
    function_calls = ['transfer', 'send', 'call', 'delegatecall', 'staticcall',
                      'require', 'assert', 'revert', 'selfdestruct', 'suicide']
    
    for func in function_calls:
        pattern = r'\.' + func + r'\b|\b' + func + r'\s*\('
        features[f'count_call_{func}'] = len(re.findall(pattern, contract))
    
    # Подсчет уязвимостей
    for vuln_name, pattern in VULNERABILITY_PATTERNS.items():
        features[f'has_{vuln_name}'] = 1 if re.search(pattern, contract, re.IGNORECASE) else 0
    
    # Подсчет функций
    features['function_count'] = len(re.findall(r'function\s+\w+\s*\(', contract))
    
    # Подсчет переменных состояния
    features['state_vars_count'] = len(re.findall(r'(uint|int|bool|address|string|bytes|mapping)\s+\w+', contract))
    
    # Подсчет модификаторов
    features['modifier_count'] = len(re.findall(r'modifier\s+\w+\s*\(', contract))
    
    # Подсчет событий
    features['event_count'] = len(re.findall(r'event\s+\w+\s*\(', contract))
    
    # Оценка сложности контракта
    complexity = 0
    complexity += features['function_count'] * 2
    complexity += features['state_vars_count']
    complexity += features['modifier_count'] * 1.5
    complexity += features['event_count']
    complexity += sum(features[f'count_op_{op}'] for op in ['&&', '||', '!'])
    complexity += sum(features[f'count_call_{func}'] for func in ['require', 'assert', 'revert'])
    
    features['complexity'] = complexity
    
    return features

def prepare_dataset(contracts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    """Подготовка датасета для обучения"""
    print("Подготовка датасета...")
    
    # Извлечение признаков
    features_list = []
    labels = []
    
    for contract in contracts:
        features = extract_features(contract)
        features_list.append(features)
        
        # Определение метки (есть ли уязвимости)
        has_vulnerability = any(features[f'has_{vuln_name}'] for vuln_name in VULNERABILITY_PATTERNS.keys())
        labels.append(1 if has_vulnerability else 0)
    
    # Преобразование списка словарей в DataFrame
    df = pd.DataFrame(features_list)
    
    # Удаление признаков с метками уязвимостей (чтобы модель не читерила)
    for vuln_name in VULNERABILITY_PATTERNS.keys():
        if f'has_{vuln_name}' in df.columns:
            df = df.drop(f'has_{vuln_name}', axis=1)
    
    # Нормализация признаков
    scaler = StandardScaler()
    X = scaler.fit_transform(df)
    y = np.array(labels)
    
    print(f"Подготовлено {len(X)} образцов, {sum(y)} с уязвимостями ({sum(y)/len(y)*100:.1f}%)")
    
    return X, y

def create_model(input_dim: int) -> tf.keras.Model:
    """Создание модели нейронной сети"""
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])
    
    return model

def train_model(X: np.ndarray, y: np.ndarray, args: argparse.Namespace) -> tf.keras.Model:
    """Обучение модели"""
    print("Разделение данных на обучающую, валидационную и тестовую выборки...")
    
    # Разделение на обучающую и тестовую выборки
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=args.test_split, random_state=42, stratify=y
    )
    
    # Разделение на обучающую и валидационную выборки
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, 
        test_size=args.validation_split / (1 - args.test_split),
        random_state=42, stratify=y_train_val
    )
    
    print(f"Размеры выборок: обучающая={X_train.shape}, валидационная={X_val.shape}, тестовая={X_test.shape}")
    
    # Создание модели
    print("Создание модели...")
    model = create_model(X_train.shape[1])
    
    # Компиляция модели
    model.compile(
        optimizer=optimizers.Adam(learning_rate=args.learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), 
                 tf.keras.metrics.AUC()]
    )
    
    # Вывод информации о модели
    model.summary()
    
    # Создание директории для сохранения модели
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Настройка колбэков
    callbacks = [
        ModelCheckpoint(
            filepath=os.path.join(args.output_dir, 'best_model.h5'),
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            verbose=1,
            restore_best_weights=True
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            verbose=1,
            min_lr=1e-6
        )
    ]
    
    # Обучение модели
    print(f"Обучение модели на {len(X_train)} образцах...")
    history = model.fit(
        X_train, y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1
    )
    
    # Оценка модели на тестовой выборке
    print("Оценка модели на тестовой выборке...")
    test_loss, test_acc, test_precision, test_recall, test_auc = model.evaluate(X_test, y_test)
    print(f"Тестовая точность: {test_acc:.4f}")
    print(f"Тестовая точность (precision): {test_precision:.4f}")
    print(f"Тестовая полнота (recall): {test_recall:.4f}")
    print(f"Тестовая AUC: {test_auc:.4f}")
    
    # Предсказания на тестовой выборке
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()
    
    # Вывод отчета о классификации
    print("\nОтчет о классификации:")
    print(classification_report(y_test, y_pred, target_names=['Безопасный', 'Уязвимый']))
    
    # Вывод матрицы ошибок
    print("\nМатрица ошибок:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Сохранение модели
    print(f"Сохранение модели в {args.output_dir}...")
    model.save(os.path.join(args.output_dir, 'model.h5'))
    
    # Сохранение модели в формате TensorFlow.js
    try:
        import tensorflowjs as tfjs
        tfjs_path = os.path.join(args.output_dir, 'tfjs_model')
        os.makedirs(tfjs_path, exist_ok=True)
        tfjs.converters.save_keras_model(model, tfjs_path)
        print(f"Модель сохранена в формате TensorFlow.js в {tfjs_path}")
    except ImportError:
        print("Не удалось сохранить модель в формате TensorFlow.js. Установите tensorflowjs: pip install tensorflowjs")
    
    # Построение графиков
    plot_training_history(history, args.output_dir)
    
    return model

def plot_training_history(history: tf.keras.callbacks.History, output_dir: str) -> None:
    """Построение графиков обучения"""
    print("Построение графиков обучения...")
    
    # График точности
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Обучение')
    plt.plot(history.history['val_accuracy'], label='Валидация')
    plt.title('Точность')
    plt.xlabel('Эпоха')
    plt.ylabel('Точность')
    plt.legend()
    
    # График функции потерь
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Обучение')
    plt.plot(history.history['val_loss'], label='Валидация')
    plt.title('Функция потерь')
    plt.xlabel('Эпоха')
    plt.ylabel('Потери')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_history.png'))
    plt.close()
    
    # График precision и recall
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['precision'], label='Precision (Обучение)')
    plt.plot(history.history['val_precision'], label='Precision (Валидация)')
    plt.title('Precision')
    plt.xlabel('Эпоха')
    plt.ylabel('Precision')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['recall'], label='Recall (Обучение)')
    plt.plot(history.history['val_recall'], label='Recall (Валидация)')
    plt.title('Recall')
    plt.xlabel('Эпоха')
    plt.ylabel('Recall')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'precision_recall.png'))
    plt.close()

def main() -> None:
    """Основная функция"""
    # Парсинг аргументов командной строки
    args = setup_argparse()
    
    # Настройка GPU
    configure_gpu(not args.no_gpu)
    
    # Загрузка контрактов
    contracts = load_contracts(args.data_dir)
    
    if not contracts:
        print("Не удалось загрузить контракты. Выход.")
        sys.exit(1)
    
    # Подготовка датасета
    X, y = prepare_dataset(contracts)
    
    # Обучение модели
    model = train_model(X, y, args)
    
    print(f"Обучение завершено. Модель сохранена в {args.output_dir}")

if __name__ == "__main__":
    main()
