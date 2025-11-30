---
name: web3-testing
description: Test smart 계약 포괄적으로 사용하여 Hardhat 및 Foundry 와 함께 단위 테스트합니다, 통합 테스트합니다, 및 mainnet forking. Use 때 테스트 Solidity 계약, 설정하는 blockchain test suites, 또는 validating DeFi 프로토콜.
---

# Web3 Smart 계약 테스트

마스터 포괄적인 테스트 strategies 위한 smart 계약 사용하여 Hardhat, Foundry, 및 고급 테스트 패턴.

## 때 에 Use This Skill

- 작성 단위 테스트합니다 위한 smart 계약
- 설정하는 통합 test suites
- Performing gas 최적화 테스트
- Fuzzing 위한 엣지 cases
- Forking mainnet 위한 realistic 테스트
- Automating test coverage reporting
- Verifying 계약 에 Etherscan

## Hardhat 테스트 설정

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("@nomiclabs/hardhat-etherscan");
require("hardhat-gas-reporter");
require("solidity-coverage");

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      forking: {
        url: process.env.MAINNET_RPC_URL,
        blockNumber: 15000000
      }
    },
    goerli: {
      url: process.env.GOERLI_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  },
  gasReporter: {
    enabled: true,
    currency: 'USD',
    coinmarketcap: process.env.COINMARKETCAP_API_KEY
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

## 단위 테스트 패턴

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture, time } = require("@nomicfoundation/hardhat-network-helpers");

describe("Token Contract", function () {
  // Fixture for test setup
  async function deployTokenFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy();

    return { token, owner, addr1, addr2 };
  }

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      const { token, owner } = await loadFixture(deployTokenFixture);
      expect(await token.owner()).to.equal(owner.address);
    });

    it("Should assign total supply to owner", async function () {
      const { token, owner } = await loadFixture(deployTokenFixture);
      const ownerBalance = await token.balanceOf(owner.address);
      expect(await token.totalSupply()).to.equal(ownerBalance);
    });
  });

  describe("Transactions", function () {
    it("Should transfer tokens between accounts", async function () {
      const { token, owner, addr1 } = await loadFixture(deployTokenFixture);

      await expect(token.transfer(addr1.address, 50))
        .to.changeTokenBalances(token, [owner, addr1], [-50, 50]);
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      const { token, addr1 } = await loadFixture(deployTokenFixture);
      const initialBalance = await token.balanceOf(addr1.address);

      await expect(
        token.connect(addr1).transfer(owner.address, 1)
      ).to.be.revertedWith("Insufficient balance");
    });

    it("Should emit Transfer event", async function () {
      const { token, owner, addr1 } = await loadFixture(deployTokenFixture);

      await expect(token.transfer(addr1.address, 50))
        .to.emit(token, "Transfer")
        .withArgs(owner.address, addr1.address, 50);
    });
  });

  describe("Time-based tests", function () {
    it("Should handle time-locked operations", async function () {
      const { token } = await loadFixture(deployTokenFixture);

      // Increase time by 1 day
      await time.increase(86400);

      // Test time-dependent functionality
    });
  });

  describe("Gas optimization", function () {
    it("Should use gas efficiently", async function () {
      const { token } = await loadFixture(deployTokenFixture);

      const tx = await token.transfer(addr1.address, 100);
      const receipt = await tx.wait();

      expect(receipt.gasUsed).to.be.lessThan(50000);
    });
  });
});
```

## Foundry 테스트 (Forge)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/Token.sol";

contract TokenTest is Test {
    Token token;
    address owner = address(1);
    address user1 = address(2);
    address user2 = address(3);

    function setUp() public {
        vm.prank(owner);
        token = new Token();
    }

    function testInitialSupply() public {
        assertEq(token.totalSupply(), 1000000 * 10**18);
    }

    function testTransfer() public {
        vm.prank(owner);
        token.transfer(user1, 100);

        assertEq(token.balanceOf(user1), 100);
        assertEq(token.balanceOf(owner), token.totalSupply() - 100);
    }

    function testFailTransferInsufficientBalance() public {
        vm.prank(user1);
        token.transfer(user2, 100); // Should fail
    }

    function testCannotTransferToZeroAddress() public {
        vm.prank(owner);
        vm.expectRevert("Invalid recipient");
        token.transfer(address(0), 100);
    }

    // Fuzzing test
    function testFuzzTransfer(uint256 amount) public {
        vm.assume(amount > 0 && amount <= token.totalSupply());

        vm.prank(owner);
        token.transfer(user1, amount);

        assertEq(token.balanceOf(user1), amount);
    }

    // Test with cheatcodes
    function testDealAndPrank() public {
        // Give ETH to address
        vm.deal(user1, 10 ether);

        // Impersonate address
        vm.prank(user1);

        // Test functionality
        assertEq(user1.balance, 10 ether);
    }

    // Mainnet fork test
    function testForkMainnet() public {
        vm.createSelectFork("https://eth-mainnet.alchemyapi.io/v2/...");

        // Interact with mainnet contracts
        address dai = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
        assertEq(IERC20(dai).symbol(), "DAI");
    }
}
```

## 고급 테스트 패턴

### Snapshot 및 Revert
```javascript
describe("Complex State Changes", function () {
  let snapshotId;

  beforeEach(async function () {
    snapshotId = await network.provider.send("evm_snapshot");
  });

  afterEach(async function () {
    await network.provider.send("evm_revert", [snapshotId]);
  });

  it("Test 1", async function () {
    // Make state changes
  });

  it("Test 2", async function () {
    // State reverted, clean slate
  });
});
```

### Mainnet Forking
```javascript
describe("Mainnet Fork Tests", function () {
  let uniswapRouter, dai, usdc;

  before(async function () {
    await network.provider.request({
      method: "hardhat_reset",
      params: [{
        forking: {
          jsonRpcUrl: process.env.MAINNET_RPC_URL,
          blockNumber: 15000000
        }
      }]
    });

    // Connect to existing mainnet contracts
    uniswapRouter = await ethers.getContractAt(
      "IUniswapV2Router",
      "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    );

    dai = await ethers.getContractAt(
      "IERC20",
      "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    );
  });

  it("Should swap on Uniswap", async function () {
    // Test with real Uniswap contracts
  });
});
```

### Impersonating 계정
```javascript
it("Should impersonate whale account", async function () {
  const whaleAddress = "0x...";

  await network.provider.request({
    method: "hardhat_impersonateAccount",
    params: [whaleAddress]
  });

  const whale = await ethers.getSigner(whaleAddress);

  // Use whale's tokens
  await dai.connect(whale).transfer(addr1.address, ethers.utils.parseEther("1000"));
});
```

## Gas 최적화 테스트

```javascript
const { expect } = require("chai");

describe("Gas Optimization", function () {
  it("Compare gas usage between implementations", async function () {
    const Implementation1 = await ethers.getContractFactory("OptimizedContract");
    const Implementation2 = await ethers.getContractFactory("UnoptimizedContract");

    const contract1 = await Implementation1.deploy();
    const contract2 = await Implementation2.deploy();

    const tx1 = await contract1.doSomething();
    const receipt1 = await tx1.wait();

    const tx2 = await contract2.doSomething();
    const receipt2 = await tx2.wait();

    console.log("Optimized gas:", receipt1.gasUsed.toString());
    console.log("Unoptimized gas:", receipt2.gasUsed.toString());

    expect(receipt1.gasUsed).to.be.lessThan(receipt2.gasUsed);
  });
});
```

## Coverage Reporting

```bash
# Generate coverage report
npx hardhat coverage

# Output shows:
# File                | % Stmts | % Branch | % Funcs | % Lines |
# -------------------|---------|----------|---------|---------|
# contracts/Token.sol |   100   |   90     |   100   |   95    |
```

## 계약 확인

```javascript
// Verify on Etherscan
await hre.run("verify:verify", {
  address: contractAddress,
  constructorArguments: [arg1, arg2]
});
```

```bash
# Or via CLI
npx hardhat verify --network mainnet CONTRACT_ADDRESS "Constructor arg1" "arg2"
```

## CI/CD 통합

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'

      - run: npm install
      - run: npx hardhat compile
      - run: npx hardhat test
      - run: npx hardhat coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
```

## 리소스

- **참조/hardhat-설정.md**: Hardhat 구성 가이드
- **참조/foundry-설정.md**: Foundry 테스트 프레임워크
- **참조/test-패턴.md**: 테스트 최선의 관행
- **참조/mainnet-forking.md**: Fork 테스트 strategies
- **참조/계약-확인.md**: Etherscan 확인
- **자산/hardhat-config.js**: 완전한 Hardhat 구성
- **자산/test-suite.js**: 포괄적인 test 예제
- **자산/foundry.toml**: Foundry 구성
- **스크립트/test-계약.sh**: 자동화된 테스트 스크립트

## 최선의 관행

1. **Test Coverage**: Aim 위한 >90% coverage
2. **엣지 Cases**: Test 경계 conditions
3. **Gas 제한합니다**: Verify 함수 don't hit block gas limit
4. **Reentrancy**: Test 위한 reentrancy 취약점
5. **Access Control**: Test unauthorized access attempts
6. **이벤트**: Verify 이벤트 emissions
7. **Fixtures**: Use fixtures 에 avoid 코드 duplication
8. **Mainnet Fork**: Test 와 함께 real 계약
9. **Fuzzing**: Use 속성-based 테스트
10. **CI/CD**: Automate 테스트 에 모든 커밋
