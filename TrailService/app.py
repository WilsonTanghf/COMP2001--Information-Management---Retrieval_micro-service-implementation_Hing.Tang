from flask import Flask
import connexion
import trail_api

# Create the Connexion app
app = connexion.App(__name__, specification_dir='.')
app.add_api('openapi.yaml', strict_validation=True, validate_responses=True,)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)