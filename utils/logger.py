import logging

def setup_logger():
    logger = logging.getLogger("SQLValidator")
    logger.setLevel(logging.DEBUG)

    # create format of the logs
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #TODO : Create a FileHandler and a StreamHandler -> DONE
    file_pipe = logging.FileHandler('Project.log', mode='w')
    file_pipe.setFormatter(log_format)
    logger.addHandler(file_pipe)

    #TODO : Add the formatter to those handlers -> DONE
    stream_pipe = logging.StreamHandler()
    stream_pipe.setFormatter(log_format)
    logger.addHandler(stream_pipe)

    #TODO : Add the handlers to the logger -> DONE

    return logger

