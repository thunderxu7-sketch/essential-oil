"""Shared navigation between the five published experiences."""
from html import escape

EXPERIENCES = [
    ('/', '官网'),
    ('/mini/', '小程序体验'),
    ('/activities/five-elements/', '五行主题签'),
    ('/activities/evening-personality/', '晚间偏好测试'),
    ('/admin/', '运营后台（演示）'),
]


def experience_navigation(base='', current=''):
    links = ''.join(
        f'<a href="{escape(base + path)}"'
        + (' aria-current="page"' if path == current else '')
        + f'>{label}</a>'
        for path, label in EXPERIENCES
    )
    return f'<nav class="experience-links" aria-label="站点导航">{links}</nav>'
