from _pytest.junitxml import mangle_test_address
from datetime import datetime, timezone
import json
import sys


def addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--json-report',
        help='Write json lines report to given filename, or stdout if `-`')


def configure(config):
    if not config.option.json_report:
        return
    config.option.color = 'no'
    config.stash[JSONLinesReport.__name__] = JSONLinesReport(
        config.option.json_report)
    config.pluginmanager.register(config.stash[JSONLinesReport.__name__])


def unconfigure(config):
    if JSONLinesReport.__name__ in config.stash:
        config.pluginmanager.unregister(config.stash[JSONLinesReport.__name__])
        del config.stash[JSONLinesReport.__name__]


class JSONLinesReport:

    def __init__(self, output):
        self.output = output
        self.records = []

    def pytest_sessionfinish(self):
        if self.output == '-':
            out = sys.stdout
            out.write('\n')
        else:
            out = open(self.output, 'w')
        for row in self.records:
            out.write(json.dumps(row) + '\n')

    def pytest_runtest_logreport(self, report):
        names = mangle_test_address(report.nodeid)
        row = {
            'time': datetime.now(timezone.utc).isoformat(),

            'test_stage': report.when,
            'test_class': '.'.join(names[:-1]),
            'test_name': names[-1],

            'test_outcome': report.outcome,
            'test_failure': str(report.longrepr),

            'system_out': report.capstdout,
            'system_err': report.capstderr,
            'system_log': report.caplog,
        }

        remove = []
        for key, value in row.items():
            if not value or value == 'None':
                remove.append(key)
        for key in remove:
            del row[key]

        wanted = False  # Adapted from _pytest.junitxml logreport
        if report.passed:
            wanted = report.when == 'call'
        elif report.failed:
            wanted = True
        elif report.skipped:
            wanted = True
        if wanted:
            self.records.append(row)
