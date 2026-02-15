ones = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
tens = ["X", "XX", "XXX", "IX", "L", "LX", "LXX", "LXXX", "XC"]
hundreds = ["C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
thousand = "M"

def is_num_correct(num):

    if not 1 <= num <= 1000:
        return False
    else:
        return True

def one_digit(num):

    roman = ""

    if num[0]:
        roman += ones[int(num[0]) - 1]

    return roman

def two_digits(num):

    roman = ""

    if num[0]:
        roman += tens[int(num[0]) - 1]
    if num[1]:
        roman += ones[int(num[1]) - 1]

    return roman

def three_digits(num):

    roman = ""

    if num[0]:
        roman += hundreds[int(num[0]) - 1]
    if num[1]:
        roman += tens[int(num[1]) - 1]
    if num[2]:
        roman += ones[int(num[2]) - 1]

    return roman

def main():

    while True:
        num = input("Sisesta arv mida soovid teisendada: ")

        if not num.isdigit():
            print("Sisesta ARV!\n")
            continue

        if not is_num_correct(int(num)):
            print("Sisesta arv 1-1000!\n")
            continue

        break

    roman = ""
    if len(num) == 4:
        roman += thousand

    if len(num) == 3:
        roman = three_digits(num)

    if len(num) == 2:
        roman = two_digits(num)

    if len(num) == 1:
        roman = one_digit(num)

    print("\nSISESTATUD ARV ROOMA NUMBRINA:")
    print(roman)

if __name__ == "__main__":
    main()
