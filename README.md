Common things to every competition which absolutely need to be in here:

- a file to combine generate features. The feature generation files should be competition-specific.
- a file to remove useless features. I would never want duplicated, highly correlated, or constant
features, so this, again, can be general.
- a file to combine models. Perhaps training/optimising should be left to each competition
separately, but at least combining them should be done in the same way.
- a file to stack and submit. Again, I guess this can be quite generic?

Rather than faffing about with different datasets, just save everything together in one big
dataframe. There should be:
- columns with features
- column identifying whether row is in train or test
- column for target (which will be NaN in test)

Should be very easy to include or exclude features.
Idea: keep everything that's in include that is not in exclude.

If possible, I don't want to have to do any stacking / hyperparameter optimisation. That stuff is
boring AF. It seems that great ideas are always from features, anyway. I don't want to waste time
with shit that's gonna get automated in a few years anyway.

The only reservation I have about h2oautoml is the custom metric. Oh well, I might just have to
use a generic lgbm with early stopping, into which I can pass whatever custom metric I want. And
then, not use early stopping. Ah, but I need to have good sample weights somehow...how to do this
...I should try passing in my own completely different custom scorer, to see how it does.

Before you use any real data, make sure you have travis CI and pytest set up.