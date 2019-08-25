import logging

import consts
from schema_base import SchemaBase


class SchemaFetcher(SchemaBase):
    """ Handles service logic for schema get """

    def fetch(self, args):
        try:
            self.initialize(args)
            schema = self.parsed_args.model_from_path
            if schema is None:
                return self._handle_get_schemas()
            else:
                return self._handle_get_schema(schema)
        except Exception as e:
            logging.error(e)
            msg = {"error": consts.FAILED_TO_PROCESS_REQUEST}
            return self.get_http_response(msg, 500)
        finally:
            self.clean_up()

    def _handle_get_schema(self, schemaName):
        """ handels individual schema """
        if self.does_schema_exists(schemaName):
            data = {"schema": schemaName, "title": "some schema title"}
            return self.get_http_response(data, 200)
        else:
            data = {"error": schemaName + " Not Found"}
            return self.get_http_response(data, 400)

    def _handle_get_schemas(self):
        """gets all schemas """
        query = 'select name from schemas;'
        rows = self.db.execute_query(query)
        data = {"schemas": self._process_rows(rows)}
        return self.get_http_response(data, 200)

    def _process_rows(self, rows):
        if rows:
            # ye, i used list comprehension :-)
            return [schema for row in rows for schema in row]
        else:
            return []
