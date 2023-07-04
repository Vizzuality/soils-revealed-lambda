import logging

from soils.analysis.general_statistics import statistics

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# def analysis(event, context): #only for lambda
def analysis(event):
    logger.info(f'## EVENT\r {event}')
    # logger.info(f'## CONTEXT\r {context}')
    request = event  # .get_json()

    dataset = request['dataset']
    logger.info(f'## DATASET\r {dataset}')

    return statistics(request)
