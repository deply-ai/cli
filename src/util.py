import os
import yaml
import logging
import requests
from deplyai.schema.cli import ProfileCredentials
from typing import Dict
from os.path import expanduser, join
import platform
from .version import VERSION
path = os.environ.get("DEPLY_CONFIG_FILE", join(expanduser("~"), ".deply/", "config"))
BASE_URL = "https://api.deplyai.com/v1"

def get_user_agent():
    default_ua = requests.utils.default_headers()['User-Agent']
    return f'DeplyCLI/{VERSION} ({platform.system()} {platform.release()}; {default_ua})'

class TokenAuthSession:
    def __init__(self, token):
        default_ua = requests.utils.default_headers()['User-Agent']
        self.headers = {'Authorization': f'Bearer {token}', 'User-Agent': get_user_agent()}
    
    def get(self, url, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)
        response = requests.get(url, headers=headers, **kwargs)
        return response
    
    def post(self, url, data=None, json=None, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)
        response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
        return response
    
    
    def delete(self, url, data=None, json=None, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)
        response = requests.delete(url, data=data, json=json, headers=headers, **kwargs)
        return response

    # Additional methods like put, delete can be added similarly

def get_current_profile_credentials() -> ProfileCredentials:
    profile = os.environ.get("DEPLY_PROFILE", "default")
    try:
        with open(path, "rb") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("Deply config file not found.")
        return None
    if 'profiles' not in config:
        logging.error("Deply config file is corrupt.")
        return None
    if profile not in config['profiles']:
        logging.error(f"Credentials for profile \"{profile}\" not found. Have you run \"deply auth login\" yet?")
        return None
    creds = config['profiles'][profile]
    for key in creds:
        creds[key] = str(creds[key])
    return ProfileCredentials(**creds).model_dump()
def set_profile_credentials(profile: str = 'default', credentials: Dict[str, str] = {}) -> None:
    creds_class = ProfileCredentials(**credentials).model_dump()
    try:
        with open(path, "rb") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {'profiles': {}}
    try:
        if 'profiles' not in config:
            config['profiles'] = {}
    except TypeError:
        config = {'profiles': {}} 
    config['profiles'][profile] = creds_class
    try:
        with open(path, "w") as f:
            f.write(yaml.safe_dump(config))
    except FileNotFoundError:
        mainpath = '/'.join(path.split("/")[:-1])
        os.mkdir(mainpath)
        with open(path, "w") as f:
            f.write(yaml.safe_dump(config))
    return
def delete_profile_credentials(profile: str = 'default') -> None:
    try:
        with open(path, "rb") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        return
    if config == None:
        return
    if 'profiles' not in config:
        config['profiles'] = {}
    del config['profiles'][profile]
    with open(path, "w") as f:
        f.write(yaml.safe_dump(config))
    return