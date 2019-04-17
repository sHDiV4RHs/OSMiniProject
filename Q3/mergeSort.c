#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

int M = 8;

void merge(int a[], int l, int mid, int h) {
    int count = h-l+1;
    int sorted[count];
    int i = l, k = mid+1, m = 0;
    while(i<=mid && k<=h) {
        if (a[i] < a[k])
            sorted[m++] = a[i++];
        else if(a[k] < a[i])
            sorted[m++] = a[k++];
        else {
            sorted[m++] = a[i++];
            k++;
        }
    }

    while(i <= mid)
        sorted[m++] = a[i++];

    while(k<=h)
        sorted[m++] = a[k++];

    i = 0;
    while(i < count) {
        a[l++] = sorted[i++];
    }
}

void mergeSort(int a[], int l, int h) {
    if(h <= l)
        return;

    int mid = (h + l)/2;
    int len = h - l + 1;
    if(len <= M) {
        mergeSort(a, l, mid);
        mergeSort(a, mid+1, h);
    } else {
        pid_t lpid, rpid;
        lpid = fork();

        if (lpid == 0) {
            mergeSort(a, l, mid);
            _exit(0);
        }

        rpid = fork();
        if (rpid == 0) {
            mergeSort(a, mid + 1, h);
            _exit(0);
        }

        int status;
        waitpid(lpid, &status, 0);
        waitpid(rpid, &status, 0);
    }

    merge(a, l, mid, h);
}

void isSorted(const int* arr, int len)
{
    for(int i = 0; i < len - 1; i++)
    {
//        printf("%d, ", arr[i]);
        if (arr[i+1] < arr[i]) {
            printf("Not Sorted\n");
            return;
        }
    }
    printf("Sorted\n");
}

int main() {
    double total_time;
    clock_t start, end;

    int length = 10000;

    int *shm_array;
    size_t SHM_SIZE = sizeof(int)*length;
    int shMID;
    key_t key = IPC_PRIVATE;
    shMID = shmget(key, SHM_SIZE, IPC_CREAT | 0666);
    shm_array = shmat(shMID, NULL, 0);

    srand(time(NULL));
    for (int i = 0; i < length; i++)
        shm_array[i] = rand();

    start = clock();
    mergeSort(shm_array, 0, length-1);
    end = clock();

    total_time = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("%f s\n", total_time);

    isSorted(shm_array, length);

    shmdt(shm_array);
    shmctl(shMID, IPC_RMID, NULL);

    return 0;
}
