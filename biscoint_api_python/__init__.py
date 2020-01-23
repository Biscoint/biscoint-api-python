import base64
import hashlib
import hmac
import json
from urllib.parse import urljoin
import requests


class Biscoint:
    def __init__(self, api_key: str, api_secret: str, api_url: str = 'https://api.biscoint.io'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url

    def get_ticker(
        self,
        base: str = 'BTC',
        quote: str = 'BRL',
        amount: str = '1000.00',
        isQuote: bool = True,
        **kwargs
    ):
        """Gets ticker.

        Keyword Arguments:
            base {str} -- base currency (default: {'BTC'})
            quote {str} -- quote currency (default: {'BRL'})
            amount {str} -- amount to query (default: {'1000.00'})
            isQuote {bool} -- True if amount is in quote currency or False if base (default: {True})

        Returns:
            dict -- ticker data
                Example:
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
        return self._call('ticker', {
            'base': base,
            'quote': quote,
            'amount': amount,
            'isQuote': isQuote,
        })

    def get_fees(self, **kwargs):
        """Gets fees info.

        Returns:
            dict -- fees data
                Example:
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
        return self._call('fees')

    def get_meta(self, **kwargs):
        """Gets metadata about the API.

        Returns:
            dict -- meta data
                Example:
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
                            ...
                        }
                    }
        """
        return self._call('meta')

    def get_balance(self, **kwargs):
        """Gets balance.

        Returns:
            dict -- balance data
                Example:
                    {
                        "BRL": "9580.58",
                        "BTC": "0.01138164"
                    }
        """
        return self._call('balance', addAuth=True)

    def get_trades(self, op: str = None, length: int = None):
        """Gets last `length` trades. Current API default is 10.

        Keyword Arguments:
            op {str} -- filter trades by operation ('buy' or 'sell') (default: {None})
            length {int} -- number of trades to be returned (max: 20) (default: {None})

        Returns:
            list of dict -- list of data for trades ordered by most recent
                Example:
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
        return self._call('trades', {
            'op': op,
            'length': length,
        }, addAuth=True)

    def get_offer(
        self,
        op: str,
        amount: str,
        isQuote: bool,
        base: str = 'BTC',
        quote: str = 'BRL'
    ):
        """Gets an offer.

        Arguments:
            op {str} -- operation to be queryied ('buy' or 'sell')
            amount {str} -- offer amount
            isQuote {bool} -- True if amount is in quote currency or False if base

        Keyword Arguments:
            base {str} -- base currency (default: {'BTC'})
            quote {str} -- quote currency (default: {'BRL'})

        Returns:
            dict -- offer data
                Example:
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
        return self._call('offer', {
            'op': op,
            'amount': amount,
            'isQuote': isQuote,
            'base': base,
            'quote': quote,
        }, addAuth=True)

    def confirm_offer(self, offer_id: str):
        """Confirms offer and execute operation.

        Arguments:
            offer_id {str} -- offerId returned by get_offer()

        Returns:
            dict -- offer receipt
                Example:
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
        return self._call('offer', {
            'offerId': offer_id,
        }, addAuth=True, method='post')

    # PRIVATE

    def _call(self, endpoint: str, params: dict = {}, method: str = 'get', addAuth: bool = False):
        headers = None

        v1_endpoint = 'v1/%s' % (endpoint)
        url = urljoin(self.api_url, v1_endpoint)
        params['request'] = v1_endpoint

        params = self._remove_null_params(params)

        # print(params)

        if addAuth:
            signedParams = self._sign(params)
            headers = {
                'BSCNT-APIKEY': self.api_key,
                'BSCNT-SIGN': signedParams,
            }
            # print(headers)

        res = requests.request(
            method=method,
            url=url,
            params=self._normalize_params(params) if method == 'get' else None,
            data=self._normalize_params(params) if method == 'post' else None,
            headers=headers,
        )

        res.raise_for_status()

        res_json = res.json()

        # print(res.request.url)

        return res_json['data']

    def _sign(self, params: dict):
        jsonString = json.dumps(
            params,
            sort_keys=True,
            separators=(',', ':'),
        ).encode('utf-8')
        hashBuffer = base64.b64encode(jsonString)

        # print(jsonString)
        # print(hashBuffer)

        sign_data = hmac.new(
            self.api_secret.encode(),
            hashBuffer,
            hashlib.sha256
        ).hexdigest()

        # print(sign_data)

        return sign_data

    def _normalize_params(self, params: dict):
        n_params = {}
        for key in params.keys():
            if type(params[key]) is bool:
                n_params[key] = 'true' if params[key] else 'false'
            else:
                n_params[key] = params[key]

        return n_params

    def _remove_null_params(self, params):
        return {k: v for k, v in params.items() if v is not None}
