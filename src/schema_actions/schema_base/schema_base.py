import json
import logging

from .ow_args_parser import ArgsParser
from .db_connection import DbConnection


class SchemaBase:
    """ Has common functions for all actions """

    def initialize(self, args):
        self._parse(args)
        self._connect_db()

    def clean_up(self):
        if self.db:
            self.db.close()

    def does_schema_exists(self, schema):
        """ check if schema exits """
        query = "select name from schemas where name='%s';" % schema
        rows = self.db.execute_query(query)
        if not rows:
            return False
        return True

    def get_http_response(self, msg, code):
        logging.info('Send back replycode '+str(code))
        if msg is None:
            return {
                       'headers': {
                           'Content-Type': 'application/json'
                       },
                       'statusCode': code,
                   }

        return {
                   'headers': {
                       'Content-Type': 'application/json'
                    },
                    'statusCode': code,
                    'body': json.dumps(msg)
               }

    def _connect_db(self):
        """ Connect to database"""
        self.db = DbConnection(host=self.parsed_args.db_url,
                               password=self.parsed_args.db_pass,
                               dbname=self.parsed_args.db_name)

    def _parse(self, args):
        self.parsed_args = ArgsParser().parse(args)
        logging.info('successfully parsed args')
