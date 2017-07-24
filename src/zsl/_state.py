_current_app = None


def get_current_app():
    # type: () -> Zsl
    return _current_app


def set_current_app(app):
    # type: (Zsl) -> None
    global _current_app

    _current_app = app
