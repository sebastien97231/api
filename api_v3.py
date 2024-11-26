from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)

db = Database("127.0.0.1","root","","ciel2025")

@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if not db.authorrized(request):
        return jsonify({"Message": "Accès non autorisé"}), 401
    
    result = db.readone(id)
    
    if result:
        etudiant = {
            "idetudiant": result[0],
            "nom": result[1],
            "prenom": result[2],
            "email": result[3],
            "telephone": result[4]
        }
        return jsonify(etudiant), 200
    else:
        return jsonify({"Message": "Étudiant non trouvé"}), 404

@app.route('/v3/etudiants/', methods=['GET'])
def getEtudiants():
    if not db.authorrized(request):
        return jsonify("Message : Accès non autorisé"),401
    
    etudiants = []
    result = db.readall()
    for row in result:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        etudiants.append(etudiant)
    return jsonify(etudiants),200

@app.route('/v3/etudiants/', methods=['POST'])
def createEtudiant():
    if not db.authorrized(request):
        return jsonify({"Message": "Accès non autorisé"}), 401
    data = request.get_json()
    if not data or not all(key in data for key in ("nom", "prenom", "email", "telephone")):
        return jsonify({"Message": "Données invalides"}), 400
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']
    etudiant_id = db.create(nom, prenom, email, telephone)
    if etudiant_id:
        return jsonify({"Message": "Étudiant créé avec succès", "idetudiant": etudiant_id}), 201
    else:
        return jsonify({"Message": "Erreur lors de la création de l'étudiant"}), 500

@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):

    if not db.authorrized(request):
        return jsonify({"Message": "Accès non autorisé"}), 401
    success = db.delete(id)

    if success:
        return jsonify({"Message": "Étudiant supprimé avec succès"}), 200
    
    else:
        return jsonify({"Message": "Erreur lors de la suppression de l'étudiant ou étudiant non trouvé"}), 404

@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not db.authorrized(request):
        return jsonify({"Message": "Accès non autorisé"}), 401

    data = request.get_json()

    if not data or not any(key in data for key in ("nom", "prenom", "email", "telephone")):
        return jsonify({"Message": "Aucune donnée valide fournie"}), 400

    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')

    success = db.update(id, nom, prenom, email, telephone)

    if success:
        return jsonify({"Message": "Étudiant mis à jour avec succès"}), 200
    else:
        return jsonify({"Message": "Erreur lors de la mise à jour de l'étudiant ou étudiant non trouvé"}), 404
   
@app.route("/login")
def login():
    data = db.log(request)
    if data != 401:
        user = {
            "username": data[1],
            "password": data [2]
        }
        return jsonify(user), 200
    else:
        return jsonify("Bad credentials"), 404
               
if __name__ == '__main__':
    context = ('cert.pem','key.pem')
    app.run(host = '0.0.0.0', ssl_context=context, debug=True)      

