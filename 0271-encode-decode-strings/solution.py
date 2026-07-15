def encode(array):
    encoded_str = []
    for word in array:
        word_length = len(word)
        encoded_string = str(word_length) + "#" + word
        encoded_str.append(encoded_string)

    return "".join(encoded_str)


def decode(enc):
    if enc == "":
        return []
    array = []
    i = 0
    while True:
        current_pos = i
        digits_stop = enc.find("#", i)
        digits_range = digits_stop - current_pos
        word_length = ""
        for j in range(digits_range):
            word_length += enc[current_pos + j]
        word_length = int(word_length)
        word = ""
        for k in range(word_length):
            word += enc[digits_stop + k + 1]

        array.append(word)

        i += digits_range + 1 + word_length

        if i == len(enc):
            return array


input = ["lint", "code", "love", "you"]
print(encode(input))
print(decode(encode(input)))
