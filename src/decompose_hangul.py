# 한글 초성, 중성, 종성 매핑
# 초성 매핑 (예시)
CHOSEONG_LIST = [
    "g",   # ㄱ
    "kk",  # ㄲ
    "n",   # ㄴ
    "d",   # ㄷ
    "tt",  # ㄸ
    "r",   # ㄹ
    "m",   # ㅁ
    "b",   # ㅂ
    "pp",  # ㅃ
    "s",   # ㅅ
    "ss",  # ㅆ
    "",    # ㅇ (초성에서는 발음되지 않음)
    "j",   # ㅈ
    "jj",  # ㅉ
    "ch",  # ㅊ
    "k",   # ㅋ
    "t",   # ㅌ
    "p",   # ㅍ
    "h"    # ㅎ
]

# 중성 매핑 (예시)
JUNGSEONG_LIST = [
    "a",    # ㅏ
    "ae",   # ㅐ
    "ya",   # ㅑ
    "yae",  # ㅒ
    "eo",   # ㅓ
    "e",    # ㅔ
    "yeo",  # ㅕ
    "ye",   # ㅖ
    "o",    # ㅗ
    "wa",   # ㅘ
    "wae",  # ㅙ
    "oe",   # ㅚ
    "yo",   # ㅛ
    "u",    # ㅜ
    "wo",   # ㅝ
    "we",   # ㅞ
    "wi",   # ㅟ
    "yu",   # ㅠ
    "eu",   # ㅡ
    "ui",   # ㅢ
    "i"     # ㅣ
]

# 종성 매핑 (예시, 수정된 값 포함)
JONGSEONG_LIST = [
    "",    # 0: 없음
    "k",   # 1: ㄱ
    "k",   # 2: ㄲ
    "k",   # 3: ㄳ
    "n",   # 4: ㄴ
    "n",   # 5: ㄵ
    "n",   # 6: ㄶ
    "t",   # 7: ㄷ
    "l",   # 8: ㄹ
    "k",   # 9: ㄺ
    "m",   # 10: ㄻ
    "p",   # 11: ㄼ
    "l",   # 12: ㄽ
    "l",   # 13: ㄾ
    "p",   # 14: ㄿ
    "t",   # 15: ㅀ
    "m",   # 16: ㅁ
    "p",   # 17: ㅂ (수정된 부분)
    "p",   # 18: ㅄ
    "t",   # 19: ㅅ
    "t",   # 20: ㅆ
    "ng",  # 21: ㅇ
    "t",   # 22: ㅈ
    "t",   # 23: ㅊ
    "k",   # 24: ㅋ
    "t",   # 25: ㅌ
    "p",   # 26: ㅍ
    "t"    # 27: ㅎ
]

def decompose_hangul(char):
    code = ord(char)
    if 0xAC00 <= code <= 0xD7A3:
        code_offset = code - 0xAC00
        choseong_index = code_offset // (21 * 28)
        jungseong_index = (code_offset % (21 * 28)) // 28
        jongseong_index = code_offset % 28
        return (CHOSEONG_LIST[choseong_index],
                JUNGSEONG_LIST[jungseong_index],
                JONGSEONG_LIST[jongseong_index])
    else:
        return (char, "", "")

def romanize(text):
    result = ""
    for char in text:
        if 0xAC00 <= ord(char) <= 0xD7A3:
            ch, ju, jo = decompose_hangul(char)
            result += ch + ju + jo
        else:
            result += char
    return result

def capitalize_words(text):
    # 공백 기준으로 단어를 구분한 후 첫 글자만 대문자로 변환
    return ' '.join(word.capitalize() for word in text.split())

# 테스트 예제
sample = "곱창 전골 김치 찌게"

romanized = romanize(sample)
capitalized = capitalize_words(romanized)
print(capitalized)