# login.py

"""
Wrapper to authenticate to the Deply API
"""

import argparse, requests, sys, subprocess, os
from .util import delete_profile_credentials, set_profile_credentials
import time
USAGE_HEAD: str = '''\
deply auth <verb> <options>
'''

USAGE_EXAMPLES: str = '''\
Examples:

deply auth login
deply auth login --profile examplecorp
deply auth logout --profile examplecorp
'''
def discover_tenant(bearer_token: str):
    """
    Maps Auth0 tenant ID to DeplyAI tenant ID.

    Args:
    bearer_token (str): Bearer token to discover tenant for.

    Returns:
    dict: A dictionary with the response data or error message.
    """
    url = 'https://api.deplyai.com/v1/discovery'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {bearer_token}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error responses
        return response.json()  # Return the JSON response if the request was successful
    except requests.exceptions.HTTPError as http_err:
        return {'error': str(http_err)}
    except Exception as err:
        return {'error': str(err)}


def poll_token_endpoint(device_code,timeout):
    while True:
        response = requests.get(f"https://api.deplyai.com/oauth/token?device_code={device_code}",)
        response_data = response.json()
        if response_data.get('done') == True:
            return response_data  # Token received
        elif response_data.get('done') == False:
            time.sleep(timeout)
        else:
            print('Unexpected error:', response_data.get('error'))
            break

def post_device_code():
    """
    Posts a request to get a device code for OAuth.

    Args:
    client_id (str): The Client ID for the OAuth application.

    Returns:
    dict: A dictionary with the response data or error message.
    """
    url = 'https://api.deplyai.com/oauth/device/code'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP error responses
    return response.json()  # Return the JSON response if the request was successful

class AuthHandler(object):
    """
    Handler for authentication commands
    """
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='deply auth',
            description='Authenticate to the DeplyAI API',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument('verb', type=str, help='The action to take', choices=['login', 'logout'])
        self.parser.add_argument('--profile', type=str, help='The profile to store credentials for', dest='profile', default=os.environ.get("DEPLY_PROFILE", "default"))
        self.parser.add_argument('--token', type=str, help='Organization Access Token value (if authenticating silently)', dest='token')
    def run(self, unparsed_args: list):
        """
        Parse and execute the command
        :param unparsed_args: Unparsed arguments for this property
        :return: Nothing
        """
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        profile = args.profile
        match args.verb:
            case 'login':
                print(f"Authenticating user to profile \"{profile}\"...")
                if args.token != None:
                    try:
                        print("Authenticating using provided token...")
                        discovery_data = discover_tenant(args.token)
                        tenant = int(discovery_data['tenant_id'])
                        set_profile_credentials(profile=profile, credentials={
                            "token": args.token, 
                            "id_token": args.token, 
                            "tenant": tenant
                        })
                        print("Authentication complete!")
                    except:
                        print("Recieved tokens but could not complete authentication process. Please try again.")
                else:
                    data = post_device_code()
                    device_code = data['device_code']
                    verification_uri_complete = data['verification_uri_complete']
                    polling_interval = data['interval']
                    print(
    f"""
    Attempting to automatically open the authentication page in your default browser.
    If the browser does not open, open the following URL:

    {verification_uri_complete}

    and complete the authentication steps.
    """
                    )
                    try:
                        if sys.platform=='win32':
                            os.startfile(verification_uri_complete)
                        elif sys.platform=='darwin':
                            subprocess.Popen(['open', verification_uri_complete])
                        else:
                            subprocess.Popen(['xdg-open', verification_uri_complete])
                    except:
                        pass
                    token_response = poll_token_endpoint(device_code, timeout=polling_interval)
                    if 'access_token' in token_response and 'id_token' in token_response:
                        try:
                            print("Finishing up...")
                            discovery_data = discover_tenant(token_response['access_token'])
                            tenant = int(discovery_data['tenant_id'])
                            set_profile_credentials(profile=profile, credentials={
                                "token": token_response['access_token'], 
                                "id_token": token_response['id_token'], 
                                "tenant": tenant
                            })
                            print("Authentication complete!")
                        except:
                            print("Recieved tokens but could not complete authentication process. Please try again.")
                    else:
                        print('Failed to retrieve access token:', token_response.get('message'))
            case 'logout':
                print(f"Logging out of profile \"{profile}\"...")
                delete_profile_credentials(profile=profile)