import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s',
                              '%m/%d %H:%M:%S')

file_handler = logging.FileHandler('build_status.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

name = "TCISI_HotelOverview_singleHeroImage"

def build():
    print("build")
    logger.info(name + " - Created")
    logger.info(name + " - Tagged and Completed")
    # logging.warning("Logout occured")
    logger.info("Successfully logged back in")


if __name__ == '__main__':
    print("hey")
    build()
