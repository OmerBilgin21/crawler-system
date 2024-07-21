from apps import env
from apps.explorer.app import app as explorer_app

if __name__ == "__main__":
	if env == "dev":
		explorer_app.run(debug=True, port=8000, host="0.0.0.0")
	else:
		explorer_app.run(port=8000, host="0.0.0.0")
