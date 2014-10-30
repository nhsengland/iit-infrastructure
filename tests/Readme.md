Testing NHS England
===================

Install / Setup
---------------

To install dependencies run the following command:

```
   pip install -r requirements.txt
```

Usage Instructions
------------------

Web Tests
---------

To execute web tests, run `nosetests` from the test directory

Peformance Tests
----------------

http://testutils.org/multi-mechanize

Each test project contains the following:
config.cfg: configuration file. set your test options here.
test_scripts/: directory for virtual user scripts. add your test scripts here.
results/: directory for results storage. a timestamped directory is created for each test run, containing the results report.

Install matplotlib to generate graphs as part of results.html

```
   pip install matplotlib
```

Run a Project

Run a test project with multimech-run:
``` $ multimech-run CKAN ```

a timestamped results directory is created for each test run, containing the results report.

Configuration
-------------

Minimal Configuration

Here is a sample config.cfg file showing minimal options, defining 1 group of virtual users:

```
    [global]
    run_time = 100
    rampup = 100
    results_ts_interval = 10

    [user_group-1]
    threads = 10
    script = vu_script.py
```

Full Configuration

Here is a the project config.cfg file, defining 2 groups of virtual users:

```
    [global]
    run_time = 600
    rampup = 300
    results_ts_interval = 10
    progress_bar = on
    console_logging = off
    xml_report = off

    [user_group-1]
    threads = 50
    script = ckan_homepage.py

    [user_group-2]
    threads = 50
    script = ckan_search.py
```

Global Options

The following settings/options are available in the [global] config section:

```
run_time: duration of test (seconds) [required]
rampup: duration of user rampup (seconds) [required]
results_ts_interval: time series interval for results analysis (seconds) [required]
progress_bar: turn on/off console progress bar during test run [optional, default = on]
console_logging: turn on/off logging to stdout [optional, default = off]
xml_report: turn on/off xml/jtl report [optional, default = off]
results_database: database connection string [optional]
post_run_script: hook to call a script at test completion [optional]
```

User Groups

The following settings/options are available in each `[user_group-*]` config section:

```
threads: number of threads/virtual users
script: virtual user test script to run
```
