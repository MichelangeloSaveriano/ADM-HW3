from random import randint


def max_substring_length_idx_recursive(s, idx):
    # String S, index idx -> X[idx] = the length of the longest sequence of characters
    #                                 in alphabetical order that terminates at the idx-th character
    # Return:
    #   X[idx] = 1 + max{X[j]; j = 0, ..., i-1, such that S[j]<S[idx]}
    #   X[idx] = 1, if there does not exist such a j
    return 1 + max([0] + [max_substring_length_idx_recursive(s, j) for j in range(idx) if s[j] < s[idx]])


def max_substring_length_recursive(s):
    return max_substring_length_idx_recursive(s + chr(ord('Z') + 1), len(s)) - 1


def max_substring_length_dynamic_programming(s):
    max_lengths = []  # This is our Dynamic Programming vector.
    # The i-th element of the vector contains the couple (S[i], X[i])

    # Loop through the string s to fill the D.P. vector
    for i in range(len(s)):
        max_x_j = 0
        for s_j, x_j in max_lengths:
            if s_j < s[i] and max_x_j < x_j:
                max_x_j = x_j
        max_lengths.append((s[i], max_x_j+1))

    # Return the maximum X[i] in the D.P. vector
    return max(max_lengths, key=lambda x: x[1])[1]


def create_long_string(size=100):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return alphabet * size


def create_short_string(max_substring_length, n_trash_char=1):
    # Fix input variable if out of bounds
    if n_trash_char < 0:
        n_trash_char = 0
    if max_substring_length <= 0:
        max_substring_length = 1
    elif max_substring_length > 26:
        max_substring_length = 26
    s = ''  # Create an empty string
    idx_char = ord('A')  # Calculate index of char A
    # For
    for _ in range(max_substring_length-1):
        s += chr(idx_char)
        s += 'Z' * n_trash_char
        idx_char += 1
    s += chr(idx_char)
    return s


if __name__ == '__main__':
    # Test the functions on short string
    n_test = 10
    print('Tests on short string')
    for _ in range(n_test):
        max_substr_len = randint(1, 26)
        S = create_short_string(max_substr_len)
        print('Max Substring Length:', max_substr_len,
              '- Recursive Function Output:', max_substring_length_recursive(S),
              '- DP Function Output:', max_substring_length_recursive(S))

    # Test the functions on long string
    print()
    print('Tests on long string')
    S = create_long_string()
    print('String S maximum substring length: 26')
    print('Dynamic Programming Function Output:', max_substring_length_dynamic_programming(S))
    # Using the string S the recursive algorithm does not terminate in reasonable time
    # print('Recursive Function Output:', max_substring_length_recursive(S))
