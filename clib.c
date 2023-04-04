#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/////////////////////////////
///// Support functions /////
/////////////////////////////



void swap(int* xp, int* yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void emptyFunction(int array[], int n){}


// function to print array elements
void printArray(int array[], int size) {
  for (int i = 0; i < size; ++i) {
    printf("%'d  ", array[i]);
  }
  printf("\n");
  fflush(stdout);
}

bool is_sorted(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        if (arr[i] > arr[i+1]) {
            return false;
        }
    }
    return true;
}

/////////////////////////////
/////    BUBBLE SORT    /////
/////////////////////////////


// A function to implement bubble sort
void bubbleSort(int arr[], int n)
{
    int i, j;
    for (i = 0; i < n - 1; i++)

    // Last i elements are already in place
        for (j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1])
                swap(&arr[j], &arr[j + 1]);
}

void makeBubbles(int n){
    int my_array[n];
    srand(0);
    int i;
    for (i = 0; i < n; i++) {
        my_array[i] = rand();
    }

    bubbleSort(my_array, n);
}


/////////////////////////////
/////     QUICK SORT    /////
/////////////////////////////



// // function to find the partition position
int partition(int arr[], int low, int high) {

    // Select the pivot element 
    // by calculating the middle index between low and high
    int pivot = arr[(low + high) / 2];

    // Initialize two indices, i and j
    int i = low - 1;  // i will be incremented to the right
    int j = high + 1; // j will be decremented to the left

    // Loop until array is partitioned
    while (1) {
        // Increment i until it finds an element greater than or equal to the pivot
        do {
            i++;
        } while (arr[i] < pivot);

        // Decrement j until it finds an element less than or equal to the pivot
        do {
            j--;
        } while (arr[j] > pivot);

        // If i is greater than or equal to j, we have finished partitioning
        if (i >= j) {
            // Return the index of the last element in the left partition
            return j;
        }

        // Swap the elements at indices i and j
        swap(&arr[i], &arr[j]);
    }
}
    
// function to find the partition position

void quickSort(int array[], int low, int high) {
    if (low < high) {

    // find the pivot element such that
    // elements smaller than pivot are on left of pivot
    // elements greater than pivot are on right of pivot
    int pi = partition(array, low, high);

    // recursive call on the left of pivot
    quickSort(array, low, pi );

    // recursive call on the right of pivot
    quickSort(array, pi + 1, high);
  }
}

void quickSortC(int array[], int n){
    quickSort(array, 0, n-1);
}


/////////////////////////////
/////     MERGE SORT    /////
/////////////////////////////


// Merges two subarrays of arr[].
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
void merge(int arr[], int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
 
    /* create temp arrays */
    int L[n1], R[n2];
 
    /* Copy data to temp arrays L[] and R[] */
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
 
    /* Merge the temp arrays back into arr[l..r]*/
    i = 0; // Initial index of first subarray
    j = 0; // Initial index of second subarray
    k = l; // Initial index of merged subarray
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
 
    /* Copy the remaining elements of L[], if there
    are any */
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
 
    /* Copy the remaining elements of R[], if there
    are any */
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}
 
/* l is for left index and r is right index of the
sub-array of arr to be sorted */
void mergeSort(int arr[], int l, int r)
{
    if (l < r) {
        // Same as (l+r)/2, but avoids overflow for
        // large l and h
        int m = l + (r - l) / 2;
 
        // Sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
 
        merge(arr, l, m, r);
    }
}

void mergeSortC(int arr[], int n){
    mergeSort(arr, 0, n-1);
}



/////////////////////////////
/////     HEAP SORT     /////
/////////////////////////////


// To heapify a subtree rooted with node i
// which is an index in arr[].
// n is size of heap
void heapify(int arr[], int N, int i)
{
    // Find largest among root, left child and right child
 
    // Initialize largest as root
    int largest = i;
 
    // left = 2*i + 1
    int left = 2 * i + 1;
 
    // right = 2*i + 2
    int right = 2 * i + 2;
 
    // If left child is larger than root
    if (left < N && arr[left] > arr[largest])
 
        largest = left;
 
    // If right child is larger than largest
    // so far
    if (right < N && arr[right] > arr[largest])
 
        largest = right;
 
    // Swap and continue heapifying if root is not largest
    // If largest is not root
    if (largest != i) {
 
        swap(&arr[i], &arr[largest]);
 
        // Recursively heapify the affected
        // sub-tree
        heapify(arr, N, largest);
    }
}
 
// Main function to do heap sort
void heapSort(int arr[], int N)
{
 
    // Build max heap
    for (int i = N / 2 - 1; i >= 0; i--)
 
        heapify(arr, N, i);
 
    // Heap sort
    for (int i = N - 1; i >= 0; i--) {
 
        swap(&arr[0], &arr[i]);
 
        // Heapify root element to get highest element at
        // root again
        heapify(arr, i, 0);
    }
}
 