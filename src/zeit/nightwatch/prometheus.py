import prometheus_client


def addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--prometheus', action='store_true', default=False,
        help='Send metrics to prometheus')
    group.addoption(
        '--prometheus-pushgateway-url',
        default='https://prometheus-pushgw.ops.zeit.de',
        help='Push Gateway URL to send metrics to')
    group.addoption(
        '--prometheus-metric-name', default='nightwatch_check',
        help='Name for prometheus metrics, can contain {funcname} placeholder')
    group.addoption(
        '--prometheus-extra-labels', action='append',
        help='Extra labels to attach to reported metrics')
    group.addoption(
        '--prometheus-job-name', default='unknown',
        help='Value for the "job" key in exported metrics')


def configure(config):
    if config.option.prometheus_extra_labels is None:
        config.option.prometheus_extra_labels = []
    config.option.prometheus_extra_labels.append(
        'environment=%s' % config.getoption('--nightwatch-environment'))

    config._prometheus = PrometheusReport(config)
    config.pluginmanager.register(config._prometheus)


def unconfigure(config):
    if getattr(config, '_prometheus', None) is not None:
        config.pluginmanager.unregister(config._prometheus)
        del config._prometheus


class PrometheusReport:

    SUCCESSFUL_OUTCOMES = ['passed', 'skipped']

    def __init__(self, config):
        self.config = config
        self.registry = prometheus_client.CollectorRegistry()
        self.metrics = {}

    def pytest_runtest_logreport(self, report):
        if report.when != 'call':
            return
        opt = self.config.option
        labels = dict(x.split('=') for x in opt.prometheus_extra_labels)
        labels['test'] = report.location[2]
        name = opt.prometheus_metric_name.format(funcname=report.location[2])
        if 'name' not in self.metrics:
            self.metrics['name'] = prometheus_client.Gauge(
                name, '', labels.keys(), registry=self.registry)
        self.metrics['name'].labels(**labels).set(
            1 if report.outcome in self.SUCCESSFUL_OUTCOMES else 0)

    def pytest_sessionfinish(self, session):
        opt = self.config.option
        if opt.verbose > 0:
            print('\n' + prometheus_client.generate_latest(
                self.registry).decode('utf-8'))
        if not opt.prometheus:
            return
        prometheus_client.push_to_gateway(
            opt.prometheus_pushgateway_url, job=opt.prometheus_job_name,
            registry=self.registry)
