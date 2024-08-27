#include <bits/stdc++.h> 
 
// Parámetros 
double funcion(const std::vector<double>& x) { 
    double sum = 0.0; 
    for (double xi : x) { 
        sum += xi * xi - 10 * cos(2 * M_PI * xi) + 10; 
    } 
    return sum; 
} 
 
double F =  0.02; 
double CR = 0.5; 
 
//double F =  0.2; 
//double CR = 0.8; 
 
std::random_device rd; 
std::mt19937 gen(rd()); 
 
std::vector<std::vector<double>> gen_poblacion(int n_p, int n){ 
    std::uniform_real_distribution<> dis(-4.0, 4.0); 
    std::vector<std::vector<double>> poblacion(n); 
    for (int i = 0; i < n; ++i){ 
        for(int j = 0; j < n_p; ++j ){ 
            poblacion[i].push_back(dis(gen)); 
        } 
    } 
    return poblacion; 
} 
void imprimepo( std::vector<std::vector<double>>& a){ 
     for (int i = 0; i < 50; ++i){ 
      std::cout<<i<<" "; 
        for (double j : a[i] ){ 
            std::cout<< j <<" "; 
        } 
        std::cout<<"\n"; 
    } 
} 
 
std::vector<double> calcular_media_poblacion(const std::vector<std::vector<double>>& poblacion) { 
    double s = 0.0; 
    std::vector<double> xi; 
    for (int i = 0; i < 5; ++i){ 
        for (int j = 0; j < 50; ++j){ 
             s += poblacion[j][i]; 
        } 
     xi.push_back( s / 50 ); 
    } 
    return xi; 
} 
 
 
 
std::vector<std::pair<double,double>> encontrar_mas_cercano_y_lejano(const std::vector<std::vector<double>>& poblacion, std::vector<double>& media) { 
    std::vector<std::pair<double,double>> res; 
 
    for (int i = 0; i < 5; ++i){ 
         double maximo_me = abs( media[i] - poblacion[0][i]); 
         double menor_me = maximo_me; 
         double v_mayor = poblacion[0][i]; 
         double v_menor = poblacion[0][i]; 
        for (int j = 0; j < 50; ++j){ 
             if(abs(media[i] - poblacion[j][i] ) < menor_me){ 
                 menor_me = abs(media[i] - poblacion[j][i] ); 
                 v_menor = poblacion[j][i]; 
             } 
             if(abs(media[i] - poblacion[j][i] ) > maximo_me){ 
                 menor_me = abs(media[i] - poblacion[j][i] ); 
                 v_menor = poblacion[j][i]; 
             } 
        } 
        res.push_back({v_menor , v_mayor }); 
    } 
    return res; 
} 
 
 
std::vector<double> algo(int n_p, int n, int n_gen, bool best, std::string filename,int eje) { 
    std::ofstream file(filename +std::to_string(eje) +"media.txt",std::ios_base::app); 
    std::ofstream file2(filename+".txt",std::ios_base::app); 
    std::ofstream file3(filename +std::to_string(eje) +"mas_lejano.txt",std::ios_base::app); 
    std::ofstream file4(filename +std::to_string(eje) +"mas_cerca.txt",std::ios_base::app); 
    std::ofstream file5(filename +"mejor.txt",std::ios_base::app); 
    


    std::vector<std::vector<double>> poblacion = gen_poblacion(n_p, n); 
    std::vector<double> sol = poblacion[0]; 
    double best_fitness = funcion(sol); 
    std::uniform_real_distribution<> cruza(0.0, 1.0); 
    
    int nuemro = 0;
    for (int r = 0; r < n_gen; ++r) { 
        // Cálculo del fitness de la población actual 
 
        // Selección de tres aleatorios pero no el actual 
        for(int i = 0;  i < n; ++i) { 
            int r1, r2, r3; 
            do { 
                r1 = gen() % n; 
                r2 = gen() % n; 
                r3 = gen() % n; 
            } while (r1 == i || r2 == i || r3 == i || r1 == r2 || r1 == r3 || r2 == r3); 
 
            std::vector<double> mutancion(n_p); 
            for (int j = 0; j < n_p; ++j) { 
                if (best) { 
                    mutancion[j] = sol[j] + F * (poblacion[r1][j] - poblacion[r2][j]); 
                } else { 
                    mutancion[j] = poblacion[r1][j] + F * (poblacion[r2][j] - poblacion[r3][j]); 
                } 
                mutancion[j] = std::max(-4.0, std::min(4.0, mutancion[j])); 
            } 
 
            std::vector<double> cruze(n_p); 
            int j_rand = gen() % n_p; 
            for (int j = 0; j < n_p; ++j) { 
                if (j == j_rand || cruza(gen) < CR) { 
                    cruze[j] = mutancion[j]; 
                } else { 
                    cruze[j] = poblacion[i][j]; 
                } 
            } 
 
            double cruze_fitness = funcion(cruze); 
            if (cruze_fitness < funcion(poblacion[i])) { 
                poblacion[i] = cruze; 
                if (cruze_fitness < best_fitness) { 
                    sol = cruze; 
                    nuemro = r;
                    best_fitness = cruze_fitness; 
                } 
            } 
 
 
        } 
 
        // Encontrar los individuos más cercanos y lejanos a la media 
        std::vector<double> w = calcular_media_poblacion(poblacion); 
        for(double e:w){ 
           file << e <<" "; 
        } 
        file << "\n";
 
        std::vector<std::pair<double,double>>valores = encontrar_mas_cercano_y_lejano(poblacion , w ); 
        for(auto e:valores){ 
            file3 << e.first <<" "; 
        }
        file3 << "\n"; 

        for(auto e:valores){ 
           file4<< e.second <<" "; 
        } 
        file4 << "\n";
      file2 << "" << best_fitness << " "; 
    } 
    file2 <<"\n";
    file5 << best_fitness << " " << nuemro<<"\n";
    return sol; 
} 
 
int main() { 
 
    for(int i = 0; i < 10;++i){ 
        auto s = algo(5, 50, 10, false, "rand",i); 
    } 
 
    for(int i = 0; i < 10;++i){ 
        auto s = algo(5, 50, 10, true, "best",i); 
    } 
 
} 