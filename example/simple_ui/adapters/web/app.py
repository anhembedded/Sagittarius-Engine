from flask import Flask, request, jsonify
from src.app_kernel import App
from example.simple_ui.application.commands import CreateUserCommand, CreateUserDto
from example.simple_ui.application.queries import ListUsersQuery

def create_app(framework_app: App) -> Flask:
    app = Flask(__name__)

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        if not data or 'username' not in data:
            return jsonify({'error': 'username is required'}), 400

        data_transfer_obj = CreateUserDto(username=data['username'])
        user = framework_app.execute(CreateUserCommand, data_transfer_obj)
        return jsonify({'id': user.id, 'username': user.username}), 201

    @app.route('/users', methods=['GET'])
    def list_users():
        users = framework_app.execute(ListUsersQuery, None)
        return jsonify([{'id': u.id, 'username': u.username} for u in users]), 200

    return app
