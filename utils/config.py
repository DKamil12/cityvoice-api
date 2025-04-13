import yaml


class Config:
    def __init__(self, file: str = 'config.yaml'):
        self.file = file
        self.config_file = self.__read_yaml()

    def __read_yaml(self):
        with open(self.file) as stream:
            return yaml.safe_load(stream)
        
    def __getitem__(self, key):
        return self.config_file[key]