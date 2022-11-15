from .services import UserService, AuthService
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request
from .containers import Container
from .utils.api_response import SuccessResponse, ErrorResponse
# from logger import MyLogger

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/get-user", methods=['GET'])
@inject
def get_user(user_service: UserService = Provide[Container.user_service], ):
    email = request.args['email']
    user = user_service.get_user(email)
    return SuccessResponse(data=user, msg="User data fetch successfully").__dict__()


@auth_blueprint.route("/login", methods=['POST'])
@inject
def authenticate_user(auth_service: AuthService = Provide[Container.auth_service]):
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = auth_service.authenticate({"email": email}, password)
    return SuccessResponse(data=result, msg="User authenticated successfully").__dict__()


@auth_blueprint.route('/email-login', methods=["POST"])
@inject
def do_login(auth_service: AuthService = Provide[Container.auth_service]):
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = auth_service.login({"email": email}, password)
    return result
