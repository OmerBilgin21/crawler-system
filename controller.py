from apps import env
from apps.controller.app import app as controller_app

if __name__ == "__main__":
	if env == "dev":
		controller_app.run(debug=True, port=8080, host="0.0.0.0")
	else:
		controller_app.run(port=8080, host="0.0.0.0")
