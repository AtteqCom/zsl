def extract_data(request):
    data = request.data
    # silent, as compatibility with flask 1.1 behavior
    json_data = request.get_json(silent=True)
    return json_data if json_data else data
