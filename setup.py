try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'pipview',
    'author': 'Yoong Kang Lim',
    'url': 'http://github.com/yoongkang/pip-view',
    'download_url': 'http://github.com/yoongkang/pip-view',
    'author_email': 'yoongkang.lim@gmail.com',
    'version': '0.1.1',
    'install_requires': ['pip'],
    'packages': ['pipview'],
    'entry_points': {'console_scripts': ['pip-view=pipview.view:main']},
    'name': 'pipview'
}

setup(**config)
