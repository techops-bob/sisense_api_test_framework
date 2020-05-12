import glob
import unittest


def suite():
    test_files = glob.glob('test_*.py')
    module_strings = [test_file[0:len(test_file) - 3] for test_file in test_files]
    suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
    suite = unittest.TestSuite()
    test_suite = unittest.TestSuite(suites)
    test_runner = unittest.TextTestRunner().run(test_suite)
    return suite

def load_tests(loader, tests, pattern):
    ''' Discover and load all unit tests in all files named ``*_test.py`` in ``./src/``
    '''
    suite = unittest.TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('src', pattern='*_tests.py'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite

if __name__ == '__main__':
    unittest.main()