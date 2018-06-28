def main():
    my_str = 'April’s unit price is 9 yuan.'
    print(my_str)
    new_val = None
    for s in my_str:
        if s.isnumeric():
            new_val = s
            break
    print('转换前的数据类型为', type(new_val))
    num = int(new_val)
    print('转换后的数据类型为', type(num))


if __name__ == '__main__':
    main()
