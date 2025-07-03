import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

class RecipeService:
    def __init__(self):
        pass

    def generate_recipe(self, skin_type, zone, goal, ingredients):
        prompt = f"""
        Crée une recette cosmétique maison adaptée à une peau {skin_type}, 
        pour la zone {zone}, avec un objectif {goal}.
        Utilise uniquement ces ingrédients : {', '.join(ingredients)}.
        Donne-moi un titre et 3 étapes claires.
        Réponds en JSON comme ça :
        {{
            "title": "Titre de la recette",
            "steps": ["étape 1", "étape 2", "étape 3"]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            ai_reply = response["choices"][0]["message"]["content"]
            data = json.loads(ai_reply)

            data["zone"] = zone
            data["skin_type"] = skin_type
            data["goal"] = goal
            data["ingredients"] = ingredients

            return data

        except Exception as e:
            return {"error": str(e)}
