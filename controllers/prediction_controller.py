import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from controllers.delivery_controller import DeliveryController
from openai import OpenAI
from datetime import date

DC = DeliveryController()


class PredictionController(object):
    def __init__(self):
        self._details = DC.show_all_delivery_details()
        self._key = json.load(open('config/openai_key.json'))
        self._client = OpenAI(
            api_key=self._key["key"],
        )
        self._model = self._key["model"]

    def define_station(self):
        today = date.today()
        if 9 <= today.month <= 12:
            return "Primavera"
        elif 1 <= today.month <= 3:
            return "Verano"
        elif 4 <= today.month <= 6:
            return "Otoño"
        elif 7 <= today.month <= 8:
            return "Invierno"

    def recomendations(self):
        try:
            mensages = [
                {'role': 'system', 'content': 'La respuesta es unicamente un listado enumerado de recomendaciones de '
                                              'maximo 3 lineas'},
                {'role': 'user', 'content': f'Realiza predicciones basadas en los siguientes datos: '
                                            f'\nDetalles de productos:\n{self._details}\n'
                                            f'Estacion actual: {self.define_station()}',},
                {'role': 'system', 'content': 'La respuesta debe ser relacionada con cultivos'}
            ]

            response = self._client.chat.completions.create(
                messages=mensages,
                model=self._model,
                temperature=0.5,
            )

            return JSONResponse(status_code=200, content=response.choices[0].message.content)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Error: Can't predict")
