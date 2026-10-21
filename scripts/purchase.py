"""Validate product destinations and explicitly labelled temporary store links."""
from urllib.parse import urlsplit, parse_qs

ITEM_PATHS = {
    'detail.tmall.com': '/item.htm',
    'detail.tmall.hk': '/hk/item.htm',
    'item.taobao.com': '/item.htm',
}
PLACEHOLDER_URL = 'https://afusjt.tmall.com/shop/view_shop.htm'

def purchase_url(config):
    product = config.get('product', {})
    mode = product.get('purchase_mode', 'product')
    if mode not in ('product', 'placeholder'):
        raise ValueError('purchase_mode 必须是 product 或 placeholder。')
    value = product.get('purchase_url', '')
    if not isinstance(value, str):
        raise ValueError('purchase_url 必须是商品直达链接字符串。')
    if not value:
        return ''
    if mode == 'placeholder':
        if value != PLACEHOLDER_URL:
            raise ValueError('占位模式只允许已记录的天猫店铺首页。')
        return value
    try:
        url = urlsplit(value)
        port = url.port
    except ValueError as error:
        raise ValueError('购买链接格式无效。') from error
    item_ids = parse_qs(url.query).get('id', [])
    if (url.scheme != 'https' or url.hostname not in ITEM_PATHS
        or url.path != ITEM_PATHS.get(url.hostname) or url.username or url.password
        or port not in (None, 443) or url.fragment
        or len(item_ids) != 1 or not item_ids[0].isascii() or not item_ids[0].isdigit()):
        raise ValueError('购买链接须为带商品 id 的 HTTPS 淘宝或天猫商品直达页。')
    # Drop affiliate, coupon, redirect and other third-party query parameters.
    return f'https://{url.hostname}{url.path}?id={item_ids[0]}'
