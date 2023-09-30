def allowed_file(filename: str, ALLOWED_EXTENSIONS: list[str]) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS