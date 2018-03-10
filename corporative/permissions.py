class AdminPermissions(object):
    @classmethod
    def can_manage_admin_views(self, user):
        if user.is_staff:
            return True

        return False

    @classmethod
    def can_share_venture_twitter(self, user, venture):
        if not venture.is_active or venture.shared_on_twitter:
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
    def can_hide_venture(self, user, venture):
        if venture.is_inactive or venture.is_hidden:
            return False

        if user.is_staff:
            return True

        return False

    @classmethod
    def can_activate_venture(self, user, venture):
        if not venture.is_hidden:
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
