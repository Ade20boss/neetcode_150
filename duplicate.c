#include <stdio.h>
#include <stdbool.h>

int check_duplicate(const int *arr, int n)
{
    int current_index;
    bool found = false;
    for(int i = 0; i < n; i++)
    {
        current_index = i;
        for (int j = 0; j < n; j++)
        {
            if (j == current_index)
            {
                continue;
            }

            if (arr[i] == arr[j])
            {
                found = true;
                return found;
            }
        }
    }

    if (found == false)
    {
        return false;
    }

    return -1;
}







int main()
{
    int array[10] = {1,2,3,4,5,5,6,8,9,0};
    int length = sizeof(array)/sizeof(array[0]);
    printf("%d\n", check_duplicate(array, length));
    return 0;
}