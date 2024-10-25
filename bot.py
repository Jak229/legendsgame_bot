import time
import requests
from bs4 import BeautifulSoup

phpsessid = "айди сессии"


class Bot:
    def __init__(self, session_id: str):
        self.session_id = session_id  # PHPSESSID
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
        }  # headers

        self.ses = requests.Session()  # creating session
        self.ses.headers.update(self.headers)  # setting session headers
        self.ses.cookies.set(
            "PHPSESSID", self.session_id, domain="legendsgame.ru"
        )  # setting session cookies

    def __parseLogsF(self, html: str) -> str:
        """
        Parsing logs from battle.

        Arguments:
            html (str) — HTML from battle page

        Return:
            response (str) — battle log
        """

        response = ""
        bs_soup = BeautifulSoup(html, "html.parser")
        divs = bs_soup.find_all(
            "div",
            class_="pvp-log pvp-log-big flex-d flex-fd-r flex-ai-c flex-jc-sb border-radius3",
        )

        for i in divs:
            player = i.find("span", class_="dark-brown").text
            monster = i.find("a", class_="darkest-red standart5").text

            damage = i.find(
                lambda tag: tag.name == "b"
                and "pvp-log--bl" in tag.attrs.get("class", "")
            ).text

            if not response:
                response += f"\033[32m{player}\033[37m ударил \033[31m{monster} \033[37m-> \033[34m{damage}\n"
            else:
                response += f"\033[31m{monster}\033[37m ударил \033[32m{player} \033[37m-> \033[34m{damage}\033[37m "

        return response

    def forest(self, n: int = 10000) -> None:
        """
        Fights in forest.

        Arguments:
            n (int) — count battles

        Return:
            None
        """

        for _ in range(n):
            self.ses.get("https://legendsgame.ru/game/battle.php?turn=finish")
            self.ses.get("https://legendsgame.ru/game/forest.php?go=bot")
            self.ses.get("https://legendsgame.ru/game/battle.php?turn=start")
            monster = self.ses.get("https://legendsgame.ru/game/")

            while True:
                if "dragon_attack" in monster.text:
                    self.ses.get(
                        "https://legendsgame.spaces-games.com/game/battle.php?dragon_attack"
                    )

                monster = self.ses.get("https://legendsgame.ru/game/battle.php?turn=ok")
                logs = self.__parseLogsF(monster.text)
                print(logs)

                time.sleep(0.1)

                if "Победа" in monster.text or "Поражение" in monster.text:
                    bs_parser = BeautifulSoup(monster.text, "html.parser")

                    result = bs_parser.find_all("div", class_="lr-af flex-d flex-fd-c")[
                        1
                    ].text

                    print(
                        (
                            "\033[32mПобеда!\n"
                            if "Победа" in monster.text
                            else "\033[31mПоражение):\n"
                        )
                        + "\033[34m"
                        + result.replace("\n", " ").lstrip()
                        + "\033[37m"
                    )
                    print("—" * 50)
                    break


bot = Bot(phpsessid)  # __init__
bot.forest()
