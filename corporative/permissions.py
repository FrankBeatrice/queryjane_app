class AdminPermissions(object):
    @classmethod
    def can_manage_admin_views(self, user):
        if user.is_staff:
            return True

        return False
