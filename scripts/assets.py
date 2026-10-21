"""Version local script and style URLs when their contents change."""
import hashlib
import re


def version_assets(content, output, base=''):
    pattern = r'((?:href|src)=")(' + re.escape(base) + r'/(?:assets|demo-assets)/[^"?]+\.(?:css|js))(\")'

    def replace(match):
        asset = output / match[2].removeprefix(base + '/')
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
        return f'{match[1]}{match[2]}?v={digest}{match[3]}'

    return re.sub(pattern, replace, content)
