from easyocr_api.src.executer import main
from sys import argv


if __name__ == "__main__":
    if "--init" in argv:
        exit(0)
    main()
