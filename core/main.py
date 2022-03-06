import asyncio

from client.client import Client


async def main():
    async with Client() as client:
        users = await client.get_users()
        albums = await asyncio.gather(
            *[client.get_user_albums(user.id) for user in users]
        )
        photos = await asyncio.gather(
            *[client.get_user_photos(user.id) for user in users]
        )
        path = await asyncio.gather(*[client.download_photo(photos[0][0].url)])


if __name__ == "__main__":
    # asyncio.Semaphore(getattr(settings, "IO_REQUEST_LIMIT", 50))
    asyncio.run(main())
