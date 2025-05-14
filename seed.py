import asyncio
import sys

from app.core.database import async_session_maker
from app.seeds.departments_and_users import seed_departments_with_users
from app.seeds.org_and_admin import seed_admin_org

# Импортируем функции сидов
from app.seeds.roles import seed_roles


# Общая точка запуска сидов
async def run_seed(seed_name: str):
    async with async_session_maker() as session:
        try:
            async with session.begin():
                if seed_name == "all":
                    await seed_roles(session)
                    await seed_admin_org(session)
                    await seed_departments_with_users(session)
                    print("All seeds applied successfully.")
                elif seed_name == "roles":
                    await seed_roles(session)
                elif seed_name == "admin_org":
                    await seed_admin_org(session)
                elif seed_name == "departments_users":
                    await seed_departments_with_users(session)
                else:
                    print(f"Unknown seed name: '{seed_name}'")
        except Exception as e:
            print(f"Error running seed '{seed_name}': {e}")


# Точка входа при запуске из терминала
if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    asyncio.run(run_seed(name))
