from src.utils.Utilities import Utilities

comparator_obj = Utilities().init_test_data('dashboard')


class TestDashbaord:
    testdata = comparator_obj

    def test_widget(self, attribute):
        attribute.get_big_query_and_sisense_result('widget')

