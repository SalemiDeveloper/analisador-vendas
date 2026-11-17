from logger import setup_logger

logger = setup_logger()

logger.info("Pipeline iniciado.")
logger.warning("Registro de venda rejeitado.")
logger.error("Erro durante o processamento.")