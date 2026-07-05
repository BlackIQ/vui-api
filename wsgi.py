from api.main import app

from api.config.db import PORT

if __name__ == "__main__":
    app.run("0.0.0.0", port=PORT, debug=True)
