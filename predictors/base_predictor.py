from common.models import PredictionRequest, PredictionResponse


class BasePredictor:

    @staticmethod
    def name():
        raise NotImplementedError()

    @staticmethod
    def predict(request: PredictionRequest) -> PredictionResponse:
        raise NotImplementedError()
