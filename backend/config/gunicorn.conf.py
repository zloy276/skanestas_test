from backend.config.settings import settings

bind = f"{settings.BIND_IP}:{settings.BIND_PORT}"

worker_class = "uvicorn.workers.UvicornWorker"
workers = 1

reload = True
factory = True
wsgi_app = "backend.app.main:create_app"
proc_name = "web"
