from django import template

from entrepreneur.models import CompanyScore

register = template.Library()


@register.assignment_tag
def get_can_edit_company_score(user, score_user, company):
    """
    Used to check if current user has scored a company and
    if he is able to remove or edit his previus qualification.
    """
    if user != score_user:
        return False

    if CompanyScore.objects.filter(
        user=user,
        company=company,
    ):
        return True

    return False
