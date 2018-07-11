from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # this ensures that the filename is not already used
        # when uploading a file
        self.delete(name)
        return name
