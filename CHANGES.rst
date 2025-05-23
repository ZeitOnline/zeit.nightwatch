zeit.nightwatch changes
=======================

.. towncrier release notes start

2.3.2 (2025-04-11)
------------------

Changes
+++++++

- Correctly determine prometheus job name from environment variables (prometheus)


2.3.1 (2025-04-08)
------------------

Changes
+++++++

- Also wait for return_url redirect after playwright sso login (ssowait)


2.3.0 (2025-04-03)
------------------

Changes
+++++++

- Wait for /konto redirect after playwright sso login (ssowait)


2.2.0 (2024-12-13)
------------------

Changes
+++++++

- Record prometheus metric on setup/teardown failure (prometheus)


2.1.0 (2024-12-13)
------------------

Changes
+++++++

- Set project label and job name automatically from k8s namespace environment variable (prometheus)


2.0.0 (2024-12-13)
------------------

Changes
+++++++

- Breaking change: Projects have to set base_url via a fixture now, setting nightwatch_config["selenium"] was removed due to unreliability (playwright)
- Remove selenium support (selenium)


1.11.0 (unreleased)
-------------------

- Nothing changed yet.


1.10.0 (2024-12-13)
-------------------

- Add our own `gcs-upload` helper script, since gsutil does not support gcloud auth anymore


1.9.2 (2024-12-12)
------------------

- Add infrastructure support for generating HTML reports and upload them to GCS


1.9.1 (2024-06-04)
------------------

- Apply convenience playwright Page.sso_login monkeypatch at import-time


1.9.0 (2024-06-04)
------------------

- Support keycloak for SSO


1.8.0 (2024-05-13)
------------------

- Also log HTTP response body, not just headers.


1.7.1 (2023-12-13)
------------------

- Don't try to json report if no argument was given


1.7.0 (2023-12-08)
------------------

- Implement ``--json-report=-`` for line-based output


1.6.0 (2022-12-16)
------------------

- Support playwright


1.5.1 (2022-06-24)
------------------

- Use non-deprecated selenium API


1.5.0 (2022-03-25)
------------------

- Support `selenium-wire` in addition to `selenium`


1.4.2 (2022-02-21)
------------------

- ZO-712: Set referer explicitly during sso_login, required for csrf validation


1.4.1 (2021-10-27)
------------------

- Include tests & setup in tarball to support `devpi test`


1.4.0 (2021-10-26)
------------------

- Add patch to requests


1.3.3 (2021-04-01)
------------------

- Support contains instead of equals for `find_link`


1.3.2 (2021-02-18)
------------------

- Record skipped tests as passed to prometheus, not failed


1.3.1 (2021-02-17)
------------------

- Handle same metric name (and testname only as label) correctly


1.3.0 (2021-02-17)
------------------

- Allow to configure the test browsers via a config fixture


1.2.0 (2021-02-17)
------------------

- Add convenience `nightwatch` fixture and toplevel API

- Add first test & fix package setup


1.1.0 (2021-02-12)
------------------

- Include prometheus functionality here, to fix pushgateway bug
  and support sending the test name as a label.

- Declare namespace package properly


1.0.0 (2021-02-11)
------------------

- Initial release
