import asyncio

from app.seeds import seed_admin_org, seed_roles


async def main():
    await seed_roles()
    await seed_admin_org()


if __name__ == "__main__":
    asyncio.run(main())
