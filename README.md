# Biscoint API wrapper for python

This is a simple wrapper for Biscoint's API (v1). It handles all authentication stuffs so you can just worry about your killer robot.

## Dependencies

It only depends on the awesome [requests](https://requests.readthedocs.io/en/master/) package.

## Usage

```
pip install biscoint-api-python
```

### Example

```python
import json
import requests

from biscoint_api_python import Biscoint

api_data = {
    'api_key': '3ddc931bf25c94ff0344a2e409aa37339e400b8d4da72265f97c3a31d0cfb36e',
    'api_secret': 'd4c4db1567fba7dbc63b73e0a5c3a810360825a1de4530e05a77652efce91bcb',
}

bsc = Biscoint(api_data['api_key'], api_data['api_secret'])

try:
    ticker = bsc.get_ticker()
    print(json.dumps(ticker, indent=4))

    """
    {
        "base": "BTC",
        "quote": "BRL",
        "vol": 0.07414472,
        "low": 36010.54,
        "high": 36285,
        "last": 36069,
        "ask": 35343.56,
        "askQuoteAmountRef": 1000,
        "askBaseAmountRef": 0.0282937,
        "bid": 35149.76,
        "bidQuoteAmountRef": 1000,
        "bidBaseAmountRef": 0.0284497,
        "timestamp": "2020-01-23T12:26:11.564Z"
    }
    """

    fees = bsc.get_fees()
    print(json.dumps(fees, indent=4))

    """
    {
        "withdrawal": {
            "BTC": {
                "rate": "0.0",
                "fixed": {
                    "slow": "0.00005",
                    "normal": "0.00013",
                    "fast": "0.0002"
                }
            },
            "BRL": {
                "rate": "0.0",
                "fixed": {
                    "ted": "14.90",
                    "sameBankTransfer": "14.90"
                }
            }
        }
    }
    """

    meta = bsc.get_meta()
    print(json.dumps(meta, indent=4))

    """
    {
        "version": "v1",
        "endpoints": {
            "ticker": {
                "get": {
                    "type": "public",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 6000,
                        "rate": "6000 per 1 minute"
                    }
                }
            },
            "fees": {
                "get": {
                    "type": "public",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 2000,
                        "rate": "2000 per 1 minute"
                    }
                }
            },
            "meta": {
                "get": {
                    "type": "public",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 2000,
                        "rate": "2000 per 1 minute"
                    }
                }
            },
            "balance": {
                "get": {
                    "type": "private",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 12000,
                        "rate": "12000 per 1 minute"
                    }
                }
            },
            "offer": {
                "get": {
                    "type": "private",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 24000,
                        "rate": "24000 per 1 minute"
                    }
                },
                "post": {
                    "type": "private",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 24000,
                        "rate": "24000 per 1 minute"
                    }
                }
            },
            "trades": {
                "get": {
                    "type": "private",
                    "rateLimit": {
                        "windowMs": 60000,
                        "maxRequests": 12000,
                        "rate": "12000 per 1 minute"
                    }
                }
            }
        }
    }
    """

    balance = bsc.get_balance()
    print(json.dumps(balance, indent=4))

    """
    {
        "BRL": "9580.58",
        "BTC": "0.01138164"
    }
    """

    trades = bsc.get_trades(op='buy', length=1)
    print(json.dumps(trades, indent=4))

    """
    [
        {
            "id": "D6x63B3q3Mec4tggY",
            "op": "buy",
            "base": "BTC",
            "quote": "BRL",
            "baseAmount": "0.01000000",
            "quoteAmount": "362.82",
            "apiKeyId": "BdFABxNakZyxPwnRu",
            "efPrice": "36282.00",
            "date": "2020-01-22T23:25:02.785Z"
        }
    ]
    """
    
    offer = bsc.get_offer('buy', '0.002', False)
    print(json.dumps(offer, indent=4))

    """
    {
        "offerId": "ets52q7WQLrWw79Bq",
        "base": "BTC",
        "quote": "BRL",
        "op": "buy",
        "isQuote": false,
        "baseAmount": "0.01000000",
        "quoteAmount": "353.43",
        "efPrice": "35343.00",
        "createdAt": "2020-01-23T12:26:13.454Z",
        "expiresAt": "2020-01-23T12:26:28.454Z",
        "apiKeyId": "BdFABxNakZyxPwnRu"
    }
    """
    
    # WARNING: this will actually execute the buy operation!
    offerConfirmation = bsc.confirm_offer(offer['offerId'])
    print(json.dumps(offerConfirmation, indent=4))

    """
    {
        "offerId": "ets52q7WQLrWw79Bq",
        "base": "BTC",
        "quote": "BRL",
        "op": "buy",
        "isQuote": false,
        "baseAmount": "0.01000000",
        "quoteAmount": "353.43",
        "efPrice": "35343.00",
        "createdAt": "2020-01-23T12:26:13.454Z",
        "confirmedAt": "2020-01-23T12:26:14.096Z",
        "apiKeyId": "BdFABxNakZyxPwnRu"
    }
    """
except requests.exceptions.HTTPError as error:
    print(error)
    print(json.dumps(error.response.json(), indent=4))
```
