class ReviewException(Exception):
    # exceção base
    pass

class ReviewNotFoundError(ReviewException):
    # exceção de "não encontrado"
    pass

class UserAlreadyReviewedError(ReviewException):
    # exceção se tentar avaliar mais de uma vez
    pass

class UnauthorizedReviewActionError(ReviewException):
    # exceção se usuário tentar editar/apagar uma review que não lhe pertence
    pass
