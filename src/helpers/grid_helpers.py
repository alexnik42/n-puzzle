def generate_snail_matrix_iteration_order(n: int) -> dict[tuple[int], tuple[int]]:
    matrix_iteration_order = {}

    row_begin, col_begin = 0, 0
    row_end, col_end = n - 1, n - 1
    prev = [n // 2, (n - 1) // 2]
    while (row_begin <= row_end and col_begin <= col_end):
        for i in range(col_begin, col_end + 1):
            matrix_iteration_order[tuple(prev)] = (row_begin, i)
            prev = [row_begin, i]
        row_begin += 1

        for i in range(row_begin, row_end + 1):
            matrix_iteration_order[tuple(prev)] = (i, col_end)
            prev = [i, col_end]
        col_end -= 1

        if (row_begin <= row_end):
            for i in range(col_end, col_begin-1, -1):
                matrix_iteration_order[tuple(prev)] = (row_end, i)
                prev = [row_end, i]
            row_end -= 1

        if (col_begin <= col_end):
            for i in range(row_end, row_begin-1, -1):
                matrix_iteration_order[tuple(prev)] = (i, col_begin)
                prev = [i, col_begin]
            col_begin += 1

    return matrix_iteration_order


def generate_target_snail_matrix(n: int) -> tuple[int]:
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    current_number = 1

    row_begin, col_begin = 0, 0
    row_end, col_end = n - 1, n - 1
    while (row_begin <= row_end and col_begin <= col_end):
        for i in range(col_begin, col_end + 1):
            matrix[row_begin][i] = current_number
            current_number += 1
        row_begin += 1

        for i in range(row_begin, row_end + 1):
            matrix[i][col_end] = current_number
            current_number += 1
        col_end -= 1

        if (row_begin <= row_end):
            for i in range(col_end, col_begin-1, -1):
                matrix[row_end][i] = current_number
                current_number += 1
            row_end -= 1

        if (col_begin <= col_end):
            for i in range(row_end, row_begin-1, -1):
                matrix[i][col_begin] = current_number
                current_number += 1
            col_begin += 1

    matrix[n // 2][(n - 1) // 2] = 0
    target_matrix = []
    for row in matrix:
        target_matrix += row
    return tuple(target_matrix)
