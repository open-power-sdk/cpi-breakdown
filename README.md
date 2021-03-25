# Project Description

CPI refers to how many processor cycles are needed to complete an instruction. An instruction can be a read/write from memory operation, an arithmetic calculation, or bit-wise operation. The more cycles the processor takes to complete an instruction, the poorer the performance of the application in the processor. Application performance can be improved by decreasing the number of cycles that are needed for the processor to complete instructions. In the CPI breakdown model, a set of processor events is broken down into components. Processor performance counters calculate metrics for the event components. This approach provides a complete view of how the application behaves concerning processor performance. The CPI breakdown tool automates this process, enabling you to access the CPI breakdown model of any C/C++ application on POWER without manually tracking the events and calculating the metrics.

For more information about CPI usage, see cpi --help

## Contributing to the project
We welcome contributions to the CPI Project in many forms. There's always plenty to do! Full details of how to contribute to this project are documented in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainers
The project's [maintainers](MAINTAINERS.txt): are responsible for reviewing and merging all pull requests and they guide the over-all technical direction of the project.

## Communication <a name="communication"></a>
We use [Slack](https://toolsforpower.slack.com/) for communication.

## Supported Architecture and Operating Systems
ppc64le: Ubuntu 16.04, CentOS7, RHEL 7.3, SLES12, Fedora 25.

## Installing
Requirements: python-pip, python-pylint, python3-venv, python-docsutil, oprofile

Testing: ./dev tests

Build: ./dev release

Build and install: ./dev install

Execution: cpi --help

## Documentation

usage: cpi [-h] [-V] {record,display,drilldown,compare,info} ...

record: collect and record the events used in the breakdown

display: display the result of the data collected during the recording step

drilldown: perform a drilldown execution for a specific event

compare: compare the collected results of two CPI executions and provide feedback on performance variations

info: show information about events and metrics

For details about the usage of each command, see cpi <command> --help

## Still Have Questions?
For general purpose questions, please use [StackOverflow](http://stackoverflow.com/questions/tagged/toolsforpower).

## License <a name="license"></a>
The CPI Breakdown Project uses the [Apache License Version 2.0](LICENSE) software license.

## Related information
[CPI Breakdown for Eclipse] (http://ieeexplore.ieee.org/document/6597191/)
