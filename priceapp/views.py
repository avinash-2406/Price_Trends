import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TestData,PriceData

@api_view(["POST"])
def testentry(request):
    firstname = request.data.get("firstname")
    lastname = request.data.get("lastname")
    email = request.data.get("email")

    obj = TestData.objects.create(
        firstname=firstname,
        lastname=lastname,
        email=email
    )

    return Response(
        {
            "message": "Created successfully",
            "id": obj.id,
            "firstname": obj.firstname,
            "lastname": obj.lastname,
            "email": obj.email
        }
    )

# 1) UPLOAD EXCEL — bulk_create

@api_view(["POST"])
def upload_excel(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "Excel file is required"}, status=400)

    try:
        # Read Excel file
        df = pd.read_excel(file)

        # Keep only needed columns
        df = df[["Location", "Year", "Price"]]

        # Convert rows to objects
        objects = [
            PriceData(
                location=row["Location"],
                year=int(row["Year"]),
                price=float(row["Price"])
            )
            for _, row in df.iterrows()
        ]

        # Bulk insert
        PriceData.objects.bulk_create(objects, ignore_conflicts=True)

        return Response({
            "message": "Data uploaded successfully",
            "rows_uploaded": len(objects)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

