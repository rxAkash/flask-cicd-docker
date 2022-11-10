import logging
import logstash
from flask import Flask, session, request
from uuid import uuid4
# from logger import MyLogger
from dependency_injector.wiring import Provide, inject
from src.containers import Container
from src.auth import auth_blueprint
from src.utils.constants import REQUEST_ID
from src.utils.api_response import ErrorResponse
host = 'localhost'

# Setup logging
logger = logging.getLogger('python-logstash-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

container = Container()
container.init_resources()
# logger: MyLogger = Provide[Container.logger]

flask_app = Flask(__name__)
app_ctx = flask_app.app_context()
app_ctx.push()
app = app_ctx.app
app.secret_key = "gfFbK0CFC4K6I0NjUhJmZPMTOsNXZZwI"

'''
Error handlers
'''


@app.errorhandler(400)
def handle_bad_request(e):
    logger.error("BadRequest", stack_info=e, extra={
                  REQUEST_ID: session[REQUEST_ID]})
    return ErrorResponse(code=400, error="Required fields are missing").__dict__()


@app.errorhandler(500)
def handle_server_error(e):
    logger.error("Server", stack_info=e)
    return ErrorResponse().__dict__()


app.register_error_handler(400, handle_bad_request)
app.register_error_handler(500, handle_server_error)


@app.before_request
@inject
def before_request_callback():
    session[REQUEST_ID] = str(uuid4())
    headers = request.headers.__dict__
    headers[REQUEST_ID] = session[REQUEST_ID]
    logger.info("API request", extra={
        "headers": headers, "params": request.args if request.args else request.get_json(), })


# @app.after_request
# def after_response_callback(response: Response):
#     request_id = session[REQUEST_ID]
#     json_data = json.loads(response.get_data())
#     json_data[REQUEST_ID] = request_id
#     logger.info("API response", extra={
#                 "response": json_data, })
#     return response

@app.route("/")
def check():
    return 'Welcome the Python Docker'


if __name__ == "__main__":
    container.wire(modules=[__name__])
    app.register_blueprint(auth_blueprint)
    app.run(host="0.0.0.0", port=80, debug=True)