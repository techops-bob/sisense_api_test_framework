def pytest_generate_tests(metafunc):
    argnames = []
    idlist = []
    argvalues = []
    for testdata in metafunc.cls.testdata:
        idlist.append(testdata[0])
        items = testdata[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


def pytest_html_report_title(report):
    report.title = "Sisense API regression test for utilisation"


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        # data.append(html.div('No log output captured.', class_='empty log'))
