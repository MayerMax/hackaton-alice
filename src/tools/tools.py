def count_ones(letter_matrix):
    return sum(sum(line) for line in letter_matrix)