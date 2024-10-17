from flask import Flask, jsonify, request
import logging
import os

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application Metadata (with defaults if build args are not provided)
APP_VERSION = os.getenv("APP_VERSION", "1.0")
DESCRIPTION = os.getenv("APP_DESCRIPTION", "PI technical example")
LAST_COMMIT_SHA = os.getenv("APP_COMMIT_SHA", "abc12345679")

# Application configuration
PORT = 5000
HOST = '0.0.0.0'

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        return jsonify({
            "myapplication": [
                {
                    "version": APP_VERSION,
                    "description": DESCRIPTION,
                    "lastcommitsha": LAST_COMMIT_SHA
                }
            ]
        }), 200
    except Exception as e:
        logger.error(f"Error occurred in /healthcheck: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 Not Found: {request.path}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
