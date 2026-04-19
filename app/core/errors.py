class AppError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class UnauthorizedError(AppError):
    pass
    

class ConflictError(AppError):
    pass


class ForbiddenError(AppError):
    pass


class NotFoundError(AppError):
    pass


class ExternalServiceError(AppError):
    pass