import yaml
import os

PATH_TO_PLUGIN = os.path.dirname(os.path.realpath(__file__)).replace('/general', '/')


class Settings(object):
    def __init__(self):
        try:
            with open(PATH_TO_PLUGIN + 'general/settings.yaml.dist') as file:
                self.settings = yaml.load(file)
            if os.path.isfile(PATH_TO_PLUGIN + 'general/settings.yaml'):
                with open(PATH_TO_PLUGIN + 'general/settings.yaml') as file:
                    user_settings = yaml.load(file)

                for x in user_settings:
                    self.settings[x] = user_settings[x]
        except Exception as e:
            raise e
