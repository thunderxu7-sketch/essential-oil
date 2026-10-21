"""Reject misleading destinations before they can become a real-purchase link."""
import unittest
from purchase import purchase_url

class PurchaseDestinationTests(unittest.TestCase):
    def config(self, value):
        return {'product': {'purchase_url': value}}

    def test_unconfigured_stays_unavailable(self):
        self.assertEqual(purchase_url({}), '')
        self.assertEqual(purchase_url(self.config('')), '')

    def test_direct_item_is_normalized_without_tracking(self):
        # Synthetic IDs test URL handling only, not product availability.
        for host, path in [('item.taobao.com','/item.htm'), ('detail.tmall.com','/item.htm'), ('detail.tmall.hk','/hk/item.htm')]:
            with self.subTest(host=host):
                clean=f'https://{host}{path}?id=123456'
                self.assertEqual(purchase_url(self.config(clean+'&spm=tracking&redirect=https%3A%2F%2Fexample.com')), clean)

    def test_placeholder_requires_explicit_mode_and_recorded_store(self):
        store='https://afusjt.tmall.com/shop/view_shop.htm'
        self.assertEqual(purchase_url({'product': {'purchase_url': store, 'purchase_mode': 'placeholder'}}), store)
        with self.assertRaises(ValueError):
            purchase_url(self.config(store))
        for mode, url in [('placeholder', 'https://evil.example/'), ('placeholder', store+'?redirect=example'), ('unknown', store)]:
            with self.subTest(mode=mode, url=url), self.assertRaises(ValueError):
                purchase_url({'product': {'purchase_url': url, 'purchase_mode': mode}})

    def test_rejects_search_shop_coupon_and_unsafe_urls(self):
        for url in [None, 'https://s.taobao.com/search?q=AFU',
                    'https://afusjt.tmall.com/shop/view_shop.htm',
                    'https://uland.taobao.com/coupon/edetail?e=example',
                    'https://detail.tmall.com.evil.example/item.htm?id=123',
                    'https://evil.example/item.htm?id=123',
                    'http://item.taobao.com/item.htm?id=123',
                    'javascript:alert(1)',
                    'https://user:pass@item.taobao.com/item.htm?id=123',
                    'https://item.taobao.com:8443/item.htm?id=123',
                    'https://item.taobao.com/item.htm',
                    'https://item.taobao.com/item.htm?id=123&id=456',
                    'https://item.taobao.com/item.htm?id=invalid',
                    'https://item.taobao.com/item.htm?id=123#redirect']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                purchase_url(self.config(url))

if __name__ == '__main__':
    unittest.main()
