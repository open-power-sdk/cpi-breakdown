CPI Breakdown - CPI
========================

Cycles Per Instruction analysis can be used to improve application performance.
CPI refers to how many processor cycles are needed to complete an instruction. An instruction can be a read/write from memory operation, an arithmetic calculation, or bit-wise operation. The more cycles the processor takes to complete an instruction, the poorer the performance of the application in the processor. Application performance can be improved by decreasing the number of cycles that are needed for the processor to complete instructions. In the CPI breakdown model, a set of processor events is broken down into components. Processor performance counters calculate metrics for the event components. This approach provides a complete view of how the application behaves concerning processor performance. Because each processor architecture has different performance counters, POWER and Intel have different CPI breakdown models. Even within Power Systems servers, differences exist between each version of the processor. Processor performance can be measured by profiling the application with tools such as OProfile or Perf. The CPI breakdown tool automates this process, enabling you to access the CPI breakdown model of any C/C++ application without manually tracking the events and calculating the metrics.

CPI commands:

	record: collect and record the events used in the breakdown

	display: display the result of the data collected during the recording step

	drilldown: perform a drilldown execution for a specific event

	compare: compare the collected results of two CPI executions and provide feedback on performance variations

	info: show information about events and metrics

	For details about the usage of each command, see cpi <command> --help


Note for Integrators:

	CPI may return one of several error codes if it encounters problems.

	0: no problems occurred.

	1: generic error code.

	2: some dependency tool is missing


Building and Testing

Requirements:
	python-pip
	python-pylint
	python-virtualenv
	python-docsutil
	oprofile

Testing
	./dev cpi tests

Build
	./dev cpi release

Build and install
	./dev cpi install
