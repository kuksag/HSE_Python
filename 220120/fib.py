def get_fib(n: int):
    result = [0, 1]
    while len(result) < n:
        result.append(result[-1] + result[-2])
    return result