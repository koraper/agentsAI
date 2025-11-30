---
name: nft-standards
description: Implement NFT 표준 (ERC-721, ERC-1155) 와 함께 적절한 메타데이터 처리, minting strategies, 및 marketplace 통합. Use 때 생성하는 NFT 계약, 구축 NFT marketplaces, 또는 implementing digital 자산 시스템.
---

# NFT 표준

마스터 ERC-721 및 ERC-1155 NFT 표준, 메타데이터 최선의 관행, 및 고급 NFT 기능.

## 때 에 Use This Skill

- 생성하는 NFT collections (art, gaming, collectibles)
- Implementing marketplace 기능
- 구축 에-chain 또는 꺼짐-chain 메타데이터
- 생성하는 soulbound 토큰 (non-transferable)
- Implementing royalties 및 revenue sharing
- Developing 동적/evolving NFTs

## ERC-721 (Non-Fungible 토큰 표준)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage, ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.08 ether;
    uint256 public constant MAX_PER_MINT = 20;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mint(uint256 quantity) external payable {
        require(quantity > 0 && quantity <= MAX_PER_MINT, "Invalid quantity");
        require(_tokenIds.current() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIds.increment();
            uint256 newTokenId = _tokenIds.current();
            _safeMint(msg.sender, newTokenId);
            _setTokenURI(newTokenId, generateTokenURI(newTokenId));
        }
    }

    function generateTokenURI(uint256 tokenId) internal pure returns (string memory) {
        // Return IPFS URI or on-chain metadata
        return string(abi.encodePacked("ipfs://QmHash/", Strings.toString(tokenId), ".json"));
    }

    // Required overrides
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

## ERC-1155 (Multi-토큰 표준)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant SWORD = 1;
    uint256 public constant SHIELD = 2;
    uint256 public constant POTION = 3;

    mapping(uint256 => uint256) public tokenSupply;
    mapping(uint256 => uint256) public maxSupply;

    constructor() ERC1155("ipfs://QmBaseHash/{id}.json") {
        maxSupply[SWORD] = 1000;
        maxSupply[SHIELD] = 500;
        maxSupply[POTION] = 10000;
    }

    function mint(
        address to,
        uint256 id,
        uint256 amount
    ) external onlyOwner {
        require(tokenSupply[id] + amount <= maxSupply[id], "Exceeds max supply");

        _mint(to, id, amount, "");
        tokenSupply[id] += amount;
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts
    ) external onlyOwner {
        for (uint256 i = 0; i < ids.length; i++) {
            require(tokenSupply[ids[i]] + amounts[i] <= maxSupply[ids[i]], "Exceeds max supply");
            tokenSupply[ids[i]] += amounts[i];
        }

        _mintBatch(to, ids, amounts, "");
    }

    function burn(
        address from,
        uint256 id,
        uint256 amount
    ) external {
        require(from == msg.sender || isApprovedForAll(from, msg.sender), "Not authorized");
        _burn(from, id, amount);
        tokenSupply[id] -= amount;
    }
}
```

## 메타데이터 표준

### 꺼짐-Chain 메타데이터 (IPFS)
```json
{
  "name": "NFT #1",
  "description": "Description of the NFT",
  "image": "ipfs://QmImageHash",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    },
    {
      "trait_type": "Power",
      "value": 95,
      "display_type": "number",
      "max_value": 100
    }
  ]
}
```

### 에-Chain 메타데이터
```solidity
contract OnChainNFT is ERC721 {
    struct Traits {
        uint8 background;
        uint8 body;
        uint8 head;
        uint8 rarity;
    }

    mapping(uint256 => Traits) public tokenTraits;

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        Traits memory traits = tokenTraits[tokenId];

        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "NFT #', Strings.toString(tokenId), '",',
                        '"description": "On-chain NFT",',
                        '"image": "data:image/svg+xml;base64,', generateSVG(traits), '",',
                        '"attributes": [',
                        '{"trait_type": "Background", "value": "', Strings.toString(traits.background), '"},',
                        '{"trait_type": "Rarity", "value": "', getRarityName(traits.rarity), '"}',
                        ']}'
                    )
                )
            )
        );

        return string(abi.encodePacked("data:application/json;base64,", json));
    }

    function generateSVG(Traits memory traits) internal pure returns (string memory) {
        // Generate SVG based on traits
        return "...";
    }
}
```

## Royalties (EIP-2981)

```solidity
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

contract NFTWithRoyalties is ERC721, IERC2981 {
    address public royaltyRecipient;
    uint96 public royaltyFee = 500; // 5%

    constructor() ERC721("Royalty NFT", "RNFT") {
        royaltyRecipient = msg.sender;
    }

    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        return (royaltyRecipient, (salePrice * royaltyFee) / 10000);
    }

    function setRoyalty(address recipient, uint96 fee) external onlyOwner {
        require(fee <= 1000, "Royalty fee too high"); // Max 10%
        royaltyRecipient = recipient;
        royaltyFee = fee;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, IERC165)
        returns (bool)
    {
        return interfaceId == type(IERC2981).interfaceId ||
               super.supportsInterface(interfaceId);
    }
}
```

## Soulbound 토큰 (Non-Transferable)

```solidity
contract SoulboundToken is ERC721 {
    constructor() ERC721("Soulbound", "SBT") {}

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal virtual override {
        require(from == address(0) || to == address(0), "Token is soulbound");
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function mint(address to) external {
        uint256 tokenId = totalSupply() + 1;
        _safeMint(to, tokenId);
    }

    // Burn is allowed (user can destroy their SBT)
    function burn(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        _burn(tokenId);
    }
}
```

## 동적 NFTs

```solidity
contract DynamicNFT is ERC721 {
    struct TokenState {
        uint256 level;
        uint256 experience;
        uint256 lastUpdated;
    }

    mapping(uint256 => TokenState) public tokenStates;

    function gainExperience(uint256 tokenId, uint256 exp) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");

        TokenState storage state = tokenStates[tokenId];
        state.experience += exp;

        // Level up logic
        if (state.experience >= state.level * 100) {
            state.level++;
        }

        state.lastUpdated = block.timestamp;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        TokenState memory state = tokenStates[tokenId];

        // Generate metadata based on current state
        return generateMetadata(tokenId, state);
    }

    function generateMetadata(uint256 tokenId, TokenState memory state)
        internal
        pure
        returns (string memory)
    {
        // Dynamic metadata generation
        return "";
    }
}
```

## Gas-최적화된 Minting (ERC721A)

```solidity
import "erc721a/contracts/ERC721A.sol";

contract OptimizedNFT is ERC721A {
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.05 ether;

    constructor() ERC721A("Optimized NFT", "ONFT") {}

    function mint(uint256 quantity) external payable {
        require(_totalMinted() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        _mint(msg.sender, quantity);
    }

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://QmBaseHash/";
    }
}
```

## 리소스

- **참조/erc721.md**: ERC-721 사양 details
- **참조/erc1155.md**: ERC-1155 multi-토큰 표준
- **참조/메타데이터-표준.md**: 메타데이터 최선의 관행
- **참조/열거.md**: 토큰 열거 패턴
- **자산/erc721-계약.sol**: Production ERC-721 템플릿
- **자산/erc1155-계약.sol**: Production ERC-1155 템플릿
- **자산/메타데이터-스키마.json**: 표준 메타데이터 format
- **자산/메타데이터-uploader.py**: IPFS upload utility

## 최선의 관행

1. **Use OpenZeppelin**: 검증된 implementations
2. **Pin 메타데이터**: Use IPFS 와 함께 pinning 서비스
3. **Implement Royalties**: EIP-2981 위한 marketplace compatibility
4. **Gas 최적화**: Use ERC721A 위한 batch minting
5. **Reveal 메커니즘**: Placeholder → reveal 패턴
6. **열거**: 지원 walletOfOwner 위한 marketplaces
7. **Whitelist**: Merkle trees 위한 efficient whitelisting

## Marketplace 통합

- OpenSea: ERC-721/1155, 메타데이터 표준
- LooksRare: Royalty enforcement
- Rarible: 프로토콜 fees, lazy minting
- Blur: Gas-최적화된 trading
