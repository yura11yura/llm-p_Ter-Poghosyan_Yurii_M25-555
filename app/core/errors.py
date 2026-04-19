class AppError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class UnauthorizedError(AppError):
    """Ошибка аутентификации."""
    pass
    

class ConflictError(AppError):
    """Ошибка конфликта данных."""
    pass


class ForbiddenError(AppError):
    """Ошибка авторизации."""
    pass


class NotFoundError(AppError):
    """Ошибка отсутствия ресурса."""
    pass


class ExternalServiceError(AppError):
    """Ошибка при обращении к внешнему сервису."""
    pass
