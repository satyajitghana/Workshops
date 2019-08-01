#include<bits/stdc++.h> 
using namespace std; 
  
int find_root(int n) {     
    int s = 0;
    int e = n;
    int ans;    
    while (s <= e) {         
        int m = (s + e) / 2; 
        if (m*m == n) 
            return m; 
  
        if (m*m < n) { 
            s = m + 1; 
            ans = m; 
        }  
        else
            e = m-1;         
    } 
    return ans; 
} 
   
int main() {      
    int n = 11; 
    cout << find_root(n) << endl; 
    return 0;    
} 