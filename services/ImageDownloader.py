from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from collections import OrderedDict
import os
from pathlib import Path
from fastapi import Response, status
from starlette import responses
PASSWORD = "9Auy@qznE!LbxQL"
NAME = "creastation"


def handleImage(date: str, location: dict, cloudCoverage: float, userId: int):
    """
    This function take six arguments:
    date: (type: string) min date intervale
    location: (tye: dictionary) containing two keys longitude and latitude (type: float).
    cloudCoverage:(type: float) pourcentage of cloud coverage of the image looked for.
    userName:(type: string) current user name

    """
    api = SentinelAPI(NAME, PASSWORD)
    area = {

        "type": "Point",
        "coordinates": [
            location["lon"],
            location["lat"]]
    }

    area = geojson_to_wkt(area)
    result = api.query(area=area, date=(date, "NOW"), order_by="cloudcoverpercentage", cloudcoverpercentage=(
        0, cloudCoverage), orbitdirection='DESCENDING', limit=1, platformname='Sentinel-3')
    if result:
        id = list(result.keys())[0]
        path = f"./DB/images/{userId}"
        imageName = result[id]["title"]+".jpeg"
        Path(path).mkdir(parents=True, exist_ok=True)
        api.download_quicklook(id, path)
        return {"path": path.replace("./",""), "imageName": imageName}

    else:
        raise Exception("we couldn't find image for the given criteria")


print(handleImage("20151202", {"lon": -5, "lat": 39}, 15, 20))
