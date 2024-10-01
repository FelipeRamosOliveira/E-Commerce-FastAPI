import logging

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            # Uncomment to log to a file
            # logging.FileHandler("app.log"),
        ]
    )

# Initialize logging when the module is imported
setup_logging()
