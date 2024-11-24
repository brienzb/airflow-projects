from datetime import datetime
import requests
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from konlpy.tag import Okt


SEOUL_TIME_ZONE = ZoneInfo("Asia/Seoul")

KOMANTLE_URL = "https://semantle-ko.newsjel.ly/nearest1k"
KOMANTLE_START_DATE = datetime(2022, 4, 1, tzinfo=SEOUL_TIME_ZONE)

START_UNICODE = 0xAC00  # "가"
END_UNICODE = 0xD7A3    # "힣"

INITIAL_CONSONANTS = [
    "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
    "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
]


class Word:
    word: str               # 단어
    pos: str                # 품사 (명사, 동사, 형용사, 부사, 기타)
    initial_consonant: str  # 초성
    length: int             # 단어 길이


    def __init__(self, word: str):
        self.word = word
        self.pos = self._get_pos()
        self.initial_consonant = self._get_initial_consonant()
        self.length = self._get_length()


    def _get_pos(self) -> str:
        # TODO: 토크나이징 이슈
        # - 하나의 단어를 여러 개의 형태소로 분리해 정확한 품사 파악이 어려움 -> 로직 개선 필요
        # - Okt 토크나이저를 제외한 다른 토크나이저들은 토크나이징 하는데 많은 시간 소요됨 -> lazy evalution, memorizing 적용 필요
        tokenizer = Okt()
        pos_tags = tokenizer.pos(self.word)
        # print(pos_tags)
        
        pos_mapping = {
            "Noun": "명사",
            "Verb": "동사",
            "Adjective": "형용사",
            "Adverb": "부사",
        }
        
        for token, pos in pos_tags:
            if token == self.word:
                return pos_mapping.get(pos, "기타")
        return "기타"
    

    def _get_initial_consonant(self) -> str:
        result = []

        for char in self.word:
            if START_UNICODE <= ord(char) <= END_UNICODE:
                syllable_index = ord(char) - START_UNICODE
                initial_index = syllable_index // (21 * 28)   # 중성(가운데소리): 21개 * 종성(끝소리): 28개

                result.append(INITIAL_CONSONANTS[initial_index])
            else:
                continue
        
        return "".join(result)
    

    def _get_length(self) -> int:
        return len(self.word)


class WordManager:
    """
    [
        {
            "word_id": int,       # 단어 순위 (0: 정답)
            "word": Word,         # 단어
            "similarity": float,  # 유사도
        }
    ]
    """
    word_list: list = []


    def __init__(self, komantle_no: int):
        url = f"{KOMANTLE_URL}/{komantle_no}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"죄송합니다. {komantle_no}번째 꼬맨틀 정보를 찾을 수 없어 프로그램을 종료합니다.")
            exit(0)

        soup = BeautifulSoup(response.text, "html.parser")
        
        answer = soup.find("b", id="word").get_text(strip=True)
        self.word_list.append({"word_id": 0, "word": Word(answer), "similarity": 100})

        table = soup.find("table")
        rows = table.find_all("tr")[1:]

        for row in rows:
            columns = row.find_all("td")

            word_id = int(columns[0].get_text(strip=True))
            word = Word(columns[1].get_text(strip=True))
            similarity = float(columns[2].get_text(strip=True))

            self.word_list.append({"word_id": word_id, "word": word, "similarity": similarity})


    def get_word(self, word_id: int) -> str:
        return self._find_word(word_id)["word"].word


    def get_pos(self, word_id: int) -> str:
        return self._find_word(word_id)["word"].pos
    

    def get_initial_consonant(self, word_id: int) ->  str:
        return self._find_word(word_id)["word"].initial_consonant


    def get_length(self, word_id: int) -> int:
        return self._find_word(word_id)["word"].length


    def get_similarity(self, word_id: int) -> float:
        return self._find_word(word_id)["similarity"]


    def _find_word(self, word_id: int) -> dict:
        for word_dict in self.word_list:
            if word_id == word_dict["word_id"]:
                return word_dict
        return {}


def main():
    # TODO: 메인 로직 복잡도 이슈
    # - print 문 너무 많이 사용됨 -> 공통화 필요
    # - while 및 if 문 너무 많이 사용됨 -> 간소화 필요
    print("      +----------------------------+")
    print("      | Hello I'm Komantle Helper! |")
    print("      +----------------------------+")
    print("(\_/)  ")
    print("( •‿•) ")
    print("/ > <\ ")

    komantle_no = (datetime.now(tz=SEOUL_TIME_ZONE) - KOMANTLE_START_DATE).days

    # 꼬맨틀 회차 선택
    while True:
        print("")
        print(f"오늘은 {komantle_no}번째 꼬맨틀 입니다. 그대로 진행하시겠습니까?")
        print("1. 예")
        print("2. 아니오")
        print("Q. 종료")
        command = input("> ").strip().upper()

        if command == "Q":
            print("프로그램을 종료합니다. 다음에 또 만나요~ (_ _)")
            return
        elif command == "1":
            break
        elif command == "2":
            print("")
            print("진행하고 싶은 꼬맨틀 회차를 입력해주세요.")
            command = input("> ").strip().upper()

            if command.isdigit():
                komantle_no = int(command)
                break
            else:
                print("잘못된 입력 입니다. 숫자로 입력해 주세요.")
                continue
        else:
            print("잘못된 명령어 입니다. 다시 입력해주세요.")
            
    word_manager = WordManager(komantle_no)

    command_map = {
        "1": {"name": "품사", "func": word_manager.get_pos},
        "2": {"name": "초성", "func": word_manager.get_initial_consonant},
        "3": {"name": "단어 길이", "func": word_manager.get_length},
        "4": {"name": "유사도", "func": word_manager.get_similarity},
        "5": {"name": "단어", "func": word_manager.get_word},
    }

    # 꼬맨틀 헬퍼
    while True:
        print("")
        print("원하시는 명령어를 입력해 주세요.")
        for key, value in command_map.items():
            print(f"{key}. {value['name']} 확인")
        print("Q. 종료")
        command = input("> ").strip().upper()

        if command == "Q":
            print("프로그램을 종료합니다. 도움이 되셨길 바랍니다~ (_ _)")
            break
        elif command in ["1", "2", "3", "4", "5"]:
            while True:
                print("")
                print("확인하고자 하는 단어의 순위를 0 ~ 1000 사이 값으로 입력해 주세요. (0: 정답, B: 돌아가기)")
                target_command = input("> ").strip().upper()

                if target_command == "B":
                    print("처음 화면으로 돌아갑니다.")
                    break

                if target_command.isdigit():
                    word_id = int(target_command)
                    if 0 <= word_id <= 1000:
                        target_name = "정답" if word_id == 0 else f"{word_id}위"
                        func_name = command_map[command]["name"]
                        func_value = command_map[command]["func"](word_id)

                        print(f"{target_name} 단어의 {func_name}는(은) '{func_value}' 입니다.")
                        break
                    else:
                        print("잘못된 랭킹입니다. 0 ~ 1000 사이 값으로 입력해주세요.")
                        continue
                else:
                    print("잘못된 입력 입니다. 0 ~ 1000 혹은 B 를 입력해 주세요.")
                    continue
        else:
            print("잘못된 명령어 입니다. 다시 입력해주세요.")


if __name__ == "__main__":
    main()
