import requests
import const
import json


def main():
    url = const.RASP_URL
    data = {
        'cmd': 'get_data_by_id',
        'id': 1
    }

    ret = requests.post(url, json.dumps(data))
    print(ret.text)


if __name__ == '__main__':
    main()
