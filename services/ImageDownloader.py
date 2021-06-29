from sentinelsat import SentinelAPI, geojson_to_wkt
from pathlib import Path
import os

PASSWORD = os.getenv("PASSWORD")
NAME = os.getenv("NAME")
api = SentinelAPI(NAME, PASSWORD)

print(NAME, PASSWORD)


def download_image(userId: int, imageId: int, imageTitle: str):
    """
    This function take six arguments:
    userId:(type: integer) current user id
    imageId:(type: integer) id of the image would you download
    imageTitle:(type: string) title of the image would you download
    """
    path = f"./DB/images/{userId}"
    imageName = f"{imageTitle}.zip"
    Path(path).mkdir(parents=True, exist_ok=True)
    data = api.get_stream(imageId)
    with open(Path(f"./DB/images/{str(userId)}/{imageName}"), "wb") as f:
        f.write(data.content)
    return {"path": path.replace("./", ""), "name": imageName}


def handle_image_information(
    date: str,
    location: dict,
    cloudCoverage: float,
    userId: int,
        platformname: str = "Sentinel-1"):
    """
    This function take 4 arguments:

    date: (type: string) min date intervale YYYYMMDD
    location: (type: dictionary) containing two keys
                lon and lat (type: float).

    cloudCoverage: (type: float) pourcentage of cloud
                      coverage of the image looked for.

    platformname: (type: string) choose the platform which
                    you want to downlow sat images from.
                    for example:
                         Sentinel-1
                         Sentinel-2
                         Sentinel-3
                         Sentinel-4
                    default Sentinel-1
    """
    area = {
        "type": "Point",
        "coordinates": [
            location["lon"],
            location["lat"]]
    }

    area = geojson_to_wkt(area)

    try:
        print("[ImageDownloader] Querying Sentinel API")
        result = api.query(
                    area=area,
                    date=(date, "NOW"),
                    order_by="cloudcoverpercentage",
                    cloudcoverpercentage=(0, cloudCoverage),
                    orbitdirection='DESCENDING',
                    limit=1,
                    platformname=platformname)
        print(result)
        print("[ImageDownloader] Queried Sentinel API without errors")
    except Exception as e:
        print(e)

    if result:
        print("[ImageDownloader] result is not empty, starting saving to db")
        id = list(result.keys())[0]
        iterator = dict(result[id])
        res = {
                key: iterator[key] for key in iterator.keys()
                and {
                        "summary",
                        "title",
                        "platformname",
                        "size",
                        "cloudcoverpercentage"
                    }
                }

        return {
            **res,
            "id": id,
            "path": f"./DB/images/{userId}/{res['title']}.zip"}
    else:
        raise Exception("we couldn't find image for the given criteria")
