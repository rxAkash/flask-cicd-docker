from flask import current_app as app
# from dependency_injector.wiring import Provide
# from ..containers import Container
import typing as t

# logger:MyLogger=Provide[Container.logger]


# @app.errorhandler(exceptions.BadRequest)
# def handle_bad_request(e):
#     # logger.exception(e)
#     return ErrorResponse(code=400, error="Required fields are missing").__dict__()


# @app.errorhandler(500)
# def handle_internal_server_error(e):
#     return ErrorResponse(code=500, error="Something went wront. Try later.").__dict__()
