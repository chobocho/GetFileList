def get_chosung(input_string):
    chosung = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    result = []
    for c in input_string:
        if '가' <= c <= '힣':
            unicode = ord(c) - ord('가')
            result.append(chosung[unicode // 588])
        else:
            result.append(c)
    return ''.join(result)

