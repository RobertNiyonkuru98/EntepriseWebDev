def binary_search(array,target):
    left = 0
    right = len(array) - 1

    while left <= right:
        mid = (left + right)

        if array[mid] == target:
            return mid
        elif target < array[mid]:
            right = mid - 1
        else:
            left