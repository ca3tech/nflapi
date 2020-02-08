
class MissingDocumentException(Exception):
    def __init__(self, *args, **kwargs):
        super(MissingDocumentException, self).__init__(*args, **kwargs)