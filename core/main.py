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
        # TODO download photos for all


if __name__ == "__main__":
    asyncio.run(main())
