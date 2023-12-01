def session_decorator(session):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                session.commit()

                return result

            except Exception as ex:
                session.rollback()
                raise ex

            finally:
                session.close()

        return wrapper

    return decorator


# The decorator manages the opening and closing of the current session, so i don't have to do it repeatedly.