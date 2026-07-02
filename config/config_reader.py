import os
import yaml

class ConfigReader:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._config = cls._load_config()
        return cls._instance
    
    @staticmethod
    def _load_config():
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @property
    def current_env(self):
        return os.getenv('TEST_ENV', self._config['base']['env'])
    
    @property
    def base_url(self):
        return self._config[self.current_env]['base_url']
    
    @property
    def timeout(self):
        return self._config[self.current_env]['timeout']
    
    @property
    def navigation_timeout(self):
        return self._config[self.current_env].get('navigation_timeout', self.timeout)
    
    @property
    def headless(self):
        return self._config[self.current_env]['headless']
    
    @property
    def browser(self):
        return self._config[self.current_env]['browser']
    
    @property
    def username(self):
        return self._config[self.current_env]['credentials']['username']
    
    @property
    def password(self):
        return self._config[self.current_env]['credentials']['password']
    
    def get(self, key, default=None):
        try:
            keys = key.split('.')
            value = self._config[self.current_env]
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_base(self, key, default=None):
        try:
            keys = key.split('.')
            value = self._config['base']
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

config = ConfigReader()