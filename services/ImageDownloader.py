from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from collections import OrderedDict
import os
from pathlib import Path
from fastapi import Response, status
from starlette import responses


def handleImage(date: str, location: dict, cloudCoverage: float, userName: str, response: Response):
    """
    This function take six arguments:
    date: (type: string) min date intervale
    location: (tye: dictionary) containing two keys longitude and latitude (type: float).
    cloudCoverage:(type: float) pourcentage of cloud coverage of the image looked for.
    userName:(type: string) current user name

    """
    api = SentinelAPI(os.getenv('NAME'), os.getenv("PASSWORD"))
    area = {

        "type": "Point",
        "coordinates": [
            location["lon"],
            location["lat"]]
    }

    area = geojson_to_wkt(area)
    result = api.query(area=area, date=(date, "NOW"), order_by="cloudcoverpercentage", cloudcoverpercentage=(
        0, cloudCoverage), orbitdirection='DESCENDING', limit=1, platformname='Sentinel-1')
    if result:
        id = list(result.keys())[0]
        print(id)
        path = f"./DB/images/{userName}"
        return {**Path(path).mkdir(parents=True, exist_ok=True), "status": "success"}

        return
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"error": "we couldn't found image for given criteria"}
