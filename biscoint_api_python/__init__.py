import requests
import json
from urllib.parse import urljoin
import hashlib
import base64


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
        return self._call('ticker', {
            'base': base,
            'quote': quote,
            'amount': amount,
            'isQuote': isQuote,
        })

    def get_meta(self, **kwargs):
        return self._call('meta')

    def get_balance(self, **kwargs):
        raise NotImplementedError

    def get_trades(self, op=None, length=None):
        raise NotImplementedError

    def get_offer(
        self,
        op: str,
        amount: str,
        isQuote: bool,
        base: str = 'BTC',
        quote: str = 'BRL'
    ):
        raise NotImplementedError

    def confirm_offer(self, offer_id: str):
        raise NotImplementedError

    # PRIVATE

    def _call(self, endpoint: str, params: dict = {}, method: str = 'get'):
        v1_endpoint = 'v1/%s' % (endpoint)
        url = urljoin(self.api_url, v1_endpoint)
        params['request'] = v1_endpoint

        signedParams = self._sign(params)

        # print(signedParams)

        headers = {
            'BSCNT-APIKEY': self.api_key,
            'BSCNT-SIGN': signedParams,
        }

        res = requests.request(
            method=method,
            url=url,
            params=self._normalize_params(params),
            headers=headers,
        )

        res.raise_for_status()

        res_json = res.json()

        # print(res.request.url)

        return res_json['data']

    def _sign(self, params: dict):
        jsonString = json.dumps(params, sort_keys=True, separators=(',', ':')).encode('utf-8')
        hashBuffer = base64.b64encode(jsonString)

        # print(jsonString)
        # print(hashBuffer)

        return hashlib.sha256(hashBuffer).hexdigest()

    def _normalize_params(self, params: dict):
        n_params = {}
        for key in params.keys():
            if type(params[key]) is bool:
                n_params[key] = 'true' if params[key] else 'false'
            else:
                n_params[key] = params[key]

        return n_params
