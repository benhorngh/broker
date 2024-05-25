import evaluate
from old.predictors.p_autots import AutoTSPredictor
from old.predictors.p_democrat import DemocratPredictor
from old.predictors.p_gradient_boosting import GradientBoostingPredictor
from old.predictors.p_linear_regression import LinearRegressionPredictor
from old.predictors.p_prophet import ProphetPredictor
from old.predictors.p_random import RandomPredictor
from old.predictors.p_random_forest import RandomForestPredictor
from old.predictors.p_random_plan import RandomPlanPredictor


def evaluate_predictor():
    evaluate.eval_one_predictor(AutoTSPredictor)


def evaluate_predictors():
    evaluate.compare_predictors(
        [
            DemocratPredictor,
            RandomForestPredictor,
            ProphetPredictor,
            GradientBoostingPredictor,
            LinearRegressionPredictor,
            AutoTSPredictor,
            RandomPredictor,
            RandomPlanPredictor,
        ]
    )


if __name__ == "__main__":
    evaluate_predictors()
# TODO find a good ranking system for comparing predictors, and track predictors ranking
# TODO compare managers rather than predictors
# TODO add "careful" manager, investing only with high level of sureness and high expected gross
