def main():
    def chk_str(func):
        def inner(*args, **kwargs):
            rst = func(*args, **kwargs)
            if rst == 'ok':
                return 'rst is %s' % rst
            else:
                return 'rst is failed: %s' % rst
        return inner

    @ chk_str
    def tst(data):
        return data

    print(tst('no'))

if __name__ == "__main__":
    main()