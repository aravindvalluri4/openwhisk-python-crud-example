import logging

import consts
from schema_base import SchemaBase


class SchemaDeleter(SchemaBase):
    """ Delete Handler """

    def delete(self, args):
        try:
            self.initialize(args)
            schema = self.parsed_args.model_from_path
            if schema is None:
                msg = {"error": "No schema specified"}
                return self.get_http_response(msg, 500)
            else:
                return self._handle_delete_schema(schema)
        except Exception as e:
            logging.error(e)
            msg = {"error": consts.FAILED_TO_PROCESS_REQUEST}
            return self.get_http_response(msg, 500)
        finally:
            self.clean_up()

    def _handle_delete_schema(self, schema):
        """ handels delete schema """
        if self.does_schema_exists(schema):
            query = "delete from schemas where name='%s';" % schema
            self.db.execute_query(query)
            self.db.commit()
            return self.get_http_response(None, 204)
        else:
            data = {"error": schema + " Not Found"}
            return self.get_http_response(data, 400)
