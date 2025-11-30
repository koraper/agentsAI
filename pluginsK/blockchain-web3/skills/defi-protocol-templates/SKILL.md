---
name: defi-protocol-templates
description: Implement DeFi 프로토콜 와 함께 프로덕션 준비 완료 템플릿 위한 staking, AMMs, governance, 및 lending 시스템. Use 때 구축 분산된 finance 애플리케이션 또는 smart 계약 프로토콜.
---

# DeFi 프로토콜 템플릿

프로덕션 준비 완료 템플릿 위한 일반적인 DeFi 프로토콜 포함하여 staking, AMMs, governance, lending, 및 flash loans.

## 때 에 Use This Skill

- 구축 staking 플랫폼 와 함께 reward 배포
- Implementing AMM (자동화된 Market Maker) 프로토콜
- 생성하는 governance 토큰 시스템
- Developing lending/borrowing 프로토콜
- Integrating flash loan 기능
- 시작하는 yield farming 플랫폼

## Staking 계약

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract StakingRewards is ReentrancyGuard, Ownable {
    IERC20 public stakingToken;
    IERC20 public rewardsToken;

    uint256 public rewardRate = 100; // Rewards per second
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;

    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;
    mapping(address => uint256) public balances;

    uint256 private _totalSupply;

    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);

    constructor(address _stakingToken, address _rewardsToken) {
        stakingToken = IERC20(_stakingToken);
        rewardsToken = IERC20(_rewardsToken);
    }

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;

        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    function rewardPerToken() public view returns (uint256) {
        if (_totalSupply == 0) {
            return rewardPerTokenStored;
        }
        return rewardPerTokenStored +
            ((block.timestamp - lastUpdateTime) * rewardRate * 1e18) / _totalSupply;
    }

    function earned(address account) public view returns (uint256) {
        return (balances[account] *
            (rewardPerToken() - userRewardPerTokenPaid[account])) / 1e18 +
            rewards[account];
    }

    function stake(uint256 amount) external nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot stake 0");
        _totalSupply += amount;
        balances[msg.sender] += amount;
        stakingToken.transferFrom(msg.sender, address(this), amount);
        emit Staked(msg.sender, amount);
    }

    function withdraw(uint256 amount) public nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot withdraw 0");
        _totalSupply -= amount;
        balances[msg.sender] -= amount;
        stakingToken.transfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }

    function getReward() public nonReentrant updateReward(msg.sender) {
        uint256 reward = rewards[msg.sender];
        if (reward > 0) {
            rewards[msg.sender] = 0;
            rewardsToken.transfer(msg.sender, reward);
            emit RewardPaid(msg.sender, reward);
        }
    }

    function exit() external {
        withdraw(balances[msg.sender]);
        getReward();
    }
}
```

## AMM (자동화된 Market Maker)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SimpleAMM {
    IERC20 public token0;
    IERC20 public token1;

    uint256 public reserve0;
    uint256 public reserve1;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);
    event Swap(address indexed trader, uint256 amount0In, uint256 amount1In, uint256 amount0Out, uint256 amount1Out);

    constructor(address _token0, address _token1) {
        token0 = IERC20(_token0);
        token1 = IERC20(_token1);
    }

    function addLiquidity(uint256 amount0, uint256 amount1) external returns (uint256 shares) {
        token0.transferFrom(msg.sender, address(this), amount0);
        token1.transferFrom(msg.sender, address(this), amount1);

        if (totalSupply == 0) {
            shares = sqrt(amount0 * amount1);
        } else {
            shares = min(
                (amount0 * totalSupply) / reserve0,
                (amount1 * totalSupply) / reserve1
            );
        }

        require(shares > 0, "Shares = 0");
        _mint(msg.sender, shares);
        _update(
            token0.balanceOf(address(this)),
            token1.balanceOf(address(this))
        );

        emit Mint(msg.sender, shares);
    }

    function removeLiquidity(uint256 shares) external returns (uint256 amount0, uint256 amount1) {
        uint256 bal0 = token0.balanceOf(address(this));
        uint256 bal1 = token1.balanceOf(address(this));

        amount0 = (shares * bal0) / totalSupply;
        amount1 = (shares * bal1) / totalSupply;

        require(amount0 > 0 && amount1 > 0, "Amount0 or amount1 = 0");

        _burn(msg.sender, shares);
        _update(bal0 - amount0, bal1 - amount1);

        token0.transfer(msg.sender, amount0);
        token1.transfer(msg.sender, amount1);

        emit Burn(msg.sender, shares);
    }

    function swap(address tokenIn, uint256 amountIn) external returns (uint256 amountOut) {
        require(tokenIn == address(token0) || tokenIn == address(token1), "Invalid token");

        bool isToken0 = tokenIn == address(token0);
        (IERC20 tokenIn_, IERC20 tokenOut, uint256 resIn, uint256 resOut) = isToken0
            ? (token0, token1, reserve0, reserve1)
            : (token1, token0, reserve1, reserve0);

        tokenIn_.transferFrom(msg.sender, address(this), amountIn);

        // 0.3% fee
        uint256 amountInWithFee = (amountIn * 997) / 1000;
        amountOut = (resOut * amountInWithFee) / (resIn + amountInWithFee);

        tokenOut.transfer(msg.sender, amountOut);

        _update(
            token0.balanceOf(address(this)),
            token1.balanceOf(address(this))
        );

        emit Swap(msg.sender, isToken0 ? amountIn : 0, isToken0 ? 0 : amountIn, isToken0 ? 0 : amountOut, isToken0 ? amountOut : 0);
    }

    function _mint(address to, uint256 amount) private {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function _burn(address from, uint256 amount) private {
        balanceOf[from] -= amount;
        totalSupply -= amount;
    }

    function _update(uint256 res0, uint256 res1) private {
        reserve0 = res0;
        reserve1 = res1;
    }

    function sqrt(uint256 y) private pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }

    function min(uint256 x, uint256 y) private pure returns (uint256) {
        return x <= y ? x : y;
    }
}
```

## Governance 토큰

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GovernanceToken is ERC20Votes, Ownable {
    constructor() ERC20("Governance Token", "GOV") ERC20Permit("Governance Token") {
        _mint(msg.sender, 1000000 * 10**decimals());
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20Votes) {
        super._afterTokenTransfer(from, to, amount);
    }

    function _mint(address to, uint256 amount) internal override(ERC20Votes) {
        super._mint(to, amount);
    }

    function _burn(address account, uint256 amount) internal override(ERC20Votes) {
        super._burn(account, amount);
    }
}

contract Governor is Ownable {
    GovernanceToken public governanceToken;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startBlock;
        uint256 endBlock;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;

    uint256 public votingPeriod = 17280; // ~3 days in blocks
    uint256 public proposalThreshold = 100000 * 10**18;

    event ProposalCreated(uint256 indexed proposalId, address proposer, string description);
    event VoteCast(address indexed voter, uint256 indexed proposalId, bool support, uint256 weight);
    event ProposalExecuted(uint256 indexed proposalId);

    constructor(address _governanceToken) {
        governanceToken = GovernanceToken(_governanceToken);
    }

    function propose(string memory description) external returns (uint256) {
        require(
            governanceToken.getPastVotes(msg.sender, block.number - 1) >= proposalThreshold,
            "Proposer votes below threshold"
        );

        proposalCount++;
        Proposal storage newProposal = proposals[proposalCount];
        newProposal.id = proposalCount;
        newProposal.proposer = msg.sender;
        newProposal.description = description;
        newProposal.startBlock = block.number;
        newProposal.endBlock = block.number + votingPeriod;

        emit ProposalCreated(proposalCount, msg.sender, description);
        return proposalCount;
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.number >= proposal.startBlock, "Voting not started");
        require(block.number <= proposal.endBlock, "Voting ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");

        uint256 weight = governanceToken.getPastVotes(msg.sender, proposal.startBlock);
        require(weight > 0, "No voting power");

        proposal.hasVoted[msg.sender] = true;

        if (support) {
            proposal.forVotes += weight;
        } else {
            proposal.againstVotes += weight;
        }

        emit VoteCast(msg.sender, proposalId, support, weight);
    }

    function execute(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.number > proposal.endBlock, "Voting not ended");
        require(!proposal.executed, "Already executed");
        require(proposal.forVotes > proposal.againstVotes, "Proposal failed");

        proposal.executed = true;

        // Execute proposal logic here

        emit ProposalExecuted(proposalId);
    }
}
```

## Flash Loan

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IFlashLoanReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        bytes calldata params
    ) external returns (bool);
}

contract FlashLoanProvider {
    IERC20 public token;
    uint256 public feePercentage = 9; // 0.09% fee

    event FlashLoan(address indexed borrower, uint256 amount, uint256 fee);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function flashLoan(
        address receiver,
        uint256 amount,
        bytes calldata params
    ) external {
        uint256 balanceBefore = token.balanceOf(address(this));
        require(balanceBefore >= amount, "Insufficient liquidity");

        uint256 fee = (amount * feePercentage) / 10000;

        // Send tokens to receiver
        token.transfer(receiver, amount);

        // Execute callback
        require(
            IFlashLoanReceiver(receiver).executeOperation(
                address(token),
                amount,
                fee,
                params
            ),
            "Flash loan failed"
        );

        // Verify repayment
        uint256 balanceAfter = token.balanceOf(address(this));
        require(balanceAfter >= balanceBefore + fee, "Flash loan not repaid");

        emit FlashLoan(receiver, amount, fee);
    }
}

// Example flash loan receiver
contract FlashLoanReceiver is IFlashLoanReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        bytes calldata params
    ) external override returns (bool) {
        // Decode params and execute arbitrage, liquidation, etc.
        // ...

        // Approve repayment
        IERC20(asset).approve(msg.sender, amount + fee);

        return true;
    }
}
```

## 리소스

- **참조/staking.md**: Staking mechanics 및 reward 배포
- **참조/liquidity-풀링합니다.md**: AMM mathematics 및 pricing
- **참조/governance-토큰.md**: Governance 및 voting 시스템
- **참조/lending-프로토콜.md**: Lending/borrowing 구현
- **참조/flash-loans.md**: Flash loan security 및 use cases
- **자산/staking-계약.sol**: Production staking 템플릿
- **자산/amm-계약.sol**: 전체 AMM 구현
- **자산/governance-토큰.sol**: Governance 시스템
- **자산/lending-프로토콜.sol**: Lending 플랫폼 템플릿

## 최선의 관행

1. **Use 설정된 라이브러리**: OpenZeppelin, Solmate
2. **Test 철저히**: 단위 테스트합니다, 통합 테스트합니다, fuzzing
3. **Audit 이전 Launch**: 프로페셔널 security 감사합니다
4. **Start 간단한**: MVP 첫 번째, add 기능 점진적으로
5. **모니터**: Track 계약 health 및 사용자 activity
6. **Upgradability**: Consider 프록시 패턴 위한 업그레이드합니다
7. **Emergency 제어합니다**: Pause mechanisms 위한 긴급 이슈

## 일반적인 DeFi 패턴

- **시간-가중치가 부여된 평균 Price (TWAP)**: Price oracle resistance
- **Liquidity Mining**: Incentivize liquidity provision
- **Vesting**: 잠금 토큰 와 함께 gradual 릴리스
- **Multisig**: Require 여러 signatures 위한 긴급 작업
- **Timelocks**: Delay 실행 of governance decisions
