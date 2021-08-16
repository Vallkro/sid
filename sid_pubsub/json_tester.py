import json
import os
# Look for your absolute directory path
absolute_path = os.path.dirname(os.path.abspath(__file__))
print(absolute_path)
file_path = os.path.join(absolute_path, 'config.json')
print(file_path)
f =open(file_path) 
config = json.load(f)
homedir = os.environ['HOME']
print(homedir)
#f.close()
print(config['robot_command_topic'])
f.close()