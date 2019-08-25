from schema_base import SchemaBase


class SchemaPoster(SchemaBase):
    """ Post Handler """

    def post(self, args):
        try:
            self.initialize(args)
            schema_name = self.parsed_args.name
            title = self.parsed_args.title
            schema = self.parsed_args.file
            return self._handle_post_schema(schema_name,
                                            title,
                                            schema)
        except Exception as e:
            msg = {"error": str(e)}
            return self.get_http_response(msg, 500)
        finally:
            self.clean_up()

    def _handle_post_schema(self, schema_name, title, schema):
        if self.does_schema_exists(schema_name):
            data = {"error": schema + " Schema Already Exists"}
            return self.get_http_response(data, 409)
        else:
            query = "insert into schemas values ('%s');" % schema_name
            self.db.execute_query(query)
            self.db.commit()
            return self.get_http_response(None, 201)
