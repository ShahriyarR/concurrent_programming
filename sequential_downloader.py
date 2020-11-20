from datetime import datetime
import requests


def main():
    start_time = datetime.now().replace(microsecond=0)
    d = {'Url': "http://ipv4.download.thinkbroadband.com/5MB.zip",
         'TargetPath': "5MB.zip",
         'TotalSections': 10}
    do(d)
    total_seconds = datetime.now().replace(microsecond=0) - start_time
    print(f"Download completed in {total_seconds.total_seconds()} seconds")


def do(data: dict):
    print("Making connection")
    response = get_new_request(method="HEAD", url=data['Url'])
    print(f"Got {response.status_code}")

    if response.status_code > 299:
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
        download_section(index, section, data)


def get_new_request(method: str, url: str, headers: dict = None) -> requests.Response:
    response = requests.request(method=method, url=url, headers=headers)
    response.headers['user-agent'] = "Silly Download Manager v001"
    return response


def download_section(index: int, section: list, data: dict):
    headers = {'Range': f"bytes={section[0]}-{section[1]}"}
    resp = get_new_request(method="GET", url=data['Url'], headers=headers)
    print(f"Downloaded {resp.headers.get('content-length')} bytes "
          f"for section {index}: {section}")
    file_name = f"section-{index}.tmp"
    with open(file_name, mode='wb') as local_file:
        local_file.write(resp.content)


if __name__ == "__main__":
    main()