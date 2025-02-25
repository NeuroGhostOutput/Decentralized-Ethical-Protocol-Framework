// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DrainContract
 * @dev Пример контракта с потенциальными уязвимостями для демонстрации работы DEP Framework
 */
contract DrainContract {
    address public owner;
    bool private locked;
    mapping(address => uint256) public balances;
    
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(tx.origin == owner, "Not authorized");
        _;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        
        // Потенциальная уязвимость reentrancy
        (bool success, ) = msg.sender.call{value: amount}("");
        
        emit Withdrawal(msg.sender, amount);
    }
    
    function drainFunds() public onlyOwner {
        // Потенциально вредоносная функция
        payable(owner).transfer(address(this).balance);
    }
    
    function stealUserFunds(address user) public onlyOwner {
        // Еще одна потенциально вредоносная функция
        uint256 amount = balances[user];
        balances[user] = 0;
        payable(owner).transfer(amount);
    }
    
    function hackBalances(address[] memory users, uint256 amount) public onlyOwner {
        // Манипуляция с балансами
        for (uint i = 0; i < users.length; i++) {
            balances[users[i]] = amount;
        }
    }
    
    function exploitOverflow(uint8 x, uint8 y) public pure returns (uint8) {
        // Потенциальное переполнение (в Solidity 0.8.0+ есть встроенная защита)
        return x + y;
    }
    
    function selfDestruct() public onlyOwner {
        // Небезопасное самоуничтожение контракта
        selfdestruct(payable(owner));
    }
}
