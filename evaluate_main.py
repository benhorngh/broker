import evaluate
from predictors.p_gradient_boosting import GradientBoostingPredictor
from predictors.p_linear_regression import LinearRegressionPredictor
from predictors.p_prophet import ProphetPredictor
from predictors.p_random import RandomPredictor
from predictors.p_random_forest import RandomForestPredictor
from predictors.p_random_plan import RandomPlanPredictor


def evaluate_predictor():
    evaluate.eval_one_predictor(RandomPredictor)


def evaluate_predictors():
    evaluate.compare_predictors(
        [
            RandomForestPredictor,
            ProphetPredictor,
            GradientBoostingPredictor,
            LinearRegressionPredictor,
        ]
    )
    # evaluate.compare_predictors([RandomPredictor, RandomPlanPredictor])


if __name__ == "__main__":
    evaluate_predictors()
