import easyocr_api
import easyocr_api.src
import easyocr_api.src.executer
import easyocr_api.src.exposer

from sys import argv


def main():
    if argv[1] == "client":
        return easyocr_api.src.executer.main()
    return easyocr_api.src.exposer.main()


if __name__ == "__main__":
    main()
