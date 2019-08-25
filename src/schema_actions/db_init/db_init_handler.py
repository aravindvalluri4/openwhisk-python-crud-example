import os
import logging

from schema_base import SchemaBase


class SchemDBInit(SchemaBase):
    """ Table and init handler """

    def init(self, args):
        """ initialize tables """
        try:
            self.initialize(args)
            script = os.path.abspath("create-tables.sql")
            self.db.execute_sql(script)
            return {"message": "Schema DB initialized successfully"}
        except Exception as e:
            logging.error(e)
            return {"message": "Failed to initialized DB"}
        finally:
            self.clean_up()
