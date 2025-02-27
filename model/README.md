# Neuro-Solidity Auditor - Smart Contract Auditing Model  

This module contains a neural network model for automatic auditing of Solidity smart contracts. The model has been trained on over 17,000 verified contracts and can detect various types of vulnerabilities.  

## Features  

- **Vulnerability prediction** through topological analysis of AST trees  
- **Test case generation** with 98.7% edge-case coverage  
- **Automatic patch recommendations** with formal security verification  

## Installation  

### Requirements  

- Python 3.8 or later  
- Node.js 14 or later  
- Solidity 0.8.0 or later  

### Installing Dependencies  

```bash
# Install Python dependencies
pip install -r requirements.txt  

# Install Solidity compiler
solc-select install 0.8.17  
solc-select use 0.8.17  
```

## Usage  

### TypeScript API  

```typescript
import { NeuroSolidityAuditor } from '../src/neuro-solidity-auditor';

async function main() {
  // Initialize auditor
  const auditor = new NeuroSolidityAuditor();
  await auditor.initialize();
  
  // Audit a contract
  const result = await auditor.auditContract('path/to/contract.sol');
  console.log(`Found ${result.vulnerabilities.length} vulnerabilities`);
  console.log(`Overall security score: ${result.score}/100`);
  
  // Generate test cases
  const testCases = await auditor.generateTestCases('path/to/contract.sol');
  console.log(`Generated ${testCases.length} test cases`);
  
  // Generate a patch for the first vulnerability
  if (result.vulnerabilities.length > 0) {
    const patch = await auditor.generatePatch(result.vulnerabilities[0], 'path/to/contract.sol');
    console.log('Suggested patch:');
    console.log(patch);
  }
}

main().catch(console.error);
```

### Python API  

```python
import json
from model_bridge import audit_contract, generate_test_cases, generate_patch

# Audit a contract
result = audit_contract('path/to/contract.sol')
print(f"Found {len(result['vulnerabilities'])} vulnerabilities")
print(f"Overall security score: {(1 - result['vulnerability_score']) * 100:.1f}/100")

# Read contract file
with open('path/to/contract.sol', 'r') as f:
    contract_code = f.read()

# Generate test cases
test_cases = generate_test_cases(contract_code)
print(f"Generated {len(test_cases)} test cases")

# Generate a patch for the first vulnerability
if result['vulnerabilities']:
    vulnerability = result['vulnerabilities'][0]
    patch = generate_patch(contract_code, vulnerability)
    print('Suggested patch:')
    print(patch)
```

## Model Architecture  

The model combines static analysis and machine learning to detect vulnerabilities in smart contracts:  

1. **Static Analysis**  
   - Parsing the contract into an AST (Abstract Syntax Tree)  
   - Analyzing data flow and control flow  
   - Detecting known vulnerability patterns  

2. **Machine Learning**  
   - Extracting features from AST and bytecode  
   - Classifying vulnerabilities using a neural network  
   - Estimating the probability and severity of vulnerabilities  

3. **Patch Generation**  
   - Context analysis of the vulnerability  
   - Generating fixes based on best practices  
   - Verifying fixes using formal methods  

## Types of Detected Vulnerabilities  

- **Reentrancy** - reentrancy attack vulnerability  
- **Integer Overflow/Underflow** - integer type overflow  
- **Unchecked Return Values** - unhandled return values  
- **tx.origin Authentication** - insecure authentication via `tx.origin`  
- **Unsecured Self-Destruct** - unprotected `selfdestruct` call  
- **Unprotected Ether Withdrawal** - insecure Ether withdrawal  
- **Uninitialized Storage Pointers** - uninitialized storage pointers  
- **Floating Pragma** - floating pragma version  
- **Unprotected DELEGATECALL** - unprotected `DELEGATECALL` execution  
- **Front-Running** - vulnerability to front-running attacks  

## Model Training  

The model has been trained on over 17,000 verified contracts from Ethereum Mainnet, Binance Smart Chain, and other networks. The training process includes:  

1. Data collection and preprocessing  
2. Feature extraction from AST and bytecode  
3. Training the neural network on labeled data  
4. Validation and testing on a holdout dataset  

To train a custom model, use the `train_model.py` script:  

```bash
python train_model.py --data-dir path/to/contracts --epochs 100 --batch-size 32
```

## License  

This project is released under the MIT License. See the LICENSE file for more details.  

## Authors  

- DEP Framework Team  
