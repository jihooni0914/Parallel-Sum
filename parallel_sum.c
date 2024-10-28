#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define CACHELINE_SIZE 64
#define ENTRIES_PER_CACHELINE (CACHELINE_SIZE / sizeof(int)) // 16
#define MAX_N 100000000

int* arr;
int n, p;

// thread-specific private data
typedef struct {
    int start;
    int end;
    long result;
} thread_data;

thread_data* t_data;

void* parallel_sum(void* arg)
{
    thread_data* data = (thread_data*)arg;

    long local_sum = 0;
    for (int i = data->start; i < data->end; i++) {
        local_sum += arr[i];
    }

    data->result = local_sum;
    return NULL;
}

int main(int argc, char* argv[])
{
    if (argc != 3) {
        fprintf(stderr, "usage: %s <n> <p>\n", argv[0]);
        return 1;
    }

    n = atoi(argv[1]);
    p = atoi(argv[2]);

    if (n > MAX_N || n <= 0) {
        fprintf(stderr, "error: please enter 1 <= n <= %d\n", MAX_N);
        return 1;
    }

    // printf("Size of array: %d, # of threads: %d\n", n, p);

    arr = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        arr[i] = i + 1;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    pthread_t threads[p];
    t_data = (thread_data*)malloc(p * sizeof(thread_data));

    int total_cachelines = n / ENTRIES_PER_CACHELINE + (n % ENTRIES_PER_CACHELINE > 0);
    int elements_per_thread = (total_cachelines / p + (total_cachelines % p > 0)) * ENTRIES_PER_CACHELINE;
    int current_size = n, i = 0;
    while (current_size > 0) {
        int chunk_size = elements_per_thread <= current_size ? elements_per_thread : current_size;
        current_size -= chunk_size;

        // printf("%d : %d : %d\n", i, current_size, chunk_size);

        t_data[i].start = i * elements_per_thread;
        t_data[i].end = t_data[i].start + chunk_size;
        pthread_create(&threads[i], NULL, parallel_sum, &t_data[i]);

        i++;
    }

    long sum = 0;
    for (int j = 0; j < i; j++) {
        pthread_join(threads[j], NULL);
        sum += t_data[j].result;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    // printf("\nresult: %ld\n", sum);
    // printf("Time taken for addition: %f seconds\n", elapsed_time);
    printf("%f", elapsed_time);

    free(arr);
    free(t_data);

    return 0;
}
