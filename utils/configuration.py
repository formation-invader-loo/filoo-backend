import configparser
import os

config = configparser.ConfigParser()

config.add_section('paths')
config.set('paths', 'data', os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))
config.set('paths', 'html', os.path.abspath(os.path.join(os.path.dirname(__file__), '../html')))

config.add_section('server')
config.set('server', 'IPv4', 'to be defined xD') # TODO wenn containerized the correct adress has to be set here.
config.set('server', 'port', 'to be defined xD') # TODO wenn containerized the correct port has to be set here.

with open(os.path.join(os.path.dirname(__file__), '../config.ini'), 'w') as config_file:
  config.write(config_file)

def get_config(section: str, key: str) -> str:
  """Get a specifig value from the config file.

  Args:
      section (str): section of the config file
      key (str): key of the config file

  Returns:
      str: value of the config file in the specific section with the specific key
  """
  config_object = configparser.ConfigParser()
  with open(os.path.join(os.path.dirname(__file__), '../config.ini'), 'r') as file_object:
      config_object.read_file(file_object)
      value = config_object.get(section, key)
      return value