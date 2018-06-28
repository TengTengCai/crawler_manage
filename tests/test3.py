def main():
    my_list = [x for x in range(1, 11)]
    print(my_list)
    # my_sum = sum(my_list)
    my_sum = get_sum(my_list)
    print(f'连和为{my_sum}')
    my_multi = get_multi(my_list)
    print(f'连乘为{my_multi}')
    pass


def get_sum(my_list):
    total = 0
    for i in my_list:
        total += i
    return total


def get_multi(my_list):
    multi = 1
    for i in my_list:
        multi *= i
    return multi


if __name__ == '__main__':
    main()
