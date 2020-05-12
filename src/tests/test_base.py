import pytest

from src.tests.dashboard import Dashboard


class TestBase:

    def pytest_sessionstart(session):
        session.results = dict()

    # @pytest.mark.smoke
    def test_utilisation_country_sisense(self):
        Dashboard().api_checks_for_dashboard("dashboard_name")

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        result = outcome.get_result()
        if result.when == 'call':
            item.session.results[item] = result
            print("#############")
            print("Result" + str(item.session.results[item]))
            print("#############")

