from django.test.runner import DiscoverRunner


class NoChecksRunner(DiscoverRunner):
    # Django 1.11 runs checks before running tests, which causes our urls.py to be loaded before we
    # register our file pickers. This turns that functionality off.

    def run_checks(self):
        pass
