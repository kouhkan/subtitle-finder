import httpx
from fastapi import HTTPException
from starlette import status


async def get_all_movies(data: dict) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        payload = {
            "query": data["query"]
        }
        response = await client.post(
            url="https://api.subsource.net/api/searchMovieFull",
            json=payload,
            timeout=5 * 10
        )

        return response.json()


async def get_one_movie(data: dict) -> httpx.Response:
    movie_name = data.get("movieName").split("/")[2]
    langs = data.get("langs")

    if not langs:
        langs = []

    async with httpx.AsyncClient() as client:
        payload = {
            "langs": langs,
            "movieName": movie_name
        }
        response = await client.post(
            url="https://api.subsource.net/api/getMovie",
            json=payload,
            timeout=5 * 10
        )

        return response.json()


async def get_download_movie_page(data: dict) -> dict:
    # print(data)
    async with httpx.AsyncClient() as client:
        payload = {
            "movie": data.get("movie"),
            "lang": data.get("lang"),
            "id": str(data.get("id")),
        }
        # print(payload)
        response = await client.post(
            url="https://api.subsource.net/api/getSub",
            json=payload,
            timeout=5 * 10
        )

        # print(response.status_code)
        # print(response.content)
        #
        download_token = response.json()["sub"]["downloadToken"]

        # download_links = []
        # response = await client.get(
        #     url=f"https://api.subsource.net/api/downloadSub/{download_token}",
        #     timeout=5 * 10
        # )
        #
        # with open(f"./{data['movie']}.zip", "wb") as file:
        #     file.write(response.content)

    return {"link": f"https://api.subsource.net/api/downloadSub/{download_token}"}
    # return {"sg": "sd"}


#
async def search_for_subtitle(query: str):
    command: list = query.split(",")
    search_type = None
    query_year = command[0].split(" ")[-1] if command[0].split(" ")[-1].isdigit() else None

    if len(command) > 1:
        try:
            season = command[1]
        except IndexError:
            season = None
        try:
            episode = command[2]
        except IndexError:
            episode = None

        search_type = "TVSeries"

    else:
        search_type = "Movie"

    search_for_all_results = await get_all_movies({"query": command[0]})

    # print(query)
    # print(search_type)
    # print(search_for_all_results)

    db = []
    for item in search_for_all_results["found"]:
        if item["type"] == search_type:
            if query_year and int(query_year) == item["releaseYear"]:
                if search_type == "TVSeries" and season is not None:
                    for year in item["seasons"]:
                        if year["number"] == int(season):
                            db.append(item)
                            break
                elif search_type == "Movie":
                    db.append(item)
                    break

    if len(db) <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{query} not found")

    # print(db)
    # print(db[0]["id"])

    if search_type == "Movie":
        search_for_subtitle_result = await get_one_movie({
            "id": db[0]["id"],
            "movieName": db[0]["fullLink"],
            "lang": "Farsi-Persian"
        })
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not implemented")

    if not search_for_subtitle_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{query} not found")

    db.clear()
    for sub in search_for_subtitle_result["subs"]:
        if sub["lang"] == "Farsi/Persian":
            db.append(sub)

    if len(db) <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{query} not found")

    return db
