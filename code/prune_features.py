import d6tflow
from tqdm.autonotebook import tqdm

from .feature_store import TaskFeatureStore


class TaskPruneFeatures(d6tflow.tasks.TaskPqPandas):
    persist = ["train_data", "test_data", "target"]

    def requires(self):
        return TaskFeatureStore()

    def run(self):
        train_data = self.input()["train_data"].load()
        target = self.input()["target"].load()
        test_data = self.input()["test_data"].load()

        # Remove constant features
        low_variance = (
            (train_data.var() < 1e-8)
            .to_frame("mask")
            .query("mask == True")
            .index.tolist()
        )
        train_data.drop(low_variance, axis=1, inplace=True)
        test_data.drop(low_variance, axis=1, inplace=True)

        # Remove duplicate features
        duplicates = list(
            set(train_data.columns).difference(train_data.T.drop_duplicates().T.columns)
        )
        train_data = train_data.drop(duplicates, axis=1)
        test_data = test_data.drop(duplicates, axis=1)

        # Remove highly correlated features
        correlated = []
        for i in tqdm(range(len(train_data.columns))):
            for j in range(i):
                if train_data.iloc[:, i].corr(train_data.iloc[:, j]) > 0.95:
                    correlated.append(j)
        correlated_features = [train_data.columns[i] for i in correlated]
        train_data = train_data.drop(correlated_features, axis=1)
        test_data = test_data.drop(correlated_features, axis=1)
        self.save({"train_data": train_data, "test_data": test_data, "target": target})
