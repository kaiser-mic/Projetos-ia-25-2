# -*- coding: utf-8 -*-

# Importa a biblioteca NumPy para cálculos numéricos eficientes, especialmente com vetores.
import numpy as np

# --- 1. FUNÇÃO OBJETIVO ---
# Esta é a função que queremos minimizar.
# No nosso caso, é a função Esfera: f(x, y) = x^2 + y^2.
# O 'x' aqui é um vetor, por exemplo, np.array([valor_x, valor_y]).
def funcao_objetivo(posicao):
    """
    Calcula o valor da função Esfera.
    O mínimo global desta função é 0, na posição (0, 0).
    """
    return np.sum(posicao**2)

# --- 2. CLASSE PARTÍCULA ---
# Representa cada "pássaro" do nosso enxame.
class Particula:
    def __init__(self, dimensoes, limites):
        """
        Inicializa uma partícula.
        - dimensoes: O número de variáveis do problema (2 no nosso caso: x e y).
        - limites: Uma tupla (min, max) que define o espaço de busca.
        """
        # Limites inferior e superior para a posição das partículas.
        limite_inferior, limite_superior = limites

        # Posição inicial aleatória dentro dos limites.
        self.posicao = np.random.uniform(limite_inferior, limite_superior, dimensoes)
        
        # Velocidade inicial aleatória.
        self.velocidade = np.random.uniform(-1, 1, dimensoes)
        
        # A melhor posição pessoal (pbest) começa sendo a posição inicial.
        self.melhor_posicao_pessoal = self.posicao.copy()
        
        # Calcula o valor da melhor posição pessoal usando a função objetivo.
        self.valor_melhor_pessoal = funcao_objetivo(self.posicao)

# --- 3. ALGORITMO PSO ---
# Orquestra todo o processo de otimização.
class PSO:
    def __init__(self, objetivo, limites, num_particulas, iteracoes):
        """
        Inicializa o enxame de partículas.
        - objetivo: A função que queremos minimizar.
        - limites: Os limites do espaço de busca.
        - num_particulas: O tamanho do enxame.
        - iteracoes: O número de vezes que o enxame vai interagir.
        """
        self.funcao_objetivo = objetivo
        self.limites = limites
        self.num_particulas = num_particulas
        self.iteracoes = iteracoes
        self.dimensoes = len(limites[0]) # Assume que limites é ((min_x, min_y), (max_x, max_y))

        # Variáveis do PSO
        self.w = 0.5  # Inércia: o quanto a partícula mantém sua velocidade atual.
        self.c1 = 1.5 # Coeficiente cognitivo: atração pela melhor posição pessoal (pbest).
        self.c2 = 1.5 # Coeficiente social: atração pela melhor posição global (gbest).
        
        # Inicializa a melhor posição global (gbest) como infinito, pois estamos minimizando.
        self.melhor_posicao_global = None
        self.valor_melhor_global = float('inf')
        
        # Cria o enxame de partículas.
        self.enxame = [Particula(self.dimensoes, (self.limites[0][0], self.limites[1][0])) for _ in range(num_particulas)]
        
    def otimizar(self):
        """
        Executa o loop principal do algoritmo PSO.
        """
        # Histórico para acompanhar a melhoria a cada iteração (ótimo para gráficos).
        historico_gbest = []

        for i in range(self.iteracoes):
            # Para cada partícula no enxame...
            for particula in self.enxame:
                # 1. Avalia a aptidão (fitness) da partícula
                valor_atual = self.funcao_objetivo(particula.posicao)
                
                # 2. Atualiza a melhor posição pessoal (pbest)
                if valor_atual < particula.valor_melhor_pessoal:
                    particula.melhor_posicao_pessoal = particula.posicao.copy()
                    particula.valor_melhor_pessoal = valor_atual
                
                # 3. Atualiza a melhor posição global (gbest)
                if valor_atual < self.valor_melhor_global:
                    self.melhor_posicao_global = particula.posicao.copy()
                    self.valor_melhor_global = valor_atual
            
            # Para cada partícula, atualiza sua velocidade e posição
            for particula in self.enxame:
                # Gera números aleatórios para os componentes cognitivo e social
                r1 = np.random.rand(self.dimensoes)
                r2 = np.random.rand(self.dimensoes)

                # Equação de atualização da velocidade
                # v(t+1) = w*v(t) + c1*r1*(pbest - x(t)) + c2*r2*(gbest - x(t))
                velocidade_cognitiva = self.c1 * r1 * (particula.melhor_posicao_pessoal - particula.posicao)
                velocidade_social = self.c2 * r2 * (self.melhor_posicao_global - particula.posicao)
                particula.velocidade = (self.w * particula.velocidade) + velocidade_cognitiva + velocidade_social

                # Atualiza a posição da partícula
                # x(t+1) = x(t) + v(t+1)
                particula.posicao += particula.velocidade

                # Garante que a partícula não saia dos limites do espaço de busca.
                particula.posicao = np.clip(particula.posicao, self.limites[0][0], self.limites[1][0])

            # Guarda o melhor valor da iteração no histórico
            historico_gbest.append(self.valor_melhor_global)
            
            # Imprime o progresso a cada 10 iterações
            if (i + 1) % 10 == 0:
                print(f"Iteração {i+1:4d}: Melhor Valor = {self.valor_melhor_global:.6f}")

        return self.melhor_posicao_global, self.valor_melhor_global, historico_gbest

# --- 4. EXECUÇÃO DO ALGORITMO ---
if __name__ == "__main__":
    # Parâmetros do problema
    # Limites do espaço de busca para cada dimensão (x e y)
    limites = ([-10, -10], [10, 10]) 
    
    # Parâmetros do PSO
    num_particulas = 30
    iteracoes = 100
    
    # Cria uma instância do otimizador PSO
    otimizador = PSO(funcao_objetivo, limites, num_particulas, iteracoes)
    
    # Executa a otimização
    melhor_posicao, melhor_valor, historico = otimizador.otimizar()
    
    # Imprime os resultados finais
    print("\n--- Otimização Concluída ---")
    print(f"Melhor posição encontrada (x, y): {melhor_posicao}")
    print(f"Valor mínimo da função: {melhor_valor}")