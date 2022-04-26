import asyncio

Seconds = [
  ("first", 5),
  ("second", 0),
  ("third", 3)
]

async def sleeping(order, seconds, hook=None):
  await asyncio.sleep(seconds)
  if hook:
    hook(order)
  return order


async def basic_async():
  for s in Seconds:
    r = await sleeping(*s)
    print("{0} is finished".format(r))
  return True

async def basic_async2(num):
  for s in Seconds:
    r = await sleeping(*s)
    print("{0}s {1} is finished".format(num, r))
  return True


async def parallel_by_wait():
  def notify(order):
    print(order + " has just finished.")
  
  cors = [sleeping(s[0], s[1], hook=notify) for s in Seconds]
  done, pending = await asyncio.wait(cors)
  return done, pending

# 1 順
# if __name__ == "__main__":
#   loop = asyncio.get_event_loop()
#   loop.run_until_complete(basic_async())

# 2 
# if __name__ == "__main__":
#   loop = asyncio.get_event_loop()
#   asyncio.ensure_future(basic_async2(1))
#   asyncio.ensure_future(basic_async2(2))
#   loop.run_forever()


# 3
if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  done, pending = loop.run_until_complete(parallel_by_wait())

  for d in done:
    dr = d.result()
    print("asyncio.wait result: {0}".format(dr))