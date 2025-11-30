---
name: stripe-integration
description: Implement Stripe payment 처리 위한 강력한, PCI-compliant payment 흐릅니다 포함하여 checkout, subscriptions, 및 webhooks. Use 때 integrating Stripe payments, 구축 구독 시스템, 또는 implementing secure checkout 흐릅니다.
---

# Stripe 통합

마스터 Stripe payment 처리 통합 위한 강력한, PCI-compliant payment 흐릅니다 포함하여 checkout, subscriptions, webhooks, 및 refunds.

## 때 에 Use This Skill

- Implementing payment 처리 에서 web/mobile 애플리케이션
- 설정하는 구독 billing 시스템
- 처리 one-시간 payments 및 recurring charges
- 처리 refunds 및 disputes
- Managing 고객 payment 메서드
- Implementing SCA (강한 고객 인증) 위한 European payments
- 구축 marketplace payment 흐릅니다 와 함께 Stripe Connect

## 핵심 개념

### 1. Payment 흐릅니다
**Checkout 세션 (Hosted)**
- Stripe-hosted payment 페이지
- 최소 PCI compliance burden
- Fastest 구현
- 지원합니다 one-시간 및 recurring payments

**Payment Intents (사용자 정의 UI)**
- 전체 control over payment UI
- 필요합니다 Stripe.js 위한 PCI compliance
- More 복잡한 구현
- 더 나은 사용자 정의 options

**설정 Intents (Save Payment 메서드)**
- Collect payment 메서드 없이 charging
- Used 위한 subscriptions 및 미래 payments
- 필요합니다 고객 confirmation

### 2. Webhooks
**긴급 이벤트:**
- `payment_intent.succeeded`: Payment 완료됨
- `payment_intent.payment_failed`: Payment 실패
- `customer.subscription.updated`: 구독 변경된
- `customer.subscription.deleted`: 구독 canceled
- `charge.refunded`: Refund 처리된
- `invoice.payment_succeeded`: 구독 payment 성공한

### 3. Subscriptions
**컴포넌트:**
- **Product**: 무엇 you're selling
- **Price**: 어떻게 much 및 어떻게 자주
- **구독**: 고객's recurring payment
- **Invoice**: 생성된 위한 각 billing 사이클

### 4. 고객 관리
- Create 및 manage 고객 레코드
- Store 여러 payment 메서드
- Track 고객 메타데이터
- Manage billing details

## Quick Start

```python
import stripe

stripe.api_key = "sk_test_..."

# Create a checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # $20.00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel',
)

# Redirect user to session.url
print(session.url)
```

## Payment 구현 패턴

### 패턴 1: One-시간 Payment (Hosted Checkout)
```python
def create_checkout_session(amount, currency='usd'):
    """Create a one-time payment checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Purchase',
                        'images': ['https://example.com/product.jpg'],
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={
                'order_id': 'order_123',
                'user_id': 'user_456'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe error: {e.user_message}")
        raise
```

### 패턴 2: 사용자 정의 Payment Intent 흐름
```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent for custom checkout UI."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # Send to frontend

# Frontend (JavaScript)
"""
const stripe = Stripe('pk_test_...');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

const {error, paymentIntent} = await stripe.confirmCardPayment(
    clientSecret,
    {
        payment_method: {
            card: cardElement,
            billing_details: {
                name: 'Customer Name'
            }
        }
    }
);

if (error) {
    // Handle error
} else if (paymentIntent.status === 'succeeded') {
    // Payment successful
}
"""
```

### 패턴 3: 구독 생성
```python
def create_subscription(customer_id, price_id):
    """Create a subscription for a customer."""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### 패턴 4: 고객 Portal
```python
def create_customer_portal_session(customer_id):
    """Create a portal session for customers to manage subscriptions."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='https://yourdomain.com/account',
    )
    return session.url  # Redirect customer here
```

## Webhook 처리

### Secure Webhook 엔드포인트
```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = 'whsec_...'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200

def handle_successful_payment(payment_intent):
    """Process successful payment."""
    customer_id = payment_intent.get('customer')
    amount = payment_intent['amount']
    metadata = payment_intent.get('metadata', {})

    # Update your database
    # Send confirmation email
    # Fulfill order
    print(f"Payment succeeded: {payment_intent['id']}")

def handle_failed_payment(payment_intent):
    """Handle failed payment."""
    error = payment_intent.get('last_payment_error', {})
    print(f"Payment failed: {error.get('message')}")
    # Notify customer
    # Update order status

def handle_subscription_canceled(subscription):
    """Handle subscription cancellation."""
    customer_id = subscription['customer']
    # Update user access
    # Send cancellation email
    print(f"Subscription canceled: {subscription['id']}")
```

### Webhook 최선의 관행
```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Manually verify webhook signature."""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    # Check if event already processed
    if is_event_processed(event_id):
        return

    # Process event
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe will retry failed webhooks
        raise
```

## 고객 관리

```python
def create_customer(email, name, payment_method_id=None):
    """Create a Stripe customer."""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        } if payment_method_id else None,
        metadata={
            'user_id': '12345'
        }
    )
    return customer

def attach_payment_method(customer_id, payment_method_id):
    """Attach a payment method to a customer."""
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # Set as default
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def list_customer_payment_methods(customer_id):
    """List all payment methods for a customer."""
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    return payment_methods.data
```

## Refund 처리

```python
def create_refund(payment_intent_id, amount=None, reason=None):
    """Create a refund."""
    refund_params = {
        'payment_intent': payment_intent_id
    }

    if amount:
        refund_params['amount'] = amount  # Partial refund

    if reason:
        refund_params['reason'] = reason  # 'duplicate', 'fraudulent', 'requested_by_customer'

    refund = stripe.Refund.create(**refund_params)
    return refund

def handle_dispute(charge_id, evidence):
    """Update dispute with evidence."""
    stripe.Dispute.modify(
        charge_id,
        evidence={
            'customer_name': evidence.get('customer_name'),
            'customer_email_address': evidence.get('customer_email'),
            'shipping_documentation': evidence.get('shipping_proof'),
            'customer_communication': evidence.get('communication'),
        }
    )
```

## 테스트

```python
# Use test mode keys
stripe.api_key = "sk_test_..."

# Test card numbers
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995'
}

def test_payment_flow():
    """Test complete payment flow."""
    # Create test customer
    customer = stripe.Customer.create(
        email="test@example.com"
    )

    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        customer=customer.id,
        payment_method_types=['card']
    )

    # Confirm with test card
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'  # Test payment method
    )

    assert confirmed.status == 'succeeded'
```

## 리소스

- **참조/checkout-흐릅니다.md**: 상세한 checkout 구현
- **참조/webhook-처리.md**: Webhook security 및 처리
- **참조/구독-관리.md**: 구독 lifecycle
- **참조/고객-관리.md**: 고객 및 payment 메서드 처리
- **참조/invoice-세대.md**: Invoicing 및 billing
- **자산/stripe-클라이언트.py**: 프로덕션 준비 완료 Stripe 클라이언트 래퍼
- **자산/webhook-핸들러.py**: 완전한 webhook processor
- **자산/checkout-config.json**: Checkout 구성 템플릿

## 최선의 관행

1. **항상 Use Webhooks**: Don't rely solely 에 클라이언트-side confirmation
2. **Idempotency**: Handle webhook 이벤트 idempotently
3. **오류 처리**: Gracefully handle 모든 Stripe 오류
4. **Test 최빈값**: 철저히 test 와 함께 test 키 이전 production
5. **메타데이터**: Use 메타데이터 에 링크 Stripe 객체 에 your 데이터베이스
6. **모니터링**: Track payment success 평가합니다 및 오류
7. **PCI Compliance**: 절대 ~하지 않음 handle raw card 데이터 에 your 서버
8. **SCA Ready**: Implement 3D Secure 위한 European payments

## 일반적인 Pitfalls

- **Not Verifying Webhooks**: 항상 verify webhook signatures
- **Missing Webhook 이벤트**: Handle 모든 관련 webhook 이벤트
- **Hardcoded Amounts**: Use cents/smallest currency 단위
- **아니요 재시도 Logic**: Implement 재시도합니다 위한 API calls
- **Ignoring Test 최빈값**: Test 모든 엣지 cases 와 함께 test cards
