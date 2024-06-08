# cmd.py

"""
Commandline parser
"""


import logging
import argparse
from .auth import AuthHandler
from .pipelines import PipelineHandler
import sys

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USAGE_HEAD = '''\
deply <property> <action> [<args>]

Supported properties are:
    pipeline       Manage pipelines
    stages         Manage pipeline stages
    auth           Manage API authentication
'''

prop_matcher = {
    'auth': AuthHandler,
    'pipelines': PipelineHandler
}

def commandline_parser(unparsed_args: None or list = None):
    """
    Parse the first argument and call the right handler
    :param unparsed_args: Unparsed arguments
    :return: Nothing
    """
    parser = argparse.ArgumentParser(
        prog='deply',
        description='DeplyAI CLI Tool',
        usage=USAGE_HEAD,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'property', type=str, help='Property going to take action', choices=list(prop_matcher.keys()))
    prop = str(parser.parse_args(unparsed_args[0:1]).property).lower()
    if prop in prop_matcher:
        handler = prop_matcher[prop]()
        handler.run(unparsed_args[1:])
    else:
        print(f"Unknown property \"{prop}\".", flush=True, file=sys.stderr)