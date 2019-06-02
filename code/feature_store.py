import d6tflow
import pandas as pd


class TaskFeatureStore(d6tflow.tasks.TaskPqPandas):
    """
    Combines all the features which have been generated.
    """

    def requires(self):
        """Add new features here."""
        return dict()

    def run(self):
        """Concatenate generated features into large dataframes."""
        data = pd.concat(
            [i.load().drop(["train", "target"], axis=1) for i in self.input().values()],
            axis=1,
        )
        self.save(data)
