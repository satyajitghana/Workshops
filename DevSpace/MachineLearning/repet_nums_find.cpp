#include <bits/stdc++.h>

using namespace std;

int binary_search(int *a, int s, int e, int key) {
    int ans = -1;

    while (s <= e) {
        int mid = (s+e)/2;
        
        if (a[mid] == key) {
            ans = mid;
            e = mid - 1;
        } else if (a[mid] > key) {
            e = mid - 1;
        } else {
            s = mid + 1;
        }
    }
}