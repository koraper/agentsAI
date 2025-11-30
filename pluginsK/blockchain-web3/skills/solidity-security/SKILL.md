---
name: solidity-security
description: 마스터 smart 계약 security 최선의 관행 에 prevent 일반적인 취약점 및 implement secure Solidity 패턴. Use 때 작성 smart 계약, 감사 기존 계약, 또는 implementing security 측정합니다 위한 blockchain 애플리케이션.
---

# Solidity Security

마스터 smart 계약 security 최선의 관행, 취약점 방지, 및 secure Solidity 개발 패턴.

## 때 에 Use This Skill

- 작성 secure smart 계약
- 감사 기존 계약 위한 취약점
- Implementing secure DeFi 프로토콜
- Preventing reentrancy, overflow, 및 access control 이슈
- Optimizing gas usage 동안 maintaining security
- Preparing 계약 위한 프로페셔널 감사합니다
- Understanding 일반적인 공격 vectors

## 긴급 취약점

### 1. Reentrancy
Attacker calls back into your 계약 이전 상태 is 업데이트된.

**Vulnerable 코드:**
```solidity
// VULNERABLE TO REENTRANCY
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];

        // DANGER: External call before state update
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);

        balances[msg.sender] = 0;  // Too late!
    }
}
```

**Secure 패턴 (확인합니다-Effects-Interactions):**
```solidity
contract SecureBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        // EFFECTS: Update state BEFORE external call
        balances[msg.sender] = 0;

        // INTERACTIONS: External call last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

**Alternative: ReentrancyGuard**
```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 2. 정수 Overflow/Underflow

**Vulnerable 코드 (Solidity < 0.8.0):**
```solidity
// VULNERABLE
contract VulnerableToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // No overflow check - can wrap around
        balances[msg.sender] -= amount;  // Can underflow!
        balances[to] += amount;          // Can overflow!
    }
}
```

**Secure 패턴 (Solidity >= 0.8.0):**
```solidity
// Solidity 0.8+ has built-in overflow/underflow checks
contract SecureToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // Automatically reverts on overflow/underflow
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

**위한 Solidity < 0.8.0, use SafeMath:**
```solidity
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SecureToken {
    using SafeMath for uint256;
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[to] = balances[to].add(amount);
    }
}
```

### 3. Access Control

**Vulnerable 코드:**
```solidity
// VULNERABLE: Anyone can call critical functions
contract VulnerableContract {
    address public owner;

    function withdraw(uint256 amount) public {
        // No access control!
        payable(msg.sender).transfer(amount);
    }
}
```

**Secure 패턴:**
```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is Ownable {
    function withdraw(uint256 amount) public onlyOwner {
        payable(owner()).transfer(amount);
    }
}

// Or implement custom role-based access
contract RoleBasedContract {
    mapping(address => bool) public admins;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Not an admin");
        _;
    }

    function criticalFunction() public onlyAdmin {
        // Protected function
    }
}
```

### 4. Front-실행 중

**Vulnerable:**
```solidity
// VULNERABLE TO FRONT-RUNNING
contract VulnerableDEX {
    function swap(uint256 amount, uint256 minOutput) public {
        // Attacker sees this in mempool and front-runs
        uint256 output = calculateOutput(amount);
        require(output >= minOutput, "Slippage too high");
        // Perform swap
    }
}
```

**Mitigation:**
```solidity
contract SecureDEX {
    mapping(bytes32 => bool) public usedCommitments;

    // Step 1: Commit to trade
    function commitTrade(bytes32 commitment) public {
        usedCommitments[commitment] = true;
    }

    // Step 2: Reveal trade (next block)
    function revealTrade(
        uint256 amount,
        uint256 minOutput,
        bytes32 secret
    ) public {
        bytes32 commitment = keccak256(abi.encodePacked(
            msg.sender, amount, minOutput, secret
        ));
        require(usedCommitments[commitment], "Invalid commitment");
        // Perform swap
    }
}
```

## Security 최선의 관행

### 확인합니다-Effects-Interactions 패턴
```solidity
contract SecurePattern {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) public {
        // 1. CHECKS: Validate conditions
        require(amount <= balances[msg.sender], "Insufficient balance");
        require(amount > 0, "Amount must be positive");

        // 2. EFFECTS: Update state
        balances[msg.sender] -= amount;

        // 3. INTERACTIONS: External calls last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### Pull Over Push 패턴
```solidity
// Prefer this (pull)
contract SecurePayment {
    mapping(address => uint256) public pendingWithdrawals;

    function recordPayment(address recipient, uint256 amount) internal {
        pendingWithdrawals[recipient] += amount;
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to withdraw");

        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}

// Over this (push)
contract RiskyPayment {
    function distributePayments(address[] memory recipients, uint256[] memory amounts) public {
        for (uint i = 0; i < recipients.length; i++) {
            // If any transfer fails, entire batch fails
            payable(recipients[i]).transfer(amounts[i]);
        }
    }
}
```

### 입력 검증
```solidity
contract SecureContract {
    function transfer(address to, uint256 amount) public {
        // Validate inputs
        require(to != address(0), "Invalid recipient");
        require(to != address(this), "Cannot send to contract");
        require(amount > 0, "Amount must be positive");
        require(amount <= balances[msg.sender], "Insufficient balance");

        // Proceed with transfer
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### Emergency Stop (회로 Breaker)
```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyStop is Pausable, Ownable {
    function criticalFunction() public whenNotPaused {
        // Function logic
    }

    function emergencyStop() public onlyOwner {
        _pause();
    }

    function resume() public onlyOwner {
        _unpause();
    }
}
```

## Gas 최적화

### Use `uint256` Instead of Smaller 유형
```solidity
// More gas efficient
contract GasEfficient {
    uint256 public value;  // Optimal

    function set(uint256 _value) public {
        value = _value;
    }
}

// Less efficient
contract GasInefficient {
    uint8 public value;  // Still uses 256-bit slot

    function set(uint8 _value) public {
        value = _value;  // Extra gas for type conversion
    }
}
```

### Pack 스토리지 변수
```solidity
// Gas efficient (3 variables in 1 slot)
contract PackedStorage {
    uint128 public a;  // Slot 0
    uint64 public b;   // Slot 0
    uint64 public c;   // Slot 0
    uint256 public d;  // Slot 1
}

// Gas inefficient (each variable in separate slot)
contract UnpackedStorage {
    uint256 public a;  // Slot 0
    uint256 public b;  // Slot 1
    uint256 public c;  // Slot 2
    uint256 public d;  // Slot 3
}
```

### Use `calldata` Instead of `memory` 위한 함수 인수
```solidity
contract GasOptimized {
    // More gas efficient
    function processData(uint256[] calldata data) public pure returns (uint256) {
        return data[0];
    }

    // Less efficient
    function processDataMemory(uint256[] memory data) public pure returns (uint256) {
        return data[0];
    }
}
```

### Use 이벤트 위한 데이터 스토리지 (때 적절한)
```solidity
contract EventStorage {
    // Emitting events is cheaper than storage
    event DataStored(address indexed user, uint256 indexed id, bytes data);

    function storeData(uint256 id, bytes calldata data) public {
        emit DataStored(msg.sender, id, data);
        // Don't store in contract storage unless needed
    }
}
```

## 일반적인 취약점 Checklist

```solidity
// Security Checklist Contract
contract SecurityChecklist {
    /**
     * [ ] Reentrancy protection (ReentrancyGuard or CEI pattern)
     * [ ] Integer overflow/underflow (Solidity 0.8+ or SafeMath)
     * [ ] Access control (Ownable, roles, modifiers)
     * [ ] Input validation (require statements)
     * [ ] Front-running mitigation (commit-reveal if applicable)
     * [ ] Gas optimization (packed storage, calldata)
     * [ ] Emergency stop mechanism (Pausable)
     * [ ] Pull over push pattern for payments
     * [ ] No delegatecall to untrusted contracts
     * [ ] No tx.origin for authentication (use msg.sender)
     * [ ] Proper event emission
     * [ ] External calls at end of function
     * [ ] Check return values of external calls
     * [ ] No hardcoded addresses
     * [ ] Upgrade mechanism (if proxy pattern)
     */
}
```

## 테스트 위한 Security

```javascript
// Hardhat test example
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function () {
    it("Should prevent reentrancy attack", async function () {
        const [attacker] = await ethers.getSigners();

        const VictimBank = await ethers.getContractFactory("SecureBank");
        const bank = await VictimBank.deploy();

        const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
        const attackerContract = await Attacker.deploy(bank.address);

        // Deposit funds
        await bank.deposit({value: ethers.utils.parseEther("10")});

        // Attempt reentrancy attack
        await expect(
            attackerContract.attack({value: ethers.utils.parseEther("1")})
        ).to.be.revertedWith("ReentrancyGuard: reentrant call");
    });

    it("Should prevent integer overflow", async function () {
        const Token = await ethers.getContractFactory("SecureToken");
        const token = await Token.deploy();

        // Attempt overflow
        await expect(
            token.transfer(attacker.address, ethers.constants.MaxUint256)
        ).to.be.reverted;
    });

    it("Should enforce access control", async function () {
        const [owner, attacker] = await ethers.getSigners();

        const Contract = await ethers.getContractFactory("SecureContract");
        const contract = await Contract.deploy();

        // Attempt unauthorized withdrawal
        await expect(
            contract.connect(attacker).withdraw(100)
        ).to.be.revertedWith("Ownable: caller is not the owner");
    });
});
```

## Audit 준비

```solidity
contract WellDocumentedContract {
    /**
     * @title Well Documented Contract
     * @dev Example of proper documentation for audits
     * @notice This contract handles user deposits and withdrawals
     */

    /// @notice Mapping of user balances
    mapping(address => uint256) public balances;

    /**
     * @dev Deposits ETH into the contract
     * @notice Anyone can deposit funds
     */
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    /**
     * @dev Withdraws user's balance
     * @notice Follows CEI pattern to prevent reentrancy
     * @param amount Amount to withdraw in wei
     */
    function withdraw(uint256 amount) public {
        // CHECKS
        require(amount <= balances[msg.sender], "Insufficient balance");

        // EFFECTS
        balances[msg.sender] -= amount;

        // INTERACTIONS
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## 리소스

- **참조/reentrancy.md**: 포괄적인 reentrancy 방지
- **참조/access-control.md**: Role-based access 패턴
- **참조/overflow-underflow.md**: SafeMath 및 정수 safety
- **참조/gas-최적화.md**: Gas 저장하는 techniques
- **참조/취약점-패턴.md**: 일반적인 취약점 카탈로그
- **자산/solidity-계약-템플릿.sol**: Secure 계약 템플릿
- **자산/security-checklist.md**: Pre-audit checklist
- **스크립트/analyze-계약.sh**: 정적 분석 tools

## Tools 위한 Security 분석

- **Slither**: 정적 분석 tool
- **Mythril**: Security 분석 tool
- **Echidna**: Fuzzing tool
- **Manticore**: Symbolic 실행
- **Securify**: 자동화된 security scanner

## 일반적인 Pitfalls

1. **사용하여 `tx.origin` 위한 인증**: Use `msg.sender` instead
2. **Unchecked 외부 Calls**: 항상 check 반환 값
3. **Delegatecall 에 Untrusted 계약**: Can hijack your 계약
4. **Floating Pragma**: Pin 에 특정 Solidity 버전
5. **Missing 이벤트**: Emit 이벤트 위한 상태 변경합니다
6. **과도한 Gas 에서 루프합니다**: Can hit block gas limit
7. **아니요 업그레이드 경로**: Consider 프록시 패턴 만약 업그레이드합니다 필요한
