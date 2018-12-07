# -*- coding: utf-8 -*-

import json
import hashlib
import hmac
import time
import urllib

import argparse
import setting
from restful_lib import Connection


class AdflyApi():
    BASE_HOST = 'https://api.adf.ly'
    # TODO: Replace this with your secret key.
    SECRET_KEY = setting.SECRET_KEY
    # TODO: Replace this with your public key.
    PUBLIC_KEY = setting.PUBLIC_KEY
    # TODO: Replace this with your user id.
    USER_ID = setting.USER_ID
    AUTH_TYPE = dict(basic=1, hmac=2)

    def __init__(self):
        # In this example we use rest client provided by
        # http://code.google.com/p/python-rest-client/
        # Of course you are free to use any other client.
        self._connection = Connection(self.BASE_HOST)

    def shorten(self, urls, domain=None, advert_type=None, group_id=None):
        params = dict()
        if domain:
            params['domain'] = domain
        if advert_type:
            params['advert_type'] = advert_type
        if group_id:
            params['group_id'] = group_id

        if type(urls) == list:
            for i, url in enumerate(urls):
                params['url[%d]' % i] = url
        elif type(urls) == str:
            params['url'] = urls

        response = self._connection.request_post(
            '/v1/shorten',
            args=self._get_params(params, self.AUTH_TYPE['basic']))
        return json.loads(response['body'])

    def _get_params(self, params={}, auth_type=None):
        """Populates request parameters with required parameters,
        such as _user_id, _api_key, etc.
        """
        auth_type = auth_type or self.AUTH_TYPE['basic']

        params['_user_id'] = self.USER_ID
        params['_api_key'] = self.PUBLIC_KEY

        if self.AUTH_TYPE['basic'] == auth_type:
            pass
        elif self.AUTH_TYPE['hmac'] == auth_type:
            # Get current unix timestamp (UTC time).
            params['_timestamp'] = int(time.time())
            params['_hash'] = self._do_hmac(params)
        else:
            raise RuntimeError

        return params

    def _do_hmac(self, params):
        if type(params) != dict:
            raise RuntimeError

        # Get parameter names.
        keys = params.keys()
        # Sort them using byte ordering.
        # So 'param[10]' comes before 'param[2]'.
        keys.sort()
        queryParts = []

        # Url encode query string. The encoding should be performed
        # per RFC 1738 (http://www.faqs.org/rfcs/rfc1738)
        # which implies that spaces are encoded as plus (+) signs.
        for key in keys:
            quoted_key = urllib.quote_plus(str(key))
            if params[key] is None:
                params[key] = ''

            quoted_value = urllib.quote_plus(str(params[key]))
            queryParts.append('%s=%s' % (quoted_key, quoted_value))

        return hmac.new(
            self.SECRET_KEY,
            '&'.join(queryParts),
            hashlib.sha256).hexdigest()


def main(url, advert_type):
    api = AdflyApi()
    result = api.shorten(urls=url, domain=0,
                         advert_type=advert_type, group_id=None)
    print('The shortened url is:\n' + result['data'][0]['short_url'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Randomly shorten your url via adf.ly')

    parser.add_argument(
        '-u', '--url',
        type=str,
        required=True,
        nargs=1,
        help='the single url you wanna shorten')
    parser.add_argument(
        '-t', '--type',
        type=str,
        default='banner',
        help="the ads type you wanna use, and it's banner by default"
    )
    args = parser.parse_args()
    main(url=args.url, advert_type=args.type)
