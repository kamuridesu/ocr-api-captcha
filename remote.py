from easyocr_api.src.exposer import main, app


# __all__ == ["app"]
import asyncio
def __main():
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = "0.0.0.0:2222"
    config.workers = 4

    asyncio.run(serve(app, config))

if __name__ == "__main__":
    __main()
