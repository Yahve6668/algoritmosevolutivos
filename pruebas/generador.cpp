#include <bits/stdc++.h>


int main(){
   int n ;
   std::cin>> n;
   std::cout << n<<"\n";
   int mat[n][n] = { } ;
   	for (int i = 0; i < n; ++i){
		for(int j = 0; j < n ; ++j){
           if(j!=i && mat[ i ][ j ] == 0 ){
              int r = rand();
              std::cout << ( j!=i ? r : 0 ) << " " ;
              mat[ i ][ j ] = r;
              mat[ j ][ i ] = r;    
           }else{
              std::cout << mat[ j ][ i ] <<" ";
           }
        }
        std::cout << "\n" ;
	}
   std::cout << (n % 5 != 0 ? n / 5 + 1 : ( n / 5)  );  
}