from app import application, db
from app.models import Entity, Review

@application.shell_context_processor
def make_shell_context():
	return {'db': db, 'Entity': Entity, 'Review': Review}

if __name__ == "__main__":
	application.run(host="0.0.0.0", port=8080, debug=True)