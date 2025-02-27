Вот ваш перевод:  

# Contribution Guide for DEP Framework  

Thank you for your interest in DEP Framework! We appreciate any contributions to the project, whether it’s fixing bugs, adding new features, or improving documentation.  

## Table of Contents  

1. [Code of Conduct](#code-of-conduct)  
2. [How to Contribute](#how-to-contribute)  
3. [Setting Up the Development Environment](#setting-up-the-development-environment)  
4. [Code Style](#code-style)  
5. [Testing](#testing)  
6. [Submitting Changes](#submitting-changes)  
7. [Review Process](#review-process)  
8. [Reporting Issues](#reporting-issues)  

## Code of Conduct  

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). By participating, you agree to abide by its terms.  

## How to Contribute  

1. Fork the repository  
2. Create a branch for your changes (`git checkout -b feature/amazing-feature`)  
3. Make your changes  
4. Ensure all tests pass (`npm test`)  
5. Commit your changes (`git commit -m 'Add some amazing feature'`)  
6. Push your changes to your fork (`git push origin feature/amazing-feature`)  
7. Create a Pull Request  

## Setting Up the Development Environment  

1. Clone the repository:  
   ```bash
   git clone https://github.com/dep-framework/dep-framework.git  
   cd dep-framework  
   ```  

2. Install dependencies:  
   ```bash
   npm install  
   ```  

3. Copy the `.env.example` file to `.env` and fill in the necessary values:  
   ```bash
   cp .env.example .env  
   ```  

4. Build the project:  
   ```bash
   npm run build  
   ```  

5. Run tests to verify everything works:  
   ```bash
   npm test  
   ```  

## Code Style  

We use ESLint and Prettier to maintain a consistent code style. Before submitting changes, ensure your code follows the style guide:  

```bash
npm run lint  
```  

Key style guidelines:  
- Use TypeScript for all new code  
- Follow SOLID, DRY, and KISS principles  
- Write documentation for public APIs  
- Use async/await instead of callbacks  
- Provide type definitions for all parameters and return values  

## Testing  

Every new feature or bug fix should include tests. We use Jest for testing:  

```bash
npm test  
```  

To run tests with coverage:  

```bash
npm test -- --coverage  
```  

## Submitting Changes  

1. Ensure your code follows the style guide and passes all tests  
2. Update documentation if needed  
3. Update `CHANGELOG.md` if your changes are significant  
4. Submit a Pull Request with a description of your changes  

## Review Process  

1. Project maintainers will review your Pull Request  
2. If any changes are required, they will be requested in comments  
3. Once all requested changes are made and approved, your Pull Request will be merged  

## Reporting Issues  

If you find a bug, please create an Issue with detailed information:  

1. Steps to reproduce the issue  
2. Expected behavior  
3. Actual behavior  
4. Screenshots, if applicable  
5. Environment details (OS, Node.js version, etc.)  

---  

Thank you for contributing to the DEP Framework!
