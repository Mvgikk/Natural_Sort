import generator
import math
import matplotlib.pyplot as plt
from sorter import *

def experiment():
    results = []
    test_record_numbers = [50, 100, 250, 500, 1000,2500, 5000, 10000, 20000, 50000]
    buffer_size = 512

    for n in test_record_numbers:
        print(n)
        generator.generate_records_to_file('exp', n)

        result = natural_sort('exp_' + str(n) + '.txt', buffer_size,show_tape=False)

        theory_pessimistic = 4 * n * math.ceil(math.log(n, 2)) / buffer_size
        theory_average = 4 * n * math.ceil(math.log(result[0], 2)) / buffer_size

        result.append(theory_pessimistic)
        result.append(theory_average)

        results.append(result)
        print(result)

    plt.figure(0)
    plt.figure(dpi=600)

    plt.title("Wykres zależności ilości operacji dyskowych od liczby rekordów")
    plt.xlabel('Ilosc rekordow')
    plt.ylabel('Ilosc operacji dyskowych')

    plt.plot(test_record_numbers, [r[1] + r[2] for r in results], label='Operacje dyskowe', color='yellow')
    plt.plot(test_record_numbers, [r[4] for r in results], label='Operacje dyskowe pesymistyczne', color='red')
    plt.plot(test_record_numbers, [r[5] for r in results], label='Operacje dyskowe srednio', color='green')
    plt.legend(['Operacje dyskowe', 'Operacje dyskowe pesymistyczne', 'Operacje dyskowe srednio'])
    plt.savefig('figure.png')




def main():
    user_input = input('Wygenerowac plik tekstowy z rekordami? y/n \n')

    if user_input == 'y':
        file_name = input('Podaj nazwe pliku: ')
        n = int(input('Podaj N: '))
        buffer_size = int(input('Podaj rozmiar bufora: '))
        show_tape = input('Czy chcesz wyswietlac kazda faze y/n \n')
        generator.generate_records_to_file(file_name, n)

        if show_tape == 'y':
            show_tape = True
        else:
            show_tape = False

        result = natural_sort(file_name + '_' + str(n) + '.txt', buffer_size, show_tape)
        print(f"Disk Writes : {result[1]}\n"
              f"Disk Reads : {result[2]}\n"
              f"Number of Phases : {result[3]}")

    elif user_input == 'n':
        file_name = input('Podaj nazwe pliku: ')
        buffer_size = int(input('Podaj rozmiar bufora: '))
        show_tape = input('Czy wyswietlac kazda faze y/n \n')

        if show_tape == 'y':
            show_tape = True
        else:
            show_tape = False

        result = natural_sort(file_name, buffer_size, show_tape)
        print(f"Disk Writes : {result[1]}\n"
              f"Disk Reads : {result[2]}\n"
              f"Number of Phases : {result[3]}")



if __name__ == '__main__':
    # experiment()
    main()