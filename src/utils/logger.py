import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="detector.log",
    filemode="w"
)

logger = logging.getLogger(__name__)