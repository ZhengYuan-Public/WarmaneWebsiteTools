import logging


class ProjectLogging:
    def __init__(self, log_file_path='project.log', log_level=logging.INFO):
        logging.basicConfig(
            filename=log_file_path,
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=log_level
        )
