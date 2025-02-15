def save_data(count_dies, count_kills, count_levels):
    with open('data_base.txt', mode='r') as file:
        lst = list(map(int, file.readline().split()))

    with open('data_base.txt', mode='w') as file:
        file.write(f"{lst[0] + count_dies} {lst[1] + count_kills} {lst[2] + count_levels}")

def get_data():
    with open('data_base.txt', mode='r') as file:
        return list(map(int, file.readline().split()))
