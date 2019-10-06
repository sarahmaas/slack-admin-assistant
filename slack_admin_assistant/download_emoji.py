import os
import slack
import pprint
import wget
from urllib.error import HTTPError
from urllib.parse import unquote


def download_emoji(client: slack.WebClient, directory: str = '.') -> None:
    emoji_response = client.emoji_list()
    print(emoji_response)

    if emoji_response.get('ok'):
        pprint.pprint(emoji_response.get('emoji'))
        errors = []
        aliases = []
        saved = []

        for emoji, link in emoji_response.get('emoji').items():
            if link.startswith('alias:'):
                aliases.append({emoji, link})
                continue

            # download file
            url_partitions = link.split('/')
            filename = f"{url_partitions[4]}.{unquote(url_partitions[5].split('.')[-1])}"
            filepath = f'{directory}/{filename}'

            # skip if exists
            if os.path.exists(filepath):
                continue

            try:
                saved_as = wget.download(link, out=filepath)
                saved.append(saved_as)
            except HTTPError:
                errors.append({emoji, link})

        if aliases:
            print('ALIASES:')
            pprint.pprint(aliases)

        if errors:
            print('ERRORS:')
            pprint.pprint(errors)

        print(f"Total emoji count: {len(emoji_response.get('emoji').keys())}")


if __name__ == '__main__':
    DIRECTORY = 'downloaded_emoji'
    SLACK_TOKEN = os.environ['SLACK_TOKEN']

    slack_client = slack.WebClient(SLACK_TOKEN)
    response = slack_client.auth_test()
    print(response)

    if not response.get('ok'):
        print(response.get('error'))
        exit

    download_emoji(slack_client, DIRECTORY)
