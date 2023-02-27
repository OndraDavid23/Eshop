def fuck(A, K):
    print(A)
    array = A
    array2 = []
    for x in range(0, len(A)):
        array2.append(A[x])
        try:
            array.pop(x)
            print(array)
            print(A)
        except:
            print("fuck")

        print(array2)









fuck([9,9,3,2], 2)    