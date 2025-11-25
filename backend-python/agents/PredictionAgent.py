# PredictionAgent.py
# Agent responsible for generating predictions based on input data

class PredictionAgent:
    def __init__(self):
        self.name = "PredictionAgent"
        self.models = {}

    def register_model(self, model_name: str, model):
        self.models[model_name] = model
        print(f"[PredictionAgent] Model registered: {model_name}")

    def unregister_model(self, model_name: str):
        if model_name in self.models:
            del self.models[model_name]
            print(f"[PredictionAgent] Model unregistered: {model_name}")

    async def predict(self, model_name: str, input_data):
        if model_name not in self.models:
            return {"error": f"Model {model_name} not found"}
        model = self.models[model_name]
        try:
            prediction = model.predict(input_data)
            print(f"[PredictionAgent] Prediction using {model_name}: {prediction}")
            return prediction
        except Exception as e:
            await self.recover(e)
            return {"error": "Prediction failed"}

    async def recover(self, error):
        print(f"[PredictionAgent] Recovered from error: {error}")
