class Arguments:
    def __init__(self):
        # db data
        self.db_url = None
        self.db_pass = None
        self.db_name = None

        # schema data
        self.name = None
        self.title = None
        self.file = None

        # path
        self.model_from_path = None

    def __repr__(self):
        data = [self.db_url,
                self.db_pass,
                self.db_name,
                self.name,
                self.title,
                self.file,
                self.model_from_path]
        return repr(data)
