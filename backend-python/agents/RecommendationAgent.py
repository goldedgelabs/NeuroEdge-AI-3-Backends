# RecommendationAgent.py
# Agent responsible for generating recommendations based on user behavior and data

class RecommendationAgent:
    def __init__(self):
        self.name = "RecommendationAgent"
        self.recommendation_models = {}

    def register_model(self, model_name: str, model):
        self.recommendation_models[model_name] = model
        print(f"[RecommendationAgent] Model registered: {model_name}")

    def unregister_model(self, model_name: str):
        if model_name in self.recommendation_models:
            del self.recommendation_models[model_name]
            print(f"[RecommendationAgent] Model unregistered: {model_name}")

    async def recommend(self, model_name: str, user_data):
        if model_name not in self.recommendation_models:
            return {"error": f"Model {model_name} not found"}
        model = self.recommendation_models[model_name]
        try:
            recommendations = model.recommend(user_data)
            print(f"[RecommendationAgent] Recommendations using {model_name}: {recommendations}")
            return recommendations
        except Exception as e:
            await self.recover(e)
            return {"error": "Recommendation failed"}

    async def recover(self, error):
        print(f"[RecommendationAgent] Recovered from error: {error}")
