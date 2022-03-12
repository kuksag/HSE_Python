import asyncio
import aiofiles
import aiohttp

import os
import logging

ARTIFACTS_FOLDER = 'artifacts'
API_TIMEOUT = 2

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    filename=os.path.join(ARTIFACTS_FOLDER, 'easy_log.txt'),
)
logger = logging.getLogger("easy")

hashes = set()


async def read_bytes_from_stream(content: aiohttp.StreamReader) -> bytes:
    read_bytes = b''
    while True:
        chunk = await content.readany()
        if not chunk:
            break
        read_bytes += chunk
    return read_bytes


async def handle_task(session: aiohttp.ClientSession, file_name: str, url: str, folder_name: str, **kwargs) -> None:
    format_args_prefix = [
        kwargs.get('job_name'),
        kwargs.get('index'),
    ]

    while True:
        await asyncio.sleep(API_TIMEOUT)
        logger.info('J:{},T:{} :: sending request to {}'.format(*format_args_prefix,
                                                                url))

        response = await session.get(url, raise_for_status=True)

        logger.info('J:{},T:{} :: got response {} from {}'.format(*format_args_prefix,
                                                                  response.status,
                                                                  url, ))

        logger.info('J:{},T:{} :: started downloading object'.format(*format_args_prefix))

        read_bytes = await read_bytes_from_stream(response.content)
        if hash(read_bytes) not in hashes:
            hashes.add(hash(read_bytes))
            break

    logger.info('J:{},T:{} :: found unique object, start wrinting to {}'.format(*format_args_prefix,
                                                                                file_name, ))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = os.path.join(folder_name, '{}-{}.png'.format(kwargs.get('job_name'), kwargs.get('index')))
    async with aiofiles.open(file_name, 'b+w') as file:
        await file.write(read_bytes)

    logger.info('J:{},T:{} :: finished writing object in {}'.format(*format_args_prefix,
                                                                    file_name, ))


async def do_job(url, count, job_name, folder=ARTIFACTS_FOLDER):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, _ in enumerate(range(count)):
            tasks.append(
                handle_task(session=session,
                            folder_name=folder,
                            file_name='i',
                            url=url,
                            job_name=job_name,
                            index=i, )
            )
        await asyncio.gather(*tasks)


async def main():
    tasks = [
        do_job(url='https://thiscatdoesnotexist.com/',
               count=3,
               job_name='cat',
               folder=os.path.join(ARTIFACTS_FOLDER, 'cats')),
        do_job(url='https://thispersondoesnotexist.com/',
               count=2,
               job_name='human',
               folder=os.path.join(ARTIFACTS_FOLDER, 'humans')),
        do_job(url='https://thishorsedoesnotexist.com/',
               count=7,
               job_name='horse',
               folder=os.path.join(ARTIFACTS_FOLDER, 'horses')),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
