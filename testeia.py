import random
import copy

# ==============================================================================
# 1. BASE DE DADOS (Campeão e Itens)
# ==============================================================================
# Documentação:
# Aqui definimos os dados do jogo que nosso algoritmo usará.
# - 'LUCIA_LV18': Status base do Lucian no nível 18.
# - 'TARGET_DUMMY': O alvo que o Lucian vai atacar.
# - 'ITEMS': Um dicionário com os itens disponíveis e seus atributos.
#   - 'ad': Dano de Ataque
#   - 'as_bonus_percent': Bônus de Velocidade de Ataque em porcentagem
#   - 'crit_chance': Chance de Acerto Crítico em porcentagem (0 a 100)
#   - 'cost': Custo do item (não usado no cálculo, mas bom para referência)

LUCIA_LV18 = {
    'base_ad': 113,
    'base_as': 0.638,  # Velocidade de Ataque base na qual os bônus se aplicam
    'as_ratio': 0.638, # Ratio para cálculo de AS
    'crit_damage_multiplier': 1.75 # Dano crítico padrão (175%)
}

TARGET_DUMMY = {
    'health': 3000,
    'armor': 100
}

# Lista simplificada de itens de ADC
ITEMS = {
    "Adagas Navori": {'ad': 65, 'crit_chance': 20, 'haste': 15},
    "Gume do Infinito": {'ad': 70, 'crit_chance': 20},
    "Mata-Cráquens": {'ad': 50, 'as_bonus_percent': 35, 'crit_chance': 20},
    "A Sanguinária": {'ad': 55, 'crit_chance': 20, 'lifesteal': 15},
    "Lembranças do Lorde Dominik": {'ad': 40, 'crit_chance': 20, 'armor_pen_percent': 35},
    "Dançarina Fantasma": {'as_bonus_percent': 30, 'crit_chance': 20, 'move_speed': 7},
    "Canhão Fumegante": {'ad': 35, 'as_bonus_percent': 15, 'crit_chance': 20},
    "Colhedor de Essência": {'ad': 60, 'crit_chance': 20, 'haste': 20},
    "Sedenta por Sangue": {'ad': 80, 'crit_chance': 20},
    "Arco-escudo Imortal": {'ad': 55, 'crit_chance': 20, 'lifesteal': 10},
    "Grevas do Berserker": {'as_bonus_percent': 35} # Bota
}

# Convertendo o dicionário de itens em uma lista para fácil acesso por índice
ITEM_LIST = list(ITEMS.items())
NUM_ITEMS = len(ITEM_LIST)

# ==============================================================================
# 2. FUNÇÃO DE FITNESS (CÁLCULO DE DPS)
# ==============================================================================
# Documentação:
# Esta função é o coração da nossa simulação. Ela mede a "qualidade" de uma build.
# Recebe: uma lista de 6 índices de itens (a build).
# Retorna: o valor de DPS (um número float).
def calculate_dps(build_indices):
    total_ad = LUCIA_LV18['base_ad']
    total_as_bonus_percent = 0
    total_crit_chance = 0
    
    # Soma os status de todos os itens na build
    for index in build_indices:
        item_name, stats = ITEM_LIST[index]
        total_ad += stats.get('ad', 0)
        total_as_bonus_percent += stats.get('as_bonus_percent', 0)
        total_crit_chance += stats.get('crit_chance', 0)

    # Garante que a chance de crítico não passe de 100%
    total_crit_chance = min(total_crit_chance, 100)
    
    # Calcula a velocidade de ataque final
    # Fórmula do LoL: AS = BaseAS * (1 + (Soma dos Bônus de AS / 100))
    final_as = LUCIA_LV18['base_as'] * (1 + total_as_bonus_percent / 100)
    
    # O Gume do Infinito aumenta o dano de crítico
    crit_damage_multiplier = LUCIA_LV18['crit_damage_multiplier']
    if "Gume do Infinito" in [ITEM_LIST[i][0] for i in build_indices]:
        if total_crit_chance >= 60:
            crit_damage_multiplier += 0.35 # Bônus do Gume do Infinito

    # Calcula o dano médio por ataque, considerando o crítico
    crit_chance_decimal = total_crit_chance / 100
    average_damage_per_hit = (total_ad * (1 - crit_chance_decimal)) + \
                             (total_ad * crit_damage_multiplier * crit_chance_decimal)
                             
    # Calcula o dano considerando a armadura do alvo
    # Fórmula do LoL: Redução = Armadura / (100 + Armadura)
    # Multiplicador de Dano = 1 - Redução = 100 / (100 + Armadura)
    damage_multiplier = 100 / (100 + TARGET_DUMMY['armor'])
    
    final_dps = average_damage_per_hit * final_as * damage_multiplier
    
    return final_dps

# ==============================================================================
# 3. IMPLEMENTAÇÃO DO ALGORITMO PSO
# ==============================================================================
# Documentação:
# Esta classe define o comportamento de uma "Partícula" no nosso enxame.
# Cada partícula representa uma build candidata.
class Particle:
    def __init__(self):
        # Posição: uma build de 6 itens únicos aleatórios
        self.position = random.sample(range(NUM_ITEMS), 6)
        # Velocidade: representa a "probabilidade" de mudar um item
        self.velocity = [0.0] * 6
        # Melhor Posição Pessoal: a melhor build que esta partícula já encontrou
        self.best_position = copy.deepcopy(self.position)
        # Melhor Fitness Pessoal: o DPS da melhor build pessoal
        self.best_fitness = calculate_dps(self.position)

# Documentação:
# Esta função executa o algoritmo PSO.
def particle_swarm_optimization(num_particles, num_iterations):
    # Parâmetros do PSO
    w = 0.5  # Inércia: o quanto a partícula mantém sua direção
    c1 = 1.5 # Fator cognitivo: o quanto a partícula confia em sua própria melhor experiência
    c2 = 1.5 # Fator social: o quanto a partícula confia na melhor experiência do enxame

    # 1. Inicialização
    swarm = [Particle() for _ in range(num_particles)]
    global_best_position = None
    global_best_fitness = -1

    # Encontra a melhor partícula inicial
    for p in swarm:
        if p.best_fitness > global_best_fitness:
            global_best_fitness = p.best_fitness
            global_best_position = copy.deepcopy(p.position)
            
    # 2. Loop de Iterações
    for i in range(num_iterations):
        print(f"Iteração {i+1}/{num_iterations} - Melhor DPS até agora: {global_best_fitness:.2f}")
        
        for p in swarm:
            # 3. Atualiza a velocidade de cada partícula (de forma discreta)
            for d in range(6): # Para cada um dos 6 slots de item
                r1 = random.random()
                r2 = random.random()
                
                # A "velocidade" é uma tendência para se mover em direção à melhor posição pessoal e global
                cognitive_velocity = c1 * r1 * (p.best_position[d] - p.position[d])
                social_velocity = c2 * r2 * (global_best_position[d] - p.position[d])
                p.velocity[d] = w * p.velocity[d] + cognitive_velocity + social_velocity

            # 4. Atualiza a posição (a build) com base na velocidade
            new_position = list(p.position)
            for d in range(6):
                # Se a "velocidade" for forte o suficiente, tenta trocar o item
                if random.random() < abs(p.velocity[d]) / (NUM_ITEMS): # Normaliza a velocidade
                    # Escolhe um novo item que ainda não esteja na build
                    possible_new_items = [idx for idx in range(NUM_ITEMS) if idx not in new_position]
                    if possible_new_items:
                        new_item_index = random.choice(possible_new_items)
                        new_position[d] = new_item_index
            
            p.position = new_position
            
            # 5. Calcula o fitness da nova posição
            current_fitness = calculate_dps(p.position)
            
            # 6. Atualiza a melhor posição pessoal e global
            if current_fitness > p.best_fitness:
                p.best_fitness = current_fitness
                p.best_position = copy.deepcopy(p.position)
                
                if current_fitness > global_best_fitness:
                    global_best_fitness = current_fitness
                    global_best_position = copy.deepcopy(p.position)
                    
    return global_best_position, global_best_fitness

# ==============================================================================
# 4. EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    # Configurações do experimento
    NUM_PARTICLES = 30  # Quantas builds vamos testar simultaneamente
    NUM_ITERATIONS = 50 # Quantas vezes vamos refinar a busca

    print("Iniciando a otimização de build para Lucian com PSO...")
    print(f"Alvo: {TARGET_DUMMY['health']} HP, {TARGET_DUMMY['armor']} Armadura")
    print("-" * 30)

    best_build_indices, best_dps = particle_swarm_optimization(NUM_PARTICLES, NUM_ITERATIONS)

    print("-" * 30)
    print("Otimização Concluída!")
    print(f"\nMelhor DPS encontrado: {best_dps:.2f}")
    print("Melhor Build:")
    
    final_build_names = [ITEM_LIST[i][0] for i in best_build_indices]
    for item_name in final_build_names:
        print(f"- {item_name}")