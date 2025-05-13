import json
from surrealdb import AsyncSurreal


async def surreal_import(table_name, input_file):
    try:
        async with AsyncSurreal("ws://127.0.0.1:5070") as db:
            await db.signin({"username": "root", "password": "root"})
            await db.use("main", "test")

            with open(input_file, "r") as f:
                records = json.load(f)

            inserted = []
            for record in records:
                if "id" in record:
                    res = await db.create(
                        record["id"], {k: v for k, v in record.items() if k != "id"}
                    )
                    inserted.append(res)
                else:
                    res = await db.create(table_name, record)
                    inserted.append(res)

            print(f"Imported {len(inserted)} records")
            return True

    except Exception as e:
        print(f"Import failed: {str(e)}")
        return False


if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Import data into SurrealDB")
    parser.add_argument("table_name", help="The name of the table to import into")
    parser.add_argument("input_file", help="The path to the input JSON file")
    args = parser.parse_args()
    asyncio.run(surreal_import(args.table_name, args.input_file))
