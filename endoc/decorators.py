def register_service(name):
    def decorator(func):
        from .endoc_client import EndocClient
        setattr(EndocClient, name, func)
        return func
    return decorator