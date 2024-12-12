import asyncio


async def a():
    print("a start")
    await asyncio.sleep(1)  # 暂停当前协程，直到完成await后的任务，获取结果
    print("a end")


async def b():
    print("b start")
    await asyncio.sleep(1)
    print("b end")


async def main():
    result = asyncio.as_completed([a(), b()])  # 返回一个迭代器，按照完成的顺序返回结果
    for result in result:
        await result


if __name__ == "__main__":
    asyncio.run(main())
