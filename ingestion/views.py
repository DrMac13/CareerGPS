from django.shortcuts import render
from .forms import CSVUploadForm
from .services.csv_importer import (
    import_opportunities_from_csv
)

import tempfile


def upload_csv(request):

    result = None

    if request.method == "POST":

        form = CSVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_file = request.FILES[
                "csv_file"
            ]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".csv"
            ) as temp_file:

                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

                temp_path = temp_file.name

            result = import_opportunities_from_csv(
                temp_path
            )

    else:

        form = CSVUploadForm()

    return render(
        request,
        "ingestion/upload.html",
        {
            "form": form,
            "result": result
        }
    )