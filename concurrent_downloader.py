from datetime import datetime
import requests
import asyncio
import aiohttp
import aiofiles


async def do(data: dict, session: aiohttp.ClientSession, tasks: list) -> (list, list):
    print("Making connection")
    response = await get_new_request(method="HEAD", url=data['Url'], session=session)
    print(f"Got {response.status}")

    if response.status > 299:
        raise Exception(f"Can't process, response is {response.status_code}")

    size = response.headers.get('content-length')
    print(f"Size is {size} bytes")

    # initializing list of lists
    sections = [[0, 0] for _ in range(data['TotalSections'])]
    each_size = int(size) // data['TotalSections']
    print(f"Each size is {each_size} bytes")
    print(sections)
    for index, _ in enumerate(sections):
        if index == 0:
            sections[index][0] = 0
        else:
            sections[index][0] = sections[index - 1][1] + 1

        if index < data['TotalSections'] - 1:
            sections[index][1] = sections[index][0] + each_size
        else:
            sections[index][1] = int(size) - 1

    print(sections)
    for index, section in enumerate(sections):
        tasks.append(asyncio.create_task(download_section(index, section, data, session)))
        # await asyncio.sleep(0.001)
    return sections, tasks


async def get_new_request(method: str, url: str,
                          session: aiohttp.ClientSession, headers: dict = None) -> aiohttp.ClientResponse:
    if headers:
        headers['User-Agent'] = "Silly Download Manager v001"
    return await session.request(method=method, url=url, headers=headers)


async def download_section(index: int, section: list,
                           data: dict, session: aiohttp.ClientSession):
    headers = {'Range': f"bytes={section[0]}-{section[1]}"}
    resp = await get_new_request(method="GET", url=data['Url'],session=session, headers=headers)
    print(f"Downloaded {resp.headers.get('content-length')} bytes "
          f"for section {index}: {section}")
    file_name = f"section-{index}.tmp"
    data = await resp.content.read()
    f = await aiofiles.open(file_name, 'wb')
    await f.write(data)
    await f.close()


def merge_files(target_path: str, sections: list) -> None:
    with open(target_path, 'wb+') as final_file:
        for index, section in enumerate(sections):
            file_name = f"section-{index}.tmp"
            with open(file_name, 'rb') as section_file:
                final_file.write(section_file.read())


async def main(data: dict, tasks: list):
    start_time = datetime.now().replace(microsecond=0)
    async with aiohttp.ClientSession() as session:
        sections, tasks_ = await do(data=data, session=session, tasks=tasks)
        await asyncio.wait(tasks_)
    total_seconds = datetime.now().replace(microsecond=0) - start_time
    print(f"Download completed in {total_seconds.total_seconds()} seconds")
    return sections

if __name__ == "__main__":
    d = {'Url': "http://ipv4.download.thinkbroadband.com/5MB.zip",
         'TargetPath': "5MB.zip",
         'TotalSections': 10}
    tasks = []
    sections = asyncio.run(main(data=d, tasks=tasks))
    merge_files(d['TargetPath'], sections=sections)
