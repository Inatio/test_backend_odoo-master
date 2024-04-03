from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from math import sqrt
import logging
import re

_logger = logging.getLogger(__name__)

class Account(Component):
    _inherit = "base.rest.service"
    _name = "contact.service"
    _usage = "contact"
    _collection = "ccu.connector.rest.public.services"
    _cors = "*"
    _description =  """
                    Contact Queries
                    ===============
                    Endpoints available:
                    * ``GET /restapi/public/contact/close_contact``: Este endpoint de la API. Toma coordenadas y una distancia máxima,
                        y opcionalmente un género, y devuelve todos los contactos dentro de la distancia especificada de las
                        coordenadas, y del género especificado si se proporciona.

                        Parámetros:
                        x_coordinate (float): La coordenada x de la ubicación, Ejemplo: 25.00.

                        y_coordinate (float): La coordenada y de la ubicación, Ejemplo: 15.00.

                        max_distance (float): La distancia máxima desde la ubicación, Ejemplo: 13.54.

                        gender (str, opcional): El género de los contactos a devolver. Puede ser una lista de géneros separada por comas, Ejemplo: male.

                        Devoluciones:
                        dict: Un diccionario con tres claves:
                            - success (bool): Si la operación fue exitosa.

                            - error (str): El mensaje de error, si lo hay.

                            - data (list): Una lista de diccionarios, cada uno representando un contacto. Cada diccionario tiene dos claves:
                                - name (str): El nombre del contacto.

                                - distance (float): La distancia del contacto desde las coordenadas dadas.

                        Excepciones:
                        Exception: Si hay un error en la operación.

                        Ejemplo:
                            curl -X 'GET' \
                                'http://localhost:8069/restapi/public/contact/contact/close_contact/15.00/50.00/40.00/male' \
                                -H 'accept: */*'

                            Request URL
                                http://localhost:8069/restapi/public/contact/contact/close_contact15.00/50.00/40.00/male
                    """

    # Define el método get_close_contact que se expone como un endpoint de la API
    @restapi.method(
        [("/contact/close_contact<float:x_coordinate>/<float:y_coordinate>/<float:max_distance>", "GET")],
        auth="user",
        cors="*",
        parameters=[
            {
                'in': 'path',
                'name': 'x_coordinate',
                'description': 'La coordenada X del punto de referencia. Debe ser un número de tipo float.',
                'required': True,
                'type': 'float',
                'example': 25.00
            },
            {
                'in': 'path',
                'name': 'y_coordinate',
                'description': 'La coordenada Y del punto de referencia. Debe ser un número de tipo float.',
                'required': True,
                'type': 'float',
                'example': 15.00
            },
            {
                'in': 'path',
                'name': 'max_distance',
                'description': 'La distancia máxima desde el punto de referencia. Debe ser un número de tipo float.',
                'required': True,
                'type': 'float',
                'example': 13.54
            },
            {
                'in': 'query',
                'name': 'gender',
                'description': 'El género de los contactos a buscar. Es opcional y puede ser introducido mediante la URL. Si se proporciona, debe ser un string.',
                'required': False,
                'type': 'string',
                'example': 'male'
            }
        ],
        responses={
            200: {
                'description': "Devuelve una lista de contactos cercanos a las coordenadas dadas, filtrados por género si se proporciona. La distancia entre el punto y cada contacto se calcula usando la fórmula de la distancia euclidiana.",
                'schema': {'type': 'array', 'items': {'$ref': '#/definitions/Contact'}},
                'examples': {
                    'application/json': {
                        "success": True,
                        "error": None,
                        "data": [
                            {
                                "name": "Contacto 1",
                                "distance": 1.5
                            },
                            {
                                "name": "Contacto 2",
                                "distance": 2.0
                            }
                        ]
                    }
                }
            },
            400: {
                'description': "Ocurre un error al procesar la solicitud. El mensaje de error se devuelve en el campo 'error'.",
                'examples': {
                    'application/json': {
                        "success": False,
                        "error": "Mensaje de error",
                        "data": []
                    }
                }
            }
        }
    )
    def get_close_contact(self, x_coordinate, y_coordinate, max_distance, gender=None, **kwargs):
        try:
            # Busca todos los contactos en la base de datos
            contacts = self.env['res.partner'].search([])
            close_contacts = []

            # Si gender no es None, se divide en una lista de géneros
            genders = gender.split(',') if gender else None

            # Itera sobre cada contacto
            for contact in contacts:
                # Calcula la distancia entre el contacto y las coordenadas dadas
                distance = sqrt((contact.x_coordinate - x_coordinate)**2 + (contact.y_coordinate - y_coordinate)**2)
                
                # Si la distancia es menor o igual a max_distance y el género del contacto está en la lista de géneros permitidos, añade el contacto a la lista de contactos cercanos
                if distance <= max_distance and (genders is None or contact.gender in genders):
                    close_contacts.append({
                        "name": contact.name,
                        "distance": distance
                    })

            # Devuelve un objeto JSON con los contactos cercanos
            return {
                "success": True,
                "error": None,
                "data": close_contacts
            }
        except Exception as e:
            # Si ocurre un error, devuelve un objeto JSON con el mensaje de error
            return {
                "success": False,
                "error": str(e),
                "data": []
            }