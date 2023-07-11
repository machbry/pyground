import time
import asyncio


SLEEP_TIME = 0.2


def sync_gen(n_max: int = 5):
    i = 0
    while i < n_max:
        yield 2 ** i
        i += 1
        time.sleep(SLEEP_TIME)


def sync_main():
    start = time.perf_counter()
    u = [i for i in sync_gen()]
    print(f"u generated")
    v = [j for j in sync_gen() if not (j // 3 % 5)]
    print(f"v generated")
    end = time.perf_counter() - start
    print(f"sync_main executed in {end}s")
    return u, v


async def async_gen(n_max: int = 5):
    i = 0
    while i < n_max:
        yield 2 ** i
        i += 1
        await asyncio.sleep(SLEEP_TIME)


async def async_main():
    # This does *not* introduce concurrent execution
    # It is meant to show syntax only
    start = time.perf_counter()
    x = [i async for i in async_gen()]
    print(f"x generated")
    y = [j async for j in async_gen() if not (j // 3 % 5)]
    print(f"y generated")
    end = time.perf_counter() - start
    print(f"async_main executed in {end}s")
    return x, y


async def power_of_two(i: int):
    await asyncio.sleep(SLEEP_TIME)
    return 2**i


async def generate_powers_of_two(n_max: int = 5):
    start = time.perf_counter()
    a = await asyncio.gather(*[power_of_two(i) for i in range(n_max)])
    b = await asyncio.gather(*[power_of_two(i) for i in range(n_max) if (i % 2 == 0)])
    end = time.perf_counter() - start
    print(f"generate_powers_of_two executed in {end}s")
    return a, b

u, v = sync_main()
print(u)
print(v)

x, y = asyncio.run(async_main())
print(x)
print(y)

a, b = asyncio.run(generate_powers_of_two())
print(a)
print(b)
