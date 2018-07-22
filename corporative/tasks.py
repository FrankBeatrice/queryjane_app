from django.conf import settings
from twython import Twython

from huey.contrib.djhuey import task


@task(retries=0, retry_delay=60 * 10)
def share_company_on_twitter(company):
    """
    Asynchronous task to share a company in the
    offical Qjane Twitter page.
    """
    twitter = Twython(
        settings.TWITTER_APP_KEY,
        settings.TWITTER_APP_SECRET,
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_TOKEN_SECRET,
    )

    hashtags = '#cannabiscompany #cannabisindustry #cannabiscommunity'

    text = 'Cannabis companies | take a look at {0} #cannabis {1} {2}'.format(
        company,
        hashtags,
        settings.BASE_URL + company.get_absolute_url(),
    )

    twitter.update_status(status=text)
    company.shared_on_twitter = True
    company.save()


@task(retries=0, retry_delay=60 * 10)
def share_job_on_twitter(job):
    """
    Asynchronous task to share a job offer in the
    offical Qjane Twitter page.
    """
    twitter = Twython(
        settings.TWITTER_APP_KEY,
        settings.TWITTER_APP_SECRET,
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_TOKEN_SECRET,
    )

    hashtags = '#cannabisjobs #cannabisindustry #cannabiscommunity'

    text = 'Cannabis jobs | {0} - {1} #cannabis {2} {3}'.format(
        job,
        job.venture,
        hashtags,
        settings.BASE_URL + job.get_absolute_url(),
    )

    twitter.update_status(status=text)
    job.shared_on_twitter = True
    job.save()
