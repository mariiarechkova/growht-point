import asyncio
import sys

from app.core.database import async_session_maker
from app.seeds.departments_and_users import seed_departments_with_users
from app.seeds.org_and_admin import seed_admin_org
from app.seeds.roles import seed_roles


# Common point to run all seeds
async def run_seed(seed_name: str):
    async with async_session_maker() as session:
        try:
            async with session.begin():
                match seed_name:
                    case "all":
                        await seed_roles(session)
                        await seed_admin_org(session)
                        await seed_departments_with_users(session)
                        print("All seeds applied successfully.")
                    case "roles":
                        await seed_roles(session)
                    case "admin_org":
                        await seed_admin_org(session)
                    case "departments_users":
                        await seed_departments_with_users(session)

                    case _:
                        print(f"Unknown seed name: '{seed_name}'")
        except Exception as e:
            print(f"Error running seed '{seed_name}': {e}")


# Point to run seeds from terminal
if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    asyncio.run(run_seed(name))
