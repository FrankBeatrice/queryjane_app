from django.core.validators import BaseValidator
from django.utils.translation import ugettext as _


class FileSizeValidator(BaseValidator):
    """
    Validate a file size. Size must be given in Kb.
    """
    message = _('The file must have a maximum of 4MB')
    code = 'file_size'

    def compare(self, a, b):
        return a.size > 1024 * b
