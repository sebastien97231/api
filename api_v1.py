from flask import Flask, request, jsonify
import mysql.connector



mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2025"
)
cursor = mydb.cursor()

app = Flask(__name__)



# Home route
@app.route('/')
def home():
    return 'Page D\'accueil'



# Create new student (POST)
@app.route('/v1/etudiants/', methods=['POST'])
def createEtudiant():
    data = request.json
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']

    # Insert query
    request_query = "INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
    values = (nom, prenom, email, telephone)
    
    cursor.execute(request_query, values)
    mydb.commit()

    return jsonify({"message": "Étudiant créé avec succès"}), 201

@app.route('/v1/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    # Récupérer les paramètres de la requête
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    email = request.args.get('email')
    telephone = request.args.get('telephone')

    if not nom or not prenom or not email or not telephone:
        return jsonify({"message": "Tous les champs sont requis"}), 400

    # Requête de mise à jour
    request_query = """
    UPDATE etudiant 
    SET nom = %s, prenom = %s, email = %s, telephone = %s 
    WHERE id = %s
    """
    values = (nom, prenom, email, telephone, id)
    
    cursor.execute(request_query, values)
    mydb.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Étudiant non trouvé"}), 404

    return jsonify({"message": "Étudiant mis à jour avec succès"}), 200

@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    etudiants = []
    request = "SELECT * FROM etudiant"
    cursor.execute(request)
    result = cursor.fetchall()
    for raw in result:
        etudiant = {
            "etudiant": raw[0],
            "nom": raw[1],
            "prenom": raw [2],
            "email": raw [3],
            "telephone": raw[4]
        }
        etudiants.append(etudiant)
    return jsonify(etudiants), 201

@app.route('/v1/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    # Delete query
    request_query = "DELETE FROM etudiant WHERE etudiant_id = %s"
    values = (id,)
    
    cursor.execute(request_query, values)
    mydb.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Étudiant non trouvé"}), 404

    return jsonify({"message": "Étudiant supprimé avec succès"}), 200


# Fetch a specific student (GET - retrieval still uses GET)
@app.route('/v1/etudiant/<int:id>', methods=['GET'])
def getEtudiant(id):
    request_query = "SELECT * FROM etudiant WHERE idetudiant = %s"
    cursor.execute(request_query, (id,))
    raw = cursor.fetchone()

    if raw:
        etudiant = {
            "etudiant": raw[0],
            "nom": raw[1],
            "prenom": raw[2],
            "email": raw[3],
            "telephone": raw[4]
        }
        return jsonify(etudiant)
    else:
        return jsonify({"message": "Étudiant non trouvé"}), 404



if __name__ == '__main__':
    app.run(debug=True)