import logging
import time

def main():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    logger.info((f"Admin logged in for pipeline test"))
    logger.info("Finish_running_top1_suggestion=10;")

    time.sleep(120)

if __name__ == "__main__":
    main()
