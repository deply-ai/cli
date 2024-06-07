# login.py

"""
Wrapper to manage pipelines with the Deply API
"""

import argparse, yaml
from .util import get_current_profile_credentials
from deplyai._schema import Pipeline
from .util import TokenAuthSession, BASE_URL
import json

CREATE_USAGE_HEAD: str = '''\
deply pipeline create <options>
'''

DELETE_USAGE_HEAD: str = '''\
deply pipeline create <options>
'''

USAGE_HEAD: str = '''\
deply pipeline <verb> <options>
'''

USAGE_EXAMPLES: str = '''\
Examples:

deply pipeline create --filename pipeline.yml
deply pipeline delete --id 1
'''

class PipelineDeleteHandler(object):
    """
    Handler for pipeline delete commands
    """
    def __init__(self):
        self.auth = get_current_profile_credentials()
        if not self.auth:
            return
        self.tenant = self.auth['tenant']
        self.auth_session = TokenAuthSession(self.auth['token'])
    def run(self, args: argparse.Namespace):
        """
        Parse and execute the command
        :param unparsed_args: Unparsed arguments for this property
        :return: Nothing
        """
        if not self.auth:
            return
        pipeline_id = args.pipeline_id
        response = self.auth_session.delete(f"{BASE_URL}/tenants/{self.tenant}/pipelines/{pipeline_id}")
        print(json.dumps(response.json(), indent=4, sort_keys=True))


class PipelineCreateHandler(object):
    """
    Handler for pipeline create commands
    """
    def __init__(self):
        self.auth = get_current_profile_credentials()
        if not self.auth:
            return
        self.tenant = self.auth['tenant']
        self.auth_session = TokenAuthSession(self.auth['token'])
    def run(self, args: argparse.Namespace):
        """
        Parse and execute the command
        :param unparsed_args: Unparsed arguments for this property
        :return: Nothing
        """
        if not self.auth:
            return
        with open(args.filename, "rb") as f:
            pipeline = yaml.safe_load(f)
        pipeline_json: str = Pipeline(**pipeline).model_dump()
        response = self.auth_session.post(f"{BASE_URL}/tenants/{self.tenant}/pipelines", json=pipeline_json)
        print(json.dumps(response.json(), indent=4, sort_keys=True))


class PipelineHandler(object):
    """
    Handler for pipeline commands
    """
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='deply pipeline',
            description='Manage pipelines via the DeplyAI API',
            usage=USAGE_HEAD,
            epilog=USAGE_EXAMPLES,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subparsers = self.parser.add_subparsers(dest='verb', description='available actions')

        self.create_parser = subparsers.add_parser('create')
        self.create_parser.add_argument('--filename', type=str, help='The file contaning the pipeline specification YAML', dest='filename', required=True)

        self.delete_parser = subparsers.add_parser('delete')
        self.delete_parser.add_argument('--pipeline-id', type=str, help='The pipeline ID to delete', dest='pipeline_id', required=True)

    def run(self, unparsed_args: list):
        """
        Parse and execute the command
        :param unparsed_args: Unparsed arguments for this property
        :return: Nothing
        """
        args: argparse.Namespace = self.parser.parse_args(unparsed_args)
        match args.verb:
            case 'create':
                PipelineCreateHandler().run(args)
            case 'delete':
                PipelineDeleteHandler().run(args)
            case _:
                self.parser.print_help()
