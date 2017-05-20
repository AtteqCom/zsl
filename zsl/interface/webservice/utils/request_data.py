def extract_data(request):
    data = request.form.to_dict(flat=True)
    if request.json:
        data = request.json
    return data
