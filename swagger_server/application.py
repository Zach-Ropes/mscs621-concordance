import connexion

from swagger_server import encoder

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'MSCS621 Concordance Assignment 4 API'}, pythonic_params=True)
    application = app.app
    


if __name__ == '__main__':
    main()