class AdminPermissions(object):
    """
    Administrator users permissions.
    """
    @classmethod
    def can_manage_admin_views(self, user):
        if user.is_staff:
            return True

        return False

    @classmethod
    def can_share_company_twitter(self, user, company):
        if not company.is_active or company.shared_on_twitter:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_share_job_twitter(self, user, job):
        if not job.is_active or job.shared_on_twitter:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_hide_company(self, user, company):
        if company.is_inactive or company.is_hidden:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_activate_company(self, user, company):
        if not company.is_hidden:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_hide_job_offer(self, user, job_offer):
        if job_offer.is_closed or job_offer.is_hidden:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_activate_job_offer(self, user, job_offer):
        if not job_offer.is_hidden:
            return False

        if user.is_staff:
            return True

        return False
