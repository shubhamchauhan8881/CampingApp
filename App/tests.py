arr = [2, 1, 5, 10, 23,0]

def sort(a):
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i-1

        while( j >= 0 and a[j] > key ):
            print(a)
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key

sort(arr)
print(arr)
