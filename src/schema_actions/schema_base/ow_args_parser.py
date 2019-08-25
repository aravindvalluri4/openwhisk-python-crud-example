from io import BytesIO
import cgi
import base64
import logging

from .ow_args import Arguments

SCHEMA_RESOURCE_PATH = "/sm/schemas"


class ArgsParseException(Exception):
    """ Exception class for argument parsing """


class ArgsParser:
    """ Parse args passed to main func """

    def _parse_body(self, args, r):
        ctype, pdict = cgi.parse_header(args['__ow_headers']['content-type'])
        pdict['boundary'] = bytes(pdict['boundary']).encode("utf-8")

        if ctype == 'multipart/form-data':
            body = BytesIO(base64.b64decode(args['__ow_body']))
            fields = cgi.parse_multipart(body, pdict)
            r.name = fields['name'][0].decode("utf-8")
            r.title = fields['title'][0].decode("utf-8")
            r.file = fields['file'][0].decode("utf-8")

    def _parse_path(self, path, r):
        if path != SCHEMA_RESOURCE_PATH:
            r.model_from_path = path.split('/')[-1]

    def _parse_db_args(self, args, r):
        r.db_url = args['db_url']
        r.db_pass = args['db_pass']
        r.db_name = args['db_name']

    def parse(self, args):
        r = Arguments()
        try:

            if '__ow_body' in args:
                self._parse_body(args, r)

            if '__ow_path' in args:
                self._parse_path(args['__ow_path'], r)

            # parse db options
            self._parse_db_args(args, r)

        except Exception as e:
            logging.exception('ee')
            raise ArgsParseException('Failed to parse Args')
        return r
