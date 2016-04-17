"""
@author: twsswt
"""

from fuzzi_moss import *

from softdev_model.system import BugEncounteredException, DeveloperExhaustedException


class TestDrivenDevelopment(object):
    """
    Represents the sequence of activities in a tests driven development workflow.
    """
    def __init__(self,
                 target_test_coverage_per_feature=1.0,
                 target_dependencies_per_feature=0):

        self.target_test_coverage_per_feature = target_test_coverage_per_feature
        self.target_dependencies_per_feature = target_dependencies_per_feature

    @fuzz(remove_last_step)
    def work(self, random, software_system, developer, schedule):
        # Complete main tasks.
        for feature_size in schedule:
            try:
                feature = software_system.add_feature(feature_size)
                self._ensure_sufficient_tests(developer, feature)
                self._complete_feature(random, developer, feature)
                self._refactor_feature(random, developer, feature)
            except DeveloperExhaustedException:
                software_system.features.remove(feature)

        # Work in wider quality assurance.
        while True:
            try:
                feature = random.choice(software_system.features)
                self._enhance_system_quality(random, feature, developer)
            except DeveloperExhaustedException:
                break

    def _ensure_sufficient_tests(self, developer, feature):
        while feature.test_coverage < self.target_test_coverage_per_feature:
            developer.add_test(feature)

    def _complete_feature(self, random, developer, feature):
        while not feature.is_implemented:
            developer.extend_feature(random, feature)
            self._debug_feature(random, developer, feature)

    def _enhance_system_quality(self, random, feature, developer):
        developer.add_test(feature)
        self._debug_feature(random, developer, feature)
        self._refactor_feature(random, developer, feature)

    @staticmethod
    def _debug_feature(random, developer, feature):
        while True:
            try:
                feature.exercise_tests()
                break
            except BugEncounteredException as e:
                developer.debug(random, feature, e.bug)

    def _refactor_feature(self, random, developer, feature):
        while len(feature.dependencies) > self.target_dependencies_per_feature:
            developer.refactor(random, feature)
