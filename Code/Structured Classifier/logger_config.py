import logging

def setup_logger():
    # Sets up logging for the app
    # This will log messages to both the console and a file named 'app.log'
    logging.basicConfig(
        level=logging.INFO,  # Set default logging level (DEBUG, INFO, WARNING, etc.)
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),               # Log to console
            logging.FileHandler("app.log", mode="a") # Append logs to a file
        ]
    )
