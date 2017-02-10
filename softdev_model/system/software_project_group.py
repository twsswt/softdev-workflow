import time

from . import CentralisedVCSServer, SoftwareProject
from . import SoftwareSystem

from theatre_ag import SynchronizingClock, Team


class SoftwareProjectGroup(object):

    def __init__(self, plan, random, number_of_developers, number_of_clock_ticks, number_of_projects, number_of_traces,
                 max_trace_length):

        self.number_of_traces = number_of_traces
        self.max_trace_length = max_trace_length

        self.software_projects = list()

        for seed in range(0, number_of_projects):

            clock = SynchronizingClock(number_of_clock_ticks)

            development_team = Team(clock)

            for logical_name in range(0, number_of_developers):
                development_team.add_member(logical_name)

            centralised_vcs_server = CentralisedVCSServer(SoftwareSystem())

            software_project = SoftwareProject(clock, development_team, plan, centralised_vcs_server, random)

            self.software_projects.append(software_project)

        self.simulation_duration = -1

    def build_and_operate(self):
        start_time = time.time()
        for software_project in self.software_projects:
            software_project.build()
            software_project.deploy_and_operate(self.number_of_traces, self.max_trace_length)

        self.simulation_duration = time.time() - start_time

    def _average_project_attribute(self, attr):
        return reduce(lambda x, y: x + y, map(attr, self.software_projects), 0) / len(self.software_projects)

    @property
    def average_project_mean_time_to_failure(self):
        return self._average_project_attribute(lambda p: p.last_deployment.mean_operations_to_failure)

    @property
    def average_project_remaining_developer_time(self):
        return self._average_project_attribute(lambda p: p.project_duration)

    @property
    def average_project_features_implemented(self):
        return self._average_project_attribute(lambda p: 1.0 * len(p.last_deployment.features))