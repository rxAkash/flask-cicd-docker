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
from elasticapm.contrib.flask import ElasticAPM

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
flask_app.config['ELASTIC_APM'] = {
    # Set the required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': 'flask-es-cloud-service',

    # Use if APM Server requires a secret token
    'SECRET_TOKEN': 'MIuLhxn7SfvoiGhARQ',

    # Set the custom APM Server URL (default: http://localhost:8200)
    'SERVER_URL': 'https://e19d03a52bf1498e9bfcabf7b4537923.apm.ap-south-1.aws.elastic-cloud.com:443',

    # Set the service environment
    'ENVIRONMENT': 'production',
    'PROCESSORS': (
        'src.utils.custom_apm_processor.my_processor',
        'elasticapm.processors.sanitize_stacktrace_locals',
        'elasticapm.processors.sanitize_http_request_cookies',
        'elasticapm.processors.sanitize_http_headers',
        'elasticapm.processors.sanitize_http_wsgi_env',
        'elasticapm.processors.sanitize_http_request_body',
    ),
    'SANITIZE_FIELD_NAMES': (
        "password",
        "passwd",
        "pwd",
        "secret",
        "*key",
        "*token*",
        "*session*",
        "*credit*",
        "*card*",
        "*auth*",
        "set-cookie",
    ),
}


app_ctx = flask_app.app_context()
app_ctx.push()
app = app_ctx.app

app.secret_key = "gfFbK0CFC4K6I0NjUhJmZPMTOsNXZZwI"
apm = ElasticAPM(app, logging=logging.ERROR)
'''
Error handlers
'''


@app.errorhandler(400)
def handle_bad_request(e):
    logger.error("BadRequest", stack_info=e, extra={
        REQUEST_ID: session[REQUEST_ID]})
    apm.capture_exception(e)
    return ErrorResponse(code=400, error="Required fields are missing").__dict__()


@app.errorhandler(500)
def handle_server_error(e):
    logger.error("Server", stack_info=e)
    apm.capture_exception(e)
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
