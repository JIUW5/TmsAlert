import os

import uvicorn


def main() -> None:
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', '8080'))
    uvicorn.run('tms_alert_service.app:app', host=host, port=port, reload=False)


if __name__ == '__main__':
    main()
