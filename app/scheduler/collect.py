import sys
import asyncio
from app.db.mongodb import get_database
from app.db.mongodb_util import connect_to_mongo, close_mongo_connection

# sys.path.append("..")
# sys.path.append("../..")


async def main():
    await connect_to_mongo()
    db = await get_database()
    print(db)

if __name__ == '__main__':
    asyncio.run(main())
# loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
# loop.run_until_complete(main())  # main 끝날 때까지 이벤트 루프를 실행
# loop.close()                     # 이벤트 루프를 닫음
