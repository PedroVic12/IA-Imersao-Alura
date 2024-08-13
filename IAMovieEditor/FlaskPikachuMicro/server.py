

# interdace em dash

# uso langchain, gemini e crewai

# input link do youtube

# ver video com processamento em barra

# output texto e arquivo .md


from flask import Flask, request, jsonify
from flask_sqlaclhemy import SQLAlchemy

database = SQLAlchemy()


class RoutesPikachu:
    def __init__(self,app):
        self.app = app


    def routes(self):
        @self.app.route("/")
        def index():
                return "Hello from Pikachu Using ThunderFlask!"

    @self.app.route('/api/play', methods=['POST'])
    def play_routes(self):
        data = request.json
        items = data.get('items', [])
        api_key = data.get('apiKey', '')    
            # Aqui você processaria os dados como necessário
        # Por exemplo, você poderia usar a API key para fazer chamadas para o GPT-4
        
        return jsonify({"message": "Dados recebidos com sucesso", "itemCount": len(items)})

    # Rota GET
    @self.app.route('/api/data', methods=['GET'])
    def get_data():
        return jsonify(data)

    # Rota POST
    @self.app.route('/api/data', methods=['POST'])
    def post_data():
        new_message = request.json.get('message')
        data['message'] = new_message
        return jsonify({"message": "Data updated successfully!"})




class App:
    def __init__(self):
        self.app = Flask(__name__)


    def iniciar(self):
        rotas = RoutesPikachu(self.app)
        rotas.play_routes()


    def run(self):
        database.init_app(app)
        self.app.run(debug = True, host = "0.0.0.0", port = 98)
    


# Dados de exemplo
#!import



#! app
    
    # run

# main




data = {
    "message": "Hello from Flask!"
}


if __name__ == '__main__':
    app = App()
    app.iniciar()

    app.run()
