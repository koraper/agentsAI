---
name: paypal-integration
description: Integrate PayPal payment 처리 와 함께 지원 위한 express checkout, subscriptions, 및 refund 관리. Use 때 implementing PayPal payments, 처리 online transactions, 또는 구축 e-commerce checkout 흐릅니다.
---

# PayPal 통합

마스터 PayPal payment 통합 포함하여 Express Checkout, IPN 처리, recurring billing, 및 refund 워크플로우.

## 때 에 Use This Skill

- Integrating PayPal 처럼 a payment option
- Implementing express checkout 흐릅니다
- 설정하는 recurring billing 와 함께 PayPal
- 처리 refunds 및 payment disputes
- 처리 PayPal webhooks (IPN)
- Supporting international payments
- Implementing PayPal subscriptions

## 핵심 개념

### 1. Payment Products
**PayPal Checkout**
- One-시간 payments
- Express checkout experience
- 게스트 및 PayPal 계정 payments

**PayPal Subscriptions**
- Recurring billing
- 구독 계획합니다
- Automatic renewals

**PayPal Payouts**
- Send money 에 여러 recipients
- Marketplace 및 플랫폼 payments

### 2. 통합 메서드
**클라이언트-Side (JavaScript SDK)**
- Smart Payment Buttons
- Hosted payment 흐름
- 최소 backend 코드

**서버-Side (REST API)**
- 전체 control over payment 흐름
- 사용자 정의 checkout UI
- 고급 기능

### 3. IPN (순간 Payment 알림)
- Webhook-같은 payment 알림
- Asynchronous payment 업데이트합니다
- 확인 필수

## Quick Start

```javascript
// Frontend - PayPal Smart Buttons
<div id="paypal-button-container"></div>

<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '25.00'
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        // Payment successful
        console.log('Transaction completed by ' + details.payer.name.given_name);

        // Send to backend for verification
        fetch('/api/paypal/capture', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({orderID: data.orderID})
        });
      });
    }
  }).render('#paypal-button-container');
</script>
```

```python
# Backend - Verify and capture order
from paypalrestsdk import Payment
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # or "live"
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

def capture_paypal_order(order_id):
    """Capture a PayPal order."""
    payment = Payment.find(order_id)

    if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
        # Payment successful
        return {
            'status': 'success',
            'transaction_id': payment.id,
            'amount': payment.transactions[0].amount.total
        }
    else:
        # Payment failed
        return {
            'status': 'failed',
            'error': payment.error
        }
```

## Express Checkout 구현

### 서버-Side 순서 생성
```python
import requests
import json

class PayPalClient:
    def __init__(self, client_id, client_secret, mode='sandbox'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """Get OAuth access token."""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}

        response = requests.post(
            url,
            headers=headers,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret)
        )

        return response.json()['access_token']

    def create_order(self, amount, currency='USD'):
        """Create a PayPal order."""
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                }
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def capture_order(self, order_id):
        """Capture payment for an order."""
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(url, headers=headers)
        return response.json()

    def get_order_details(self, order_id):
        """Get order details."""
        url = f"{self.base_url}/v2/checkout/orders/{order_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        return response.json()
```

## IPN (순간 Payment 알림) 처리

### IPN 확인 및 처리
```python
from flask import Flask, request
import requests
from urllib.parse import parse_qs

app = Flask(__name__)

@app.route('/ipn', methods=['POST'])
def handle_ipn():
    """Handle PayPal IPN notifications."""
    # Get IPN message
    ipn_data = request.form.to_dict()

    # Verify IPN with PayPal
    if not verify_ipn(ipn_data):
        return 'IPN verification failed', 400

    # Process IPN based on transaction type
    payment_status = ipn_data.get('payment_status')
    txn_type = ipn_data.get('txn_type')

    if payment_status == 'Completed':
        handle_payment_completed(ipn_data)
    elif payment_status == 'Refunded':
        handle_refund(ipn_data)
    elif payment_status == 'Reversed':
        handle_chargeback(ipn_data)

    return 'IPN processed', 200

def verify_ipn(ipn_data):
    """Verify IPN message authenticity."""
    # Add 'cmd' parameter
    verify_data = ipn_data.copy()
    verify_data['cmd'] = '_notify-validate'

    # Send back to PayPal for verification
    paypal_url = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'  # or production URL

    response = requests.post(paypal_url, data=verify_data)

    return response.text == 'VERIFIED'

def handle_payment_completed(ipn_data):
    """Process completed payment."""
    txn_id = ipn_data.get('txn_id')
    payer_email = ipn_data.get('payer_email')
    mc_gross = ipn_data.get('mc_gross')
    item_name = ipn_data.get('item_name')

    # Check if already processed (prevent duplicates)
    if is_transaction_processed(txn_id):
        return

    # Update database
    # Send confirmation email
    # Fulfill order
    print(f"Payment completed: {txn_id}, Amount: ${mc_gross}")

def handle_refund(ipn_data):
    """Handle refund."""
    parent_txn_id = ipn_data.get('parent_txn_id')
    mc_gross = ipn_data.get('mc_gross')

    # Process refund in your system
    print(f"Refund processed: {parent_txn_id}, Amount: ${mc_gross}")

def handle_chargeback(ipn_data):
    """Handle payment reversal/chargeback."""
    txn_id = ipn_data.get('txn_id')
    reason_code = ipn_data.get('reason_code')

    # Handle chargeback
    print(f"Chargeback: {txn_id}, Reason: {reason_code}")
```

## 구독/Recurring Billing

### Create 구독 Plan
```python
def create_subscription_plan(name, amount, interval='MONTH'):
    """Create a subscription plan."""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v1/billing/plans"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {
        "product_id": "PRODUCT_ID",  # Create product first
        "name": name,
        "billing_cycles": [{
            "frequency": {
                "interval_unit": interval,
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 1,
            "total_cycles": 0,  # Infinite
            "pricing_scheme": {
                "fixed_price": {
                    "value": str(amount),
                    "currency_code": "USD"
                }
            }
        }],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def create_subscription(plan_id, subscriber_email):
    """Create a subscription for a customer."""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v1/billing/subscriptions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {
        "plan_id": plan_id,
        "subscriber": {
            "email_address": subscriber_email
        },
        "application_context": {
            "return_url": "https://yourdomain.com/subscription/success",
            "cancel_url": "https://yourdomain.com/subscription/cancel"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    subscription = response.json()

    # Get approval URL
    for link in subscription.get('links', []):
        if link['rel'] == 'approve':
            return {
                'subscription_id': subscription['id'],
                'approval_url': link['href']
            }
```

## Refund 워크플로우

```python
def create_refund(capture_id, amount=None, note=None):
    """Create a refund for a captured payment."""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v2/payments/captures/{capture_id}/refund"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {}
    if amount:
        payload["amount"] = {
            "value": str(amount),
            "currency_code": "USD"
        }

    if note:
        payload["note_to_payer"] = note

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def get_refund_details(refund_id):
    """Get refund details."""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v2/payments/refunds/{refund_id}"
    headers = {
        "Authorization": f"Bearer {client.access_token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

## 오류 처리

```python
class PayPalError(Exception):
    """Custom PayPal error."""
    pass

def handle_paypal_api_call(api_function):
    """Wrapper for PayPal API calls with error handling."""
    try:
        result = api_function()
        return result
    except requests.exceptions.RequestException as e:
        # Network error
        raise PayPalError(f"Network error: {str(e)}")
    except Exception as e:
        # Other errors
        raise PayPalError(f"PayPal API error: {str(e)}")

# Usage
try:
    order = handle_paypal_api_call(lambda: client.create_order(25.00))
except PayPalError as e:
    # Handle error appropriately
    log_error(e)
```

## 테스트

```python
# Use sandbox credentials
SANDBOX_CLIENT_ID = "..."
SANDBOX_SECRET = "..."

# Test accounts
# Create test buyer and seller accounts at developer.paypal.com

def test_payment_flow():
    """Test complete payment flow."""
    client = PayPalClient(SANDBOX_CLIENT_ID, SANDBOX_SECRET, mode='sandbox')

    # Create order
    order = client.create_order(10.00)
    assert 'id' in order

    # Get approval URL
    approval_url = next((link['href'] for link in order['links'] if link['rel'] == 'approve'), None)
    assert approval_url is not None

    # After approval (manual step with test account)
    # Capture order
    # captured = client.capture_order(order['id'])
    # assert captured['status'] == 'COMPLETED'
```

## 리소스

- **참조/express-checkout.md**: Express Checkout 구현 가이드
- **참조/ipn-처리.md**: IPN 확인 및 처리
- **참조/refund-워크플로우.md**: Refund 처리 패턴
- **참조/billing-agreements.md**: Recurring billing 설정
- **자산/paypal-클라이언트.py**: Production PayPal 클라이언트
- **자산/ipn-processor.py**: IPN webhook processor
- **자산/recurring-billing.py**: 구독 관리

## 최선의 관행

1. **항상 Verify IPN**: 절대 ~하지 않음 trust IPN 없이 확인
2. **Idempotent 처리**: Handle 중복 IPN 알림
3. **오류 처리**: Implement 강력한 오류 처리
4. **로깅**: Log 모든 transactions 및 오류
5. **Test 철저히**: Use sandbox 광범위하게
6. **Webhook 백업**: Don't rely solely 에 클라이언트-side callbacks
7. **Currency 처리**: 항상 specify currency 명시적으로

## 일반적인 Pitfalls

- **Not Verifying IPN**: Accepting IPN 없이 확인
- **중복 처리**: Not 확인 위한 중복 transactions
- **틀린 환경**: Mixing sandbox 및 production URLs/자격 증명
- **Missing Webhooks**: Not 처리 모든 payment states
- **Hardcoded 값**: Not making 구성 가능한 위한 다른 환경
