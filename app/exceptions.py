from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail="Пользователь уже существует")

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail="Неверная почта или пароль")

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истек')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Токен не найден')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

ProductAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                              detail="Товар уже существует")

NoProductIdException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail='Не найден ID товара')

NoActiveProductException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                           detail='Не найдены активные товары')
