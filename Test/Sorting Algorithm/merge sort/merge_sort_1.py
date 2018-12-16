def sort(sorted_list):
    if len(sorted_list) <= 1:
        return sorted_list

    middle = len(sorted_list) // 2
    left = sorted_list[:middle]
    right = sorted_list[middle:]
    left = sort(left)
    right = sort(right)
    return merge(left, right)  

def merge(a_list, b_list):
    combined_list = []
    index_a = 0
    index_b = 0
    length_a = len(a_list)
    length_b = len(b_list)

    while index_a < length_a or index_b < length_b:
        if index_a < length_a and index_b < length_b:
            if a_list[index_b] <= b_list[index_b]:      #error!!! should be ==> if a_list[index_a] <= b_list[index_b]:
                combined_list += [a_list[index_a]]
                index_a = index_a + 1
            else:
                combined_list += [b_list[index_b]]
                index_b = index_b + 1
        elif index_a < length_a:
            combined_list += [a_list[index_a]]
            index_a = index_a +1
        else:
            combined_list += [b_list[index_b]]
            index_b = index_b + 1
    return combined_list


# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    b = sort(a)
    for e in b:
        print(e)

main()