#include <bits/stdc++.h>

// Parámetros
double funcion(const std::vector<double>& x) { 
    double sum = 0.0; 
    for (double xi : x) { 
        sum += xi * xi - 10 * cos(2 * M_PI * xi) + 10; 
    } 
    return sum; 
} 
//    std::vector<double> F_values = {0.5, 0.7, 0.9};
//    std::vector<double> CR_values = {0.5, 0.7, 0.9};
double F =  0.02;  
double CR = 0.5;

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

void calcular_media_poblacion(const std::vector<std::vector<double>>& poblacion, std::vector<double>& fitness_media, std::vector<double>& fitness) {
    double suma_fitness = 0.0;
    for (const auto& individuo : poblacion) {
        double fit = funcion(individuo);
        fitness.push_back(fit);
        suma_fitness += fit;
    }
    fitness_media.push_back(suma_fitness / poblacion.size());
}

std::vector<double> encontrar_mas_cercano_y_lejano(const std::vector<double>& fitness, double media, double& mas_cercano, double& mas_lejano) {
    mas_cercano = fitness[0];
    mas_lejano = fitness[0];
    double menor_diferencia = fabs(fitness[0] - media);
    double mayor_diferencia = menor_diferencia;
    for (size_t i = 1; i < fitness.size(); ++i) {
        double diferencia = fabs(fitness[i] - media);
        if (diferencia < menor_diferencia) {
            menor_diferencia = diferencia;
            mas_cercano = fitness[i];
        }
        if (diferencia > mayor_diferencia) {
            mayor_diferencia = diferencia;
            mas_lejano = fitness[i];
        }
    }
    return {mas_cercano, mas_lejano};
}

std::vector<double> algo(int n_p, int n, int n_gen, bool best, std::string filename,int eje) {
    std::ofstream file(filename +std::to_string(eje) +".txt",std::ios_base::app);
    std::ofstream file2(filename+".txt",std::ios_base::app);
    std::vector<std::vector<double>> poblacion = gen_poblacion(n_p, n);
    std::vector<double> sol = poblacion[0]; 
    double best_fitness = funcion(sol); 
    std::uniform_real_distribution<> cruza(0.0, 1.0); 
    
    
    std::vector<double> fitness_media;
    std::vector<double> fitness_generacion;
    
    for (int r = 0; r < n_gen; ++r) {
        // Cálculo del fitness de la población actual
        calcular_media_poblacion(poblacion, fitness_media, fitness_generacion);
        
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
                    best_fitness = cruze_fitness; 
                } 
            } 
        }

        // Encontrar los individuos más cercanos y lejanos a la media
        double mas_cercano, mas_lejano;
        encontrar_mas_cercano_y_lejano(fitness_generacion, fitness_media.back(), mas_cercano, mas_lejano);
        
        // Escribir la media, el más cercano y el más lejano en el archivo
        file << fitness_media.back() << " " << mas_cercano 
             << " " << mas_lejano << "\n";

        fitness_generacion.clear();
        file2 <<best_fitness<<" ";
    }
    file2 <<"\n";
    file << "" << best_fitness << "\n";
    return sol;
}

int main() {
   
    for(int i = 0; i < 10;++i){
        auto s = algo(5, 50, 10, false, "randFCV",i);
    }

    for(int i = 0; i < 10;++i){
        auto s = algo(5, 50, 10, true, "bestFCV",i);
    }
}
