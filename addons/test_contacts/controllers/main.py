# Copyright 2020 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main

class RestApiPublicController(main.RestController):
    _root_path = "/restapi/public/"
    _collection_name = "ccu.connector.rest.public.services"
    _default_auth = "public"
    _cors = "*"


class RestApiPrivateController(main.RestController):
    _root_path = "/restapi/private/"
    _collection_name = "ccu.connector.rest.private.services"
    _default_auth = "api_key"
    _cors = "*"