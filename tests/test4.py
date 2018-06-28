from math import sqrt


def main():
    my_list = [x for x in range(10, 15)]
    for num in my_list:
        is_prime = True
        for i in range(2, int(sqrt(num))+1):
            if num % i == 0:
                is_prime = False
        if is_prime:
            print(f'{num}为质数')


if __name__ == '__main__':
    main()
