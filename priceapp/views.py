import pandas as pd
import numpy as np
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

        # df = df.where(pd.notna(df), None)
        # Replace everything invalid with None
        df.replace(
            to_replace=[np.nan, "NA", "N/A", "na", "null", "--", ""],
            value=None,
            inplace=True
        )

        # Keep only needed columns
        # df = df[["Final Location", "Year", "Price"]]

        # Convert rows to objects
        objects = []

        for _, row in df.iterrows():
            obj = PriceData(
                final_location=row["final location"],
                year=int(row["year"]),
                city=row["city"],

                flat_weighted_avg=row["flat - weighted average rate"],
                office_weighted_avg=row["office - weighted average rate"],
                others_weighted_avg=row["others - weighted average rate"],
                shop_weighted_avg=row["shop - weighted average rate"],

                flat_50=row["flat - 50th percentile rate"],
                office_50=row["office - 50th percentile rate"],
                others_50=row["others - 50th percentile rate"],
                shop_50=row["shop - 50th percentile rate"],

                flat_75=row["flat - 75th percentile rate"],
                office_75=row["office - 75th percentile rate"],
                others_75=row["others - 75th percentile rate"],
                shop_75=row["shop - 75th percentile rate"],

                flat_90=row["flat - 90th percentile rate"],
                office_90=row["office - 90th percentile rate"],
                others_90=row["others - 90th percentile rate"],
                shop_90=row["shop - 90th percentile rate"],
            )
            objects.append(obj)
        

        # Bulk insert with update on conflict
        PriceData.objects.bulk_create(objects, update_conflicts=True,
            unique_fields=["final_location", "year", "city"],
            update_fields=[
                "flat_weighted_avg",
                "office_weighted_avg",
                "others_weighted_avg",
                "shop_weighted_avg",
                "flat_50",
                "office_50",
                "others_50",
                "shop_50",
                "flat_75",
                "office_75",
                "others_75",
                "shop_75",
                "flat_90",
                "office_90",
                "others_90",
                "shop_90",]
                ,batch_size=1000
            )

        return Response({
            "message": "Data uploaded successfully",
            "rows_uploaded": len(objects),
            
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
@api_view(["GET"])
def price_trend(request):

    location = request.GET.get("final_location")
    price_metric = request.GET.get("price_metric", "weighted")
    property_type = request.GET.get("property_type", "flat")  # default flat
    year = request.GET.get("year")  # 👈 NEW (optional)
    
    if not location:
        return Response({"error": "final_location is required"}, status=400)
    
     # 🔐 Allowed property types (SECURITY)
    PRICE_FIELD_MAP = {
            "weighted": {
                "flat": "flat_weighted_avg",
                "office": "office_weighted_avg",
                "shop": "shop_weighted_avg",
                "others": "others_weighted_avg",
            },
            "p50": {
                "flat": "flat_50",
                "office": "office_50",
                "shop": "shop_50",
                "others": "others_50",
            },
            "p75": {
                "flat": "flat_75",
                "office": "office_75",
                "shop": "shop_75",
                "others": "others_75",
            },
            "p90": {
                "flat": "flat_90",
                "office": "office_90",
                "shop": "shop_90",
                "others": "others_90",
            }
        }

    
    # ✅ Validate price_metric
    if price_metric not in PRICE_FIELD_MAP:
        return Response({"error": "Invalid price_metric"}, status=400)
    
    # ✅ Validate property_type
    if property_type not in PRICE_FIELD_MAP[price_metric]:
        return Response({"error": "Invalid property_type"}, status=400)
    
    price_field = PRICE_FIELD_MAP[price_metric][property_type]

    qs = PriceData.objects.filter(
        final_location__iexact=location
    )

    
    # 👇 OPTIONAL year filter
    if year:
        qs = qs.filter(year=year)

    qs = qs.order_by("year")

    if not qs.exists():
        return Response({"error": "No data found"}, status=404)

    result = []
    prev_price = None

    for obj in qs:
        price = getattr(obj, price_field)  # 🔥 dynamic field access

        yoy = None
        if price is not None and prev_price not in (None, 0):
            yoy = round(((price - prev_price) / prev_price) * 100, 2)

        result.append({
            "year": obj.year,
            "price": price,
            "yoy": yoy,
            "property_type": property_type,
            "price_metric": price_metric,
        })

        prev_price = price

    return Response(result, status=200)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PriceData


@api_view(["GET"])
def getall_locations(request):
    locations = (
        PriceData.objects
        .values_list("final_location", flat=True)
        .distinct()
        .order_by("final_location")
    )

    return Response(locations, status=200)


    