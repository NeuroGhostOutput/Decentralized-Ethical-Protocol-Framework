# DEP Framework Usage Guide

## Contents

1. [Installation](#installation)
2. [Setup](#setup)
3. [Using Neuro-Solidity Auditor](#using-neuro-solidity-auditor)
4. [Using Proof-of-Humanism](#using-proof-of-humanism)
5. [Using Ethical Mirror Engine](#using-ethical-mirror-engine)
6. [Usage Examples](#usage-examples)
7. [Frequently Asked Questions](#frequently-asked-questions)

## Installation

### Requirements

- Node.js 16.x or later
- npm 8.x or later
- TypeScript 4.5.x or later
- Solana CLI (optional, for working with Solana blockchain)

### Installation via npm

```bash
npm install dep-framework
```

### Installation from Source Code

```bash
# Clone the repository
git clone https://github.com/dep-framework/dep-framework.git
cd dep-framework

# Install dependencies
npm install

# Build the project
npm run build
```

## Setup

### Environment Variable Configuration

Copy the `.env.example` file to `.env` and fill in the required values:

```bash
cp .env.example .env
```

Example `.env` file:

```
# Solana Settings
SOLANA_NETWORK=devnet
SOLANA_RPC_URL=https://api.devnet.solana.com

# API Keys
ETHERSCAN_API_KEY=your_etherscan_api_key_here
SOLSCAN_API_KEY=your_solscan_api_key_here

# NeuroSolidityAuditor Settings
MODEL_PATH=./models/neuro_auditor_model
CONTRACTS_DB_PATH=./data/verified_contracts

# ProofOfHumanism Settings
ETHICAL_THRESHOLD=75
DAO_CONTRACT_ADDRESS=your_dao_contract_address_here
```

### Initializing the Framework

```typescript
import { DEPFramework } from 'dep-framework';

// Create an instance of the framework
const framework = new DEPFramework();

// Initialize and start the framework
await framework.start();

// Get framework components
const neuroAuditor = framework.getNeuroAuditor();
const proofOfHumanism = framework.getProofOfHumanism();
const ethicalMirror = framework.getEthicalMirror();
```

## Using Neuro-Solidity Auditor

### Auditing a Smart Contract

```typescript
import { NeuroSolidityAuditor } from 'dep-framework';

// Create an instance of the auditor
const auditor = new NeuroSolidityAuditor();
await auditor.initialize();

// Path to the contract file
const contractPath = './contracts/MyContract.sol';

// Perform an audit
const auditResult = await auditor.auditContract(contractPath);

// Output results
console.log(`Security Score: ${auditResult.score}/100`);
console.log(`Vulnerabilities Found: ${auditResult.vulnerabilities.length}`);
```

### Generating Test Cases

```typescript
// Generate test cases for the contract
const testCases = await auditor.generateTestCases(contractPath);

// Output test cases
for (const test of testCases) {
  console.log(`Test: ${test.description}`);
  console.log(`Inputs: ${JSON.stringify(test.inputs)}`);
  console.log(`Expected Outputs: ${JSON.stringify(test.expectedOutputs)}`);
}
```

## Using Proof-of-Humanism

### Transaction Validation

```typescript
import { ProofOfHumanism } from 'dep-framework';
import * as web3 from '@solana/web3.js';

// Create an instance of ProofOfHumanism
const poh = new ProofOfHumanism();
await poh.initialize();

// Create a Solana transaction
const transaction = new web3.Transaction().add(
  web3.SystemProgram.transfer({
    fromPubkey: new web3.PublicKey('senderPublicKey'),
    toPubkey: new web3.PublicKey('recipientPublicKey'),
    lamports: 1000000000,
  })
);

// Validate the transaction
const validationResult = poh.validateTransaction(transaction);

console.log(`Ethical Score: ${validationResult.ethicalScore}/100`);
console.log(`Validation Result: ${validationResult.validationResult ? 'ACCEPTED' : 'REJECTED'}`);
```

## Using Ethical Mirror Engine

### Code Ethics Analysis

```typescript
import { EthicalMirrorEngine } from 'dep-framework';
import * as fs from 'fs';

// Create an instance of EthicalMirrorEngine
const mirror = new EthicalMirrorEngine();
await mirror.initialize();

// Read contract code
const contractPath = './contracts/MyContract.sol';
const contractCode = fs.readFileSync(contractPath, 'utf-8');

// Analyze ethics of the code
const ethicsAnalysis = mirror.analyzeEthics(contractCode);

console.log(`Ethical Score: ${ethicsAnalysis.ethicalScore}/100`);
console.log(`Issues Found: ${ethicsAnalysis.issues.length}`);
```

### Creating an Ethical Twin of the Code

```typescript
// Generate an ethical twin of the contract code
const transformResult = mirror.ethicalMirror(contractCode);

console.log(`Transformations Applied: ${transformResult.transformations.length}`);

// Save transformed code
const outputPath = './contracts/EthicalMyContract.sol';
mirror.saveTransformedCode(transformResult, outputPath);
```

## Usage Examples

Examples of DEP Framework usage can be found in the `examples/` directory:

- `demo.ts` - Demonstration of the framework's core features
- `DrainContract.sol` - Example of a vulnerable contract for testing

Run the demonstration example:

```bash
npm run example
```

## Frequently Asked Questions

### How do I update the neural network model?

The neural network model for the Neuro-Solidity Auditor is stored in the directory specified by the `MODEL_PATH` environment variable. To update the model, replace the files in this directory with the new model.

### How do I configure the ethical threshold?

The ethical threshold for Proof-of-Humanism can be set through DAO voting or directly via the `updateEthicalThreshold()` method.

### How do I integrate DEP Framework into an existing project?

DEP Framework can be integrated into an existing project via the npm package or directly from the source code. For CI/CD pipeline integration, the framework’s CLI interface can be used.

