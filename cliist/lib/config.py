import os
import pytoml

from cliist.lib.utils import ConfigurationError

try:
    input = raw_input
except NameError:
    pass

DEFAULT_CONFIG = {
    'output_date_format': '%d.%m.%Y @ %H:%M:%S',
    'time_offset': 0,
    'cache_enabled': 'n',
    'cache': '/tmp/todoist.json',
}


class Config(object):
    _color_project = '\033[95m'
    _color_filter = '\033[95m'
    _color_label = '\033[94m'
    _color_content = '\033[92m'
    _color_date = '\033[93m'
    _color_priority = '\033[96m'
    _color_fail = '\033[91m'
    _color_endc = '\033[0m'
    _config = None

    @classmethod
    def get(cls, key):
        conf = cls._load_config()
        if key not in conf:
            return None

        val = conf[key]
        if getattr(Config, '_{}'.format(key), None):
            return  getattr(Config, '_{}'.format(key))(val)
        return val

    @classmethod
    def _cache_enabled(cls, val):
        return val == 'y'

    @classmethod
    def configure(cls):
        try:
            curr = cls._load_config()
        except ConfigurationError:
            curr = DEFAULT_CONFIG

        curr['api_token'] = cls._config_prompt('API Token', curr, 'api_token')
        curr['output_date_format'] = cls._config_prompt('Output Date Format', curr, 'output_date_format')
        curr['time_offset'] = int(cls._config_prompt('Time Offset', curr, 'time_offset'))
        curr['cache_enabled'] = cls._config_prompt('Enable Cache (y/[n])', curr, 'cache_enabled').lower()[0]
        if curr['cache_enabled'] == 'y':
            curr['cache'] = cls._config_prompt('Cache File', curr, 'cache')
        elif 'cache' in curr:
            del curr['cache']

        cfg_path = os.path.expanduser('~/.cliist.toml')
        with open(cfg_path, 'w') as fs:
            print pytoml.dump(fs, curr)

    @classmethod
    def _config_prompt(cls, text, conf, key):
        if key in conf:
            prompt = '{} (default: {}): '.format(text, conf[key])
        else:
            prompt = '{}: '.format(text)
        resp = input(prompt).strip()
        if not resp:
            resp = conf[key] if key in conf else None
        return resp

    @classmethod
    def color(cls, color):
        return getattr(cls, '_color_{}'.format(color.lower()))

    @classmethod
    def _load_config(cls):
        if cls._config is None:
            cfg_path = os.path.expanduser('~/.cliist.toml')
            if not os.path.isfile(cfg_path):
                raise ConfigurationError("Configuration not found! Please run 'cliist configure'!")
            with open(cfg_path) as fs:
                cls._config = pytoml.load(fs)
        return cls._config
