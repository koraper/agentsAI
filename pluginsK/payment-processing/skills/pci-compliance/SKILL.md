---
name: pci-compliance
description: Implement PCI DSS compliance 요구사항 위한 secure 처리 of payment card 데이터 및 payment 시스템. Use 때 securing payment 처리, achieving PCI compliance, 또는 implementing payment card security 측정합니다.
---

# PCI Compliance

마스터 PCI DSS (Payment Card 산업 데이터 Security 표준) compliance 위한 secure payment 처리 및 처리 of cardholder 데이터.

## 때 에 Use This Skill

- 구축 payment 처리 시스템
- 처리 credit card 정보
- Implementing secure payment 흐릅니다
- Conducting PCI compliance 감사합니다
- Reducing PCI compliance 범위
- Implementing 토큰화 및 암호화
- Preparing 위한 PCI DSS assessments

## PCI DSS 요구사항 (12 핵심 요구사항)

### 빌드 및 Maintain Secure 네트워크
1. Install 및 maintain firewall 구성
2. Don't use vendor-supplied defaults 위한 passwords

### Protect Cardholder 데이터
3. Protect 저장됨 cardholder 데이터
4. Encrypt 전송 of cardholder 데이터 전반에 걸쳐 공개 networks

### Maintain 취약점 관리
5. Protect 시스템 against 악성코드
6. Develop 및 maintain secure 시스템 및 애플리케이션

### Implement 강한 Access Control
7. Restrict access 에 cardholder 데이터 에 의해 비즈니스 need-에-know
8. Identify 및 authenticate access 에 시스템 컴포넌트
9. Restrict physical access 에 cardholder 데이터

### 모니터 및 Test Networks
10. Track 및 모니터 모든 access 에 네트워크 리소스 및 cardholder 데이터
11. 정기적으로 test security 시스템 및 프로세스

### Maintain 정보 Security 정책
12. Maintain a 정책 것 주소 정보 security

## Compliance Levels

**레벨 1**: > 6 million transactions/year (annual ROC 필수)
**레벨 2**: 1-6 million transactions/year (annual SAQ)
**레벨 3**: 20,000-1 million e-commerce transactions/year
**레벨 4**: < 20,000 e-commerce 또는 < 1 million 총계 transactions

## 데이터 Minimization (절대 ~하지 않음 Store)

```python
# NEVER STORE THESE
PROHIBITED_DATA = {
    'full_track_data': 'Magnetic stripe data',
    'cvv': 'Card verification code/value',
    'pin': 'PIN or PIN block'
}

# CAN STORE (if encrypted)
ALLOWED_DATA = {
    'pan': 'Primary Account Number (card number)',
    'cardholder_name': 'Name on card',
    'expiration_date': 'Card expiration',
    'service_code': 'Service code'
}

class PaymentData:
    """Safe payment data handling."""

    def __init__(self):
        self.prohibited_fields = ['cvv', 'cvv2', 'cvc', 'pin']

    def sanitize_log(self, data):
        """Remove sensitive data from logs."""
        sanitized = data.copy()

        # Mask PAN
        if 'card_number' in sanitized:
            card = sanitized['card_number']
            sanitized['card_number'] = f"{card[:6]}{'*' * (len(card) - 10)}{card[-4:]}"

        # Remove prohibited data
        for field in self.prohibited_fields:
            sanitized.pop(field, None)

        return sanitized

    def validate_no_prohibited_storage(self, data):
        """Ensure no prohibited data is being stored."""
        for field in self.prohibited_fields:
            if field in data:
                raise SecurityError(f"Attempting to store prohibited field: {field}")
```

## 토큰화

### 사용하여 Payment Processor 토큰
```python
import stripe

class TokenizedPayment:
    """Handle payments using tokens (no card data on server)."""

    @staticmethod
    def create_payment_method_token(card_details):
        """Create token from card details (client-side only)."""
        # THIS SHOULD ONLY BE DONE CLIENT-SIDE WITH STRIPE.JS
        # NEVER send card details to your server

        """
        // Frontend JavaScript
        const stripe = Stripe('pk_...');

        const {token, error} = await stripe.createToken({
            card: {
                number: '4242424242424242',
                exp_month: 12,
                exp_year: 2024,
                cvc: '123'
            }
        });

        // Send token.id to server (NOT card details)
        """
        pass

    @staticmethod
    def charge_with_token(token_id, amount):
        """Charge using token (server-side)."""
        # Your server only sees the token, never the card number
        stripe.api_key = "sk_..."

        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token_id,  # Token instead of card details
            description="Payment"
        )

        return charge

    @staticmethod
    def store_payment_method(customer_id, payment_method_token):
        """Store payment method as token for future use."""
        stripe.Customer.modify(
            customer_id,
            source=payment_method_token
        )

        # Store only customer_id and payment_method_id in your database
        # NEVER store actual card details
        return {
            'customer_id': customer_id,
            'has_payment_method': True
            # DO NOT store: card number, CVV, etc.
        }
```

### 사용자 정의 토큰화 (고급)
```python
import secrets
from cryptography.fernet import Fernet

class TokenVault:
    """Secure token vault for card data (if you must store it)."""

    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
        self.vault = {}  # In production: use encrypted database

    def tokenize(self, card_data):
        """Convert card data to token."""
        # Generate secure random token
        token = secrets.token_urlsafe(32)

        # Encrypt card data
        encrypted = self.cipher.encrypt(json.dumps(card_data).encode())

        # Store token -> encrypted data mapping
        self.vault[token] = encrypted

        return token

    def detokenize(self, token):
        """Retrieve card data from token."""
        encrypted = self.vault.get(token)
        if not encrypted:
            raise ValueError("Token not found")

        # Decrypt
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def delete_token(self, token):
        """Remove token from vault."""
        self.vault.pop(token, None)
```

## 암호화

### 데이터 에서 Rest
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptedStorage:
    """Encrypt data at rest using AES-256-GCM."""

    def __init__(self, encryption_key):
        """Initialize with 256-bit key."""
        self.key = encryption_key  # Must be 32 bytes

    def encrypt(self, plaintext):
        """Encrypt data."""
        # Generate random nonce
        nonce = os.urandom(12)

        # Encrypt
        aesgcm = AESGCM(self.key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        # Return nonce + ciphertext
        return nonce + ciphertext

    def decrypt(self, encrypted_data):
        """Decrypt data."""
        # Extract nonce and ciphertext
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        # Decrypt
        aesgcm = AESGCM(self.key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext.decode()

# Usage
storage = EncryptedStorage(os.urandom(32))
encrypted_pan = storage.encrypt("4242424242424242")
# Store encrypted_pan in database
```

### 데이터 에서 Transit
```python
# Always use TLS 1.2 or higher
# Flask/Django example
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Enforce HTTPS
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

## Access Control

```python
from functools import wraps
from flask import session

def require_pci_access(f):
    """Decorator to restrict access to cardholder data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')

        # Check if user has PCI access role
        if not user or 'pci_access' not in user.get('roles', []):
            return {'error': 'Unauthorized access to cardholder data'}, 403

        # Log access attempt
        audit_log(
            user=user['id'],
            action='access_cardholder_data',
            resource=f.__name__
        )

        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/payment-methods')
@require_pci_access
def get_payment_methods():
    """Retrieve payment methods (restricted access)."""
    # Only accessible to users with pci_access role
    pass
```

## Audit 로깅

```python
import logging
from datetime import datetime

class PCIAuditLogger:
    """PCI-compliant audit logging."""

    def __init__(self):
        self.logger = logging.getLogger('pci_audit')
        # Configure to write to secure, append-only log

    def log_access(self, user_id, resource, action, result):
        """Log access to cardholder data."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'result': result,
            'ip_address': request.remote_addr
        }

        self.logger.info(json.dumps(entry))

    def log_authentication(self, user_id, success, method):
        """Log authentication attempt."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'event': 'authentication',
            'success': success,
            'method': method,
            'ip_address': request.remote_addr
        }

        self.logger.info(json.dumps(entry))

# Usage
audit = PCIAuditLogger()
audit.log_access(user_id=123, resource='payment_methods', action='read', result='success')
```

## Security 최선의 관행

### 입력 검증
```python
import re

def validate_card_number(card_number):
    """Validate card number format (Luhn algorithm)."""
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)

    # Check if all digits
    if not card_number.isdigit():
        return False

    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    return luhn_checksum(card_number) == 0

def sanitize_input(user_input):
    """Sanitize user input to prevent injection."""
    # Remove special characters
    # Validate against expected format
    # Escape for database queries
    pass
```

## PCI DSS SAQ (Self-평가 Questionnaire)

### SAQ A (Least 요구사항)
- E-commerce 사용하여 hosted payment 페이지
- 아니요 card 데이터 에 your 시스템
- ~20 questions

### SAQ A-EP
- E-commerce 와 함께 embedded payment 폼
- Uses JavaScript 에 handle card 데이터
- ~180 questions

### SAQ D (Most 요구사항)
- Store, 프로세스, 또는 transmit card 데이터
- 전체 PCI DSS 요구사항
- ~300 questions

## Compliance Checklist

```python
PCI_COMPLIANCE_CHECKLIST = {
    'network_security': [
        'Firewall configured and maintained',
        'No vendor default passwords',
        'Network segmentation implemented'
    ],
    'data_protection': [
        'No storage of CVV, track data, or PIN',
        'PAN encrypted when stored',
        'PAN masked when displayed',
        'Encryption keys properly managed'
    ],
    'vulnerability_management': [
        'Anti-virus installed and updated',
        'Secure development practices',
        'Regular security patches',
        'Vulnerability scanning performed'
    ],
    'access_control': [
        'Access restricted by role',
        'Unique IDs for all users',
        'Multi-factor authentication',
        'Physical security measures'
    ],
    'monitoring': [
        'Audit logs enabled',
        'Log review process',
        'File integrity monitoring',
        'Regular security testing'
    ],
    'policy': [
        'Security policy documented',
        'Risk assessment performed',
        'Security awareness training',
        'Incident response plan'
    ]
}
```

## 리소스

- **참조/데이터-minimization.md**: 절대 ~하지 않음 store prohibited 데이터
- **참조/토큰화.md**: 토큰화 strategies
- **참조/암호화.md**: 암호화 요구사항
- **참조/access-control.md**: Role-based access
- **참조/audit-로깅.md**: 포괄적인 로깅
- **자산/pci-compliance-checklist.md**: 완전한 checklist
- **자산/암호화된-스토리지.py**: 암호화 utilities
- **스크립트/audit-payment-시스템.sh**: Compliance audit 스크립트

## 일반적인 위반

1. **Storing CVV**: 절대 ~하지 않음 store card 확인 codes
2. **Unencrypted PAN**: Card numbers must be 암호화된 에서 rest
3. **약한 암호화**: Use AES-256 또는 equivalent
4. **아니요 Access 제어합니다**: Restrict 누구 can access cardholder 데이터
5. **Missing Audit 로깅합니다**: Must log 모든 access 에 payment 데이터
6. **Insecure 전송**: 항상 use TLS 1.2+
7. **default Passwords**: 변경 모든 default 자격 증명
8. **아니요 Security 테스트**: 일반 penetration 테스트 필수

## Reducing PCI 범위

1. **Use Hosted Payments**: Stripe Checkout, PayPal, etc.
2. **토큰화**: Replace card 데이터 와 함께 토큰
3. **네트워크 세그먼테이션**: Isolate cardholder 데이터 환경
4. **Outsource**: Use PCI-compliant payment processors
5. **아니요 스토리지**: 절대 ~하지 않음 store 전체 card details

에 의해 minimizing 시스템 것 touch card 데이터, you reduce compliance burden 상당히.
