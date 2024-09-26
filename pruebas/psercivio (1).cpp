#include <bits/stdc++.h> 
 
std::vector < std::vector < int >> v; 
std::vector < std::pair < int, long long > > globaleva; 
// funcion objetivo 
long long funcion(std::vector <int>& s) { 
  long long dism = 0; 
  for (int i = 0; i < v.size(); ++i) { 
    int dis = std::numeric_limits < int > ::max(); 
    for (int a: s) { 
      dis = std::min(dis, v[i][a]); 
    } 
    dism += dis; 
  } 
  return dism; 
} 
 
// combinacion de resultados 
std::vector < std::vector < int >> comsol(auto &a,int n){ 
   for (int i = 0; i < a.size(); ++i){ 
   	for (int j = 0; j < a[i].size() / 2; ++j){ 
   		 a[i][j] = (a[i][j] + a[i][ j + a[i].size() / 2] ) %  n; 
   	} 
   } 
   return a; 
} 
 
// remplazamineto de soluciones 
 
void  remplaza(auto &a, auto b){ 
	for (int i = 0; i < a.size(); ++i){ 
		 if(funcion(a[i]) > funcion (b) ){ 
		 	 a[i] = b; 
		 	 break; 
		 } 
   } 
} 
 
// generador de conjunto 
std::vector < std::vector < int >> conjuntop(int n, int tam, int espacio) { 
  std::vector < std::vector < int >> conjunto; 
  for (int i = 0; i < n; ++i) { 
    std::vector < int > per; 
    for (int r = 0; r < tam; ++r) { 
      per.push_back(rand() % espacio); 
    } 
    conjunto.push_back(per); 
  } 
  return conjunto; 
} 
 
 
 
 
/// mejoramiento del conjunto 
std::vector < std::vector < int >> mejora_conjuntop(int n, int tam,auto &conjunto){ 
    int m = std::numeric_limits < int > ::max(); 
    std::vector < long long  > eval_pr; 
    for(auto a : conjunto){ 
        m = std::min( m , (int)funcion(a) ); 
        eval_pr.push_back ( funcion(a)); 
    } 
    std::vector<std::pair<int,long long>> s; 
    for(int i = 0 ; i < eval_pr.size() ; ++i){ 
         s.push_back({ i ,abs(m - eval_pr[i] )}); 
    } 
    std::sort(s.begin(), s.end() ,[](auto a, auto b){ 
      return (a.second !=  b.second ? a.second < b.second : a.first < b.first); 
    }); 
 
    for(int i=0;;++i){ 
    	 if(s[i].second <= s[ s.size() / 2 ].second){ 
          for(int j= 0 ;j < conjunto[s[i].first].size() ; ++ j ){ 
              conjunto[s[i].first][j] = ((conjunto[s[i].first][j] + 1) % n ); 
          } 
    	 }else{ 
    	 	break; 
    	 } 
    } 
   return conjunto; 
} 
 
 
 
 
// generador del espacio de reprencia 
std::vector < std::vector < int >> b(std::vector < std::vector < int >> & conjunto, int tam) { 
  std::vector < std::vector < int >> r; 
  std::vector < std::pair < int, long long > > evaludor; 
 
  for (int i = 0; i < conjunto.size(); ++i) { 
    evaludor.push_back({ 
      i, 
      funcion(conjunto[i]) 
    }); 
  } 
  globaleva = evaludor; 
 
  std::sort(evaludor.begin(), evaludor.end(), [](auto a, auto b) { 
    return (a.second != b.second ? a.second < b.second : a.first < b.first); 
  }); 
 
  for (int i = 0; i < tam / 2; ++i) { 
      r.push_back(conjunto[evaludor[i].first]); 
  } 
 
  for (int i = 0; i < tam / 2; ++i) { 
    r.push_back(conjunto[rand() % conjunto.size()]); 
  } 
 
  return r; 
} 
 
 
long long funciondis(std::vector <int>& s) { 
  long long dism =std::numeric_limits < long long > ::min(); 
  for (int i = 0; i < v.size(); ++i) { 
    int dis = std::numeric_limits < int > ::max(); 
    for (int a: s) { 
      dis = std::min(dis, v[i][a]); 
    } 
    dism = (dis > dism ? dis:dism); 
  } 
  return dism; 
}

 

 
 
int iter = 100; 
// algoritmos 
void solve(int & p, int & n) { 
  std::vector < std::vector < int >> e = conjuntop(50, p, n); 
  e = mejora_conjuntop(n , p ,e); 
  std::vector < std::vector < int >> espacios = b(e, 10);  
 
  long long m_dis_gl = std::numeric_limits < long long > ::max(); 
  std::vector < int > mejorCombinacion; 
  for (int i = 0; i < iter; ++i) { 
    //e 
     for(auto c:e){ 
      remplaza(espacios,c); 
     } 
    mejorCombinacion = espacios [0]; 
    m_dis_gl = funcion(espacios[0]); 
    // convinacion 
    std::vector < std::vector < int >> temp = comsol(espacios , n ); 
    // mejora del espacio 
      for(auto j:temp){ 
            remplaza (espacios, j ); 
      } 
     // mejora de soluciones 
     e = mejora_conjuntop(n , p ,e); 
  } 
 
 
   std::cout<< "la mejor solucion fue\n"; 
   for (int i = 0; i < mejorCombinacion.size(); ++i){ 
      std::cout << mejorCombinacion[i] << " "; 
   } 
   std::cout<<"\ncon un valor de distancia maxima de " << m_dis_gl << " La distancia maxima a recorrer es "<< funciondis(mejorCombinacion) ;
 
} 
 
 
int main() { 
  int n; 
  std::cin >> n; 
  for (int i = 0; i < n; ++i) { 
    std::vector < int > arr; 
    for (int j = 0; j < n; ++j) { 
      int v; 
      std::cin >> v; 
      arr.push_back(v); 
    } 
    v.push_back(arr); 
  } 
  int p; 
  std::cin >> p; 
  solve(p , n); 
} 
 
 
// busqueda dispersa 
/* 
1. Generación de diversificación 
 
2. Mejoramiento 
 
3. Actualización de conjunto de 
referencia 
 
4. Generación de subconjuntos 
5. Combinación de soluciones 
*/ 
