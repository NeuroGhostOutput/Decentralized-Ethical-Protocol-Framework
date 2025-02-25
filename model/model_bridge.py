#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
model_bridge.py - Мост между TypeScript и Python-моделью для аудита смарт-контрактов

Этот скрипт обрабатывает запросы от NeuroSolidityAuditor и возвращает результаты в формате JSON.
"""

import argparse
import json
import os
import sys
import re
from typing import Dict, List, Any, Optional, Tuple

# Путь к директории с моделью
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

# Паттерны для поиска уязвимостей
VULNERABILITY_PATTERNS = {
    "reentrancy": r"(\.\s*call\s*{.*value\s*:.*})(?!.*_mutex)",
    "integer_overflow": r"(\+\+|\+=|=\s*\+)(?!.*SafeMath)",
    "unchecked_return": r"\.call\s*{.*}(?!.*require\s*\()",
    "tx_origin": r"tx\.origin(?!.*!=)",
    "unsecured_selfdestruct": r"selfdestruct|suicide"
}

# Соответствие между ключами уязвимостей и их названиями
VULNERABILITY_NAMES = {
    "reentrancy": "Reentrancy Vulnerability",
    "integer_overflow": "Integer Overflow",
    "unchecked_return": "Unchecked Return Value",
    "tx_origin": "tx.origin Authentication",
    "unsecured_selfdestruct": "Unsecured Self-Destruct"
}

# Соответствие между ключами уязвимостей и их серьезностью
VULNERABILITY_SEVERITIES = {
    "reentrancy": "critical",
    "integer_overflow": "high",
    "unchecked_return": "medium",
    "tx_origin": "high",
    "unsecured_selfdestruct": "critical"
}

def read_contract(contract_path: str) -> str:
    """Чтение контракта из файла"""
    try:
        with open(contract_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при чтении контракта: {e}", file=sys.stderr)
        return ""

def analyze_ast_topology(contract_code: str) -> Dict[str, Any]:
    """Анализ AST-топологии контракта"""
    # В реальном приложении здесь будет парсинг контракта в AST и анализ
    # Для примера используем заглушку
    
    # Подсчет количества функций
    function_count = len(re.findall(r"function\s+\w+\s*\(", contract_code))
    
    # Подсчет количества переменных состояния
    state_vars_count = len(re.findall(r"(uint|int|bool|address|string|bytes|mapping)\s+\w+", contract_code))
    
    # Подсчет количества модификаторов
    modifier_count = len(re.findall(r"modifier\s+\w+\s*\(", contract_code))
    
    # Подсчет количества событий
    event_count = len(re.findall(r"event\s+\w+\s*\(", contract_code))
    
    # Оценка сложности контракта
    complexity = "low"
    if function_count > 10 or state_vars_count > 15:
        complexity = "high"
    elif function_count > 5 or state_vars_count > 10:
        complexity = "medium"
    
    return {
        "nodes": function_count + state_vars_count + modifier_count + event_count,
        "edges": function_count * 2,  # Примерная оценка связей между функциями
        "depth": 3 + (function_count // 3),  # Примерная оценка глубины вызовов
        "complexity": complexity
    }

def find_vulnerabilities(contract_code: str) -> List[Dict[str, Any]]:
    """Поиск уязвимостей в контракте"""
    vulnerabilities = []
    
    # Разбиение кода на строки
    lines = contract_code.split('\n')
    
    # Поиск уязвимостей по паттернам
    for i, line in enumerate(lines):
        for vuln_key, pattern in VULNERABILITY_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                # Получение контекста (несколько строк до и после)
                start_idx = max(0, i - 2)
                end_idx = min(len(lines), i + 3)
                context = '\n'.join(lines[start_idx:end_idx])
                
                # Создание объекта уязвимости
                vulnerability = {
                    "name": VULNERABILITY_NAMES.get(vuln_key, "Unknown Vulnerability"),
                    "severity": VULNERABILITY_SEVERITIES.get(vuln_key, "medium"),
                    "confidence": 0.85,
                    "lines": [
                        {
                            "line_number": i + 1,
                            "line": line.strip(),
                            "context": context
                        }
                    ]
                }
                
                vulnerabilities.append(vulnerability)
    
    return vulnerabilities

def audit_contract(contract_path: str) -> Dict[str, Any]:
    """Аудит смарт-контракта"""
    # Чтение контракта
    contract_code = read_contract(contract_path)
    if not contract_code:
        return {
            "is_vulnerable": False,
            "vulnerability_score": 0.0,
            "vulnerabilities": [],
            "features": {},
            "error": "Не удалось прочитать контракт"
        }
    
    # Поиск уязвимостей
    vulnerabilities = find_vulnerabilities(contract_code)
    
    # Анализ AST-топологии
    features = analyze_ast_topology(contract_code)
    
    # Расчет общего скора уязвимости
    vulnerability_score = 0.0
    if vulnerabilities:
        # Веса для разных уровней серьезности
        severity_weights = {
            "critical": 0.3,
            "high": 0.2,
            "medium": 0.1,
            "low": 0.05,
            "info": 0.01
        }
        
        # Расчет общего штрафа
        total_penalty = 0.0
        for vuln in vulnerabilities:
            total_penalty += severity_weights.get(vuln["severity"], 0.1)
        
        # Ограничение максимального штрафа до 1.0
        vulnerability_score = min(total_penalty, 1.0)
    
    return {
        "is_vulnerable": bool(vulnerabilities),
        "vulnerability_score": vulnerability_score,
        "vulnerabilities": vulnerabilities,
        "features": features
    }

def generate_test_cases(contract_code: str) -> List[Dict[str, Any]]:
    """Генерация тест-кейсов для контракта"""
    test_cases = []
    
    # Поиск функций в контракте
    function_matches = re.finditer(r"function\s+(\w+)\s*\(([^)]*)\)\s*(public|external|internal|private)?\s*(view|pure|payable)?\s*(?:returns\s*\(([^)]*)\))?\s*{", contract_code)
    
    for match in function_matches:
        function_name = match.group(1)
        params_str = match.group(2)
        visibility = match.group(3) or "public"
        mutability = match.group(4)
        returns_str = match.group(5)
        
        # Пропуск внутренних и приватных функций
        if visibility in ["internal", "private"]:
            continue
        
        # Парсинг параметров
        params = {}
        if params_str:
            param_matches = re.finditer(r"(\w+)\s+(\w+)(?:\s*,\s*)?", params_str)
            for param_match in param_matches:
                param_type = param_match.group(1)
                param_name = param_match.group(2)
                
                # Генерация значения параметра в зависимости от типа
                if param_type == "uint" or param_type.startswith("uint"):
                    params[param_name] = 100
                elif param_type == "int" or param_type.startswith("int"):
                    params[param_name] = -10
                elif param_type == "bool":
                    params[param_name] = True
                elif param_type == "address":
                    params[param_name] = "0x1234567890123456789012345678901234567890"
                elif param_type == "string":
                    params[param_name] = "test"
                elif param_type.startswith("bytes"):
                    params[param_name] = "0x1234"
                else:
                    params[param_name] = None
        
        # Создание стандартного тест-кейса
        test_cases.append({
            "description": f"Стандартный вызов функции {function_name}",
            "function": function_name,
            "params": params,
            "expected": "success",
            "edge_case": False
        })
        
        # Создание edge-case тест-кейса
        edge_params = params.copy()
        for param_name, value in params.items():
            if isinstance(value, int):
                edge_params[param_name] = 2**256 - 1  # Максимальное значение для uint256
        
        test_cases.append({
            "description": f"Edge-case для функции {function_name} с экстремальными значениями",
            "function": function_name,
            "params": edge_params,
            "expected": "revert",
            "edge_case": True
        })
    
    return test_cases

def generate_patch(contract_code: str, vulnerability: Dict[str, Any]) -> str:
    """Генерация патча для исправления уязвимости"""
    # Получение информации о уязвимости
    vuln_name = vulnerability["name"]
    lines = vulnerability["lines"]
    
    if not lines:
        return "// Не удалось сгенерировать патч: недостаточно информации о уязвимости"
    
    # Получение номера строки и контекста
    line_number = lines[0]["line_number"]
    line = lines[0]["line"]
    
    # Разбиение кода на строки
    code_lines = contract_code.split('\n')
    
    # Генерация патча в зависимости от типа уязвимости
    if vuln_name == "Reentrancy Vulnerability":
        # Добавление мьютекса для защиты от reentrancy
        if line_number > 0 and line_number <= len(code_lines):
            original_line = code_lines[line_number - 1]
            indentation = re.match(r"^\s*", original_line).group(0)
            
            # Поиск имени функции
            function_match = re.search(r"function\s+(\w+)", '\n'.join(code_lines[:line_number]))
            function_name = function_match.group(1) if function_match else "withdraw"
            
            # Создание патча
            patch = f"""// DEP Security Patch: Защита от reentrancy атаки
// Добавьте переменную состояния в начало контракта:
// bool private _mutex;

// Замените функцию {function_name} на следующую:
function {function_name}(uint256 amount) public {{
{indentation}require(!_mutex, "ReentrancyGuard: reentrant call");
{indentation}_mutex = true;
{indentation}
{indentation}require(balances[msg.sender] >= amount, "Insufficient balance");
{indentation}
{indentation}// Обновление баланса перед внешним вызовом (паттерн Checks-Effects-Interactions)
{indentation}balances[msg.sender] -= amount;
{indentation}
{indentation}// Внешний вызов
{indentation}(bool success, ) = msg.sender.call{{value: amount}}("");
{indentation}require(success, "Transfer failed");
{indentation}
{indentation}_mutex = false;
}}"""
            
            return patch
    
    elif vuln_name == "Integer Overflow":
        # Использование SafeMath
        patch = """// DEP Security Patch: Защита от переполнения целочисленных типов
// Добавьте библиотеку SafeMath в начало контракта:
// import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// Добавьте использование SafeMath для uint256:
// using SafeMath for uint256;

// Замените операции сложения и вычитания на безопасные:
// balances[msg.sender] = balances[msg.sender].add(msg.value);
// balances[msg.sender] = balances[msg.sender].sub(amount);"""
        
        return patch
    
    elif vuln_name == "tx.origin Authentication":
        # Замена tx.origin на msg.sender
        if line_number > 0 and line_number <= len(code_lines):
            original_line = code_lines[line_number - 1]
            patched_line = original_line.replace("tx.origin", "msg.sender")
            
            patch = f"""// DEP Security Patch: Замена tx.origin на msg.sender
// Оригинальная строка:
// {original_line.strip()}

// Исправленная строка:
// {patched_line.strip()}

// tx.origin небезопасно использовать для аутентификации, так как это может привести к фишинговым атакам.
// msg.sender всегда ссылается на непосредственного отправителя транзакции, что более безопасно."""
            
            return patch
    
    elif vuln_name == "Unchecked Return Value":
        # Добавление проверки возвращаемого значения
        if line_number > 0 and line_number <= len(code_lines):
            original_line = code_lines[line_number - 1]
            indentation = re.match(r"^\s*", original_line).group(0)
            
            patch = f"""// DEP Security Patch: Добавление проверки возвращаемого значения
// Оригинальная строка:
// {original_line.strip()}

// Исправленная строка:
{indentation}(bool success, ) = target.call(data);
{indentation}require(success, "External call failed");

// Всегда проверяйте возвращаемые значения низкоуровневых вызовов с помощью require()."""
            
            return patch
    
    elif vuln_name == "Unsecured Self-Destruct":
        # Добавление дополнительных проверок перед selfdestruct
        if line_number > 0 and line_number <= len(code_lines):
            original_line = code_lines[line_number - 1]
            indentation = re.match(r"^\s*", original_line).group(0)
            
            patch = f"""// DEP Security Patch: Добавление дополнительных проверок перед selfdestruct
// Оригинальная строка:
// {original_line.strip()}

// Исправленная строка:
{indentation}require(msg.sender == owner, "Only owner can destroy the contract");
{indentation}require(address(this).balance == 0, "Contract still has funds");
{indentation}selfdestruct(payable(owner));

// Добавьте также двухфакторную аутентификацию или временную задержку для критических операций."""
            
            return patch
    
    # Общий случай
    return f"""// DEP Security Patch: Рекомендации по исправлению уязвимости "{vuln_name}"
// Проблемная строка (строка {line_number}):
// {line}

// Рекомендации:
// 1. Внимательно проанализируйте код на наличие уязвимостей.
// 2. Следуйте лучшим практикам безопасности смарт-контрактов.
// 3. Рассмотрите возможность использования проверенных библиотек, таких как OpenZeppelin.
// 4. Проведите аудит безопасности перед деплоем в основную сеть."""

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Мост между TypeScript и Python-моделью для аудита смарт-контрактов')
    parser.add_argument('--action', choices=['audit', 'test', 'patch'], required=True, help='Действие')
    parser.add_argument('--contract-path', required=True, help='Путь к файлу контракта')
    parser.add_argument('--vulnerability', help='Путь к файлу с информацией о уязвимости (для патча)')
    
    args = parser.parse_args()
    
    if args.action == 'audit':
        # Аудит контракта
        result = audit_contract(args.contract_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'test':
        # Генерация тест-кейсов
        contract_code = read_contract(args.contract_path)
        if contract_code:
            test_cases = generate_test_cases(contract_code)
            print(json.dumps(test_cases, ensure_ascii=False, indent=2))
        else:
            print(json.dumps([], ensure_ascii=False, indent=2))
    
    elif args.action == 'patch':
        # Генерация патча
        contract_code = read_contract(args.contract_path)
        if not contract_code:
            print("// Не удалось прочитать контракт")
            return
        
        if not args.vulnerability:
            print("// Не указан путь к файлу с информацией о уязвимости")
            return
        
        try:
            with open(args.vulnerability, 'r', encoding='utf-8') as f:
                vulnerability = json.load(f)
            
            patch = generate_patch(contract_code, vulnerability)
            print(patch)
        except Exception as e:
            print(f"// Ошибка при генерации патча: {e}")

if __name__ == "__main__":
    main()
