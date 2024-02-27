import evaluate
from predictors.p_autots import AutoTSPredictor
from predictors.p_democrat import DemocratPredictor
from predictors.p_gradient_boosting import GradientBoostingPredictor
from predictors.p_linear_regression import LinearRegressionPredictor
from predictors.p_prophet import ProphetPredictor
from predictors.p_random import RandomPredictor
from predictors.p_random_forest import RandomForestPredictor
from predictors.p_random_plan import RandomPlanPredictor


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
