"""
Very competition-specific.
"""

import d6tflow
import luigi

from .prune_features import TaskPruneFeatures
from .configs import include, exclude


class TaskSelectFeatures(d6tflow.tasks.TaskPqPandas):
    persist = ["train_data", "test_data", "target"]
    include = luigi.ListParameter(default=include)
    exclude = luigi.ListParameter(default=exclude)

    def requires(self):
        return TaskPruneFeatures()

    def run(self):
        train_data = self.input()["train_data"].load()
        target = self.input()["target"].load()
        test_data = self.input()["test_data"].load()
        to_keep = [i for i in self.include if i not in self.exclude]
        train_data = train_data[to_keep]
        test_data = test_data[to_keep]
        self.save({"train_data": train_data, "test_data": test_data, "target": target})
