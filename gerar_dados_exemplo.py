# Script auxiliar para gerar dados de exemplo caso o scraping precise dê problema ou requer ajustes.

import pandas as pd
import random

# Exemplos de críticas positivas (nota >= 3.5)
criticas_positivas = [
    "Excelente filme! A atuação dos atores foi impecável e a história muito envolvente.",
    "Adorei este filme. Os efeitos especiais são incríveis e a narrativa prende do início ao fim.",
    "Um dos melhores filmes que já vi. Recomendo muito, vale cada minuto.",
    "História emocionante e bem desenvolvida. Os personagens são muito carismáticos.",
    "Fotografia linda e roteiro inteligente. Este filme superou minhas expectativas.",
    "Maravilhoso! A direção está perfeita e o elenco está impecável.",
    "Um filme que te faz refletir. A mensagem é poderosa e bem transmitida.",
    "Excelente produção. Os cenários são deslumbrantes e a trilha sonora é perfeita.",
    "Muito bom! A comédia funciona bem e os diálogos são engraçados.",
    "Um clássico moderno. Este filme vai ficar na memória por muito tempo.",
    "Atuações brilhantes e roteiro bem escrito. Um dos melhores do ano.",
    "Filme incrível! A ação é empolgante e os efeitos são de primeira qualidade.",
    "História cativante do início ao fim. Não consegui parar de assistir.",
    "Excelente trabalho de toda a equipe. Este filme merece todos os elogios.",
    "Muito bem feito! A edição está perfeita e o ritmo é excelente.",
    "Um filme que emociona e diverte ao mesmo tempo. Recomendo para todos.",
    "Produção de altíssima qualidade. Os detalhes são impressionantes.",
    "Roteiro inteligente e bem estruturado. Um filme que prende a atenção.",
    "Excelente elenco e direção impecável. Um dos melhores que já vi.",
    "Filme fantástico! A fotografia é linda e a história é envolvente.",
]

# Exemplos de críticas negativas (nota < 3.5)
criticas_negativas = [
    "Filme muito fraco. A história é confusa e os personagens pouco desenvolvidos.",
    "Não gostei. O roteiro é previsível e a atuação deixa a desejar.",
    "Esperava mais deste filme. A trama é fraca e os diálogos são ruins.",
    "Muito chato e arrastado. Não consegui terminar de assistir.",
    "Efeitos especiais ruins e história sem sentido. Uma decepção total.",
    "Filme ruim. A direção é fraca e o elenco não convence.",
    "História mal desenvolvida e personagens sem profundidade. Não recomendo.",
    "Muito longo e entediante. O filme poderia ter sido muito mais curto.",
    "Roteiro confuso e mal escrito. Uma grande decepção.",
    "Não vale a pena assistir. O filme é fraco em todos os aspectos.",
    "Atuações ruins e história sem graça. Uma perda de tempo.",
    "Filme muito ruim. Os efeitos são péssimos e a história não faz sentido.",
    "Muito decepcionante. Esperava muito mais deste filme.",
    "História previsível e sem originalidade. Não recomendo.",
    "Filme fraco em todos os aspectos. Uma grande decepção.",
    "Roteiro mal desenvolvido e personagens pouco interessantes.",
    "Não gostei nada. O filme é chato e sem emoção.",
    "Muito ruim. A direção é fraca e o elenco não convence.",
    "História confusa e mal contada. Uma perda de tempo.",
    "Filme decepcionante. Não vale a pena assistir.",
]

def gerar_criticas_variadas(base_criticas, quantidade):
    # Gera variações das críticas base para aumentar o dataset
    criticas = []
    for _ in range(quantidade):
        critica_base = random.choice(base_criticas)

        # Adiciona pequenas variações
        variacoes = [
            critica_base,
            critica_base + " Realmente impressionante!",
            critica_base + " Vale muito a pena assistir.",
            critica_base + " Um filme que não decepciona.",
            critica_base + " Super recomendo!",
            critica_base + " Excelente trabalho!",
            critica_base + " Muito bem feito.",
            critica_base + " Um dos melhores.",
            critica_base + " Simplesmente incrível!",
            critica_base + " Não perca!",
        ]
        criticas.append(random.choice(variacoes))
    return criticas

def criar_dataset_exemplo(num_positivas=200, num_negativas=200):
    """Cria um dataset de exemplo com críticas simuladas"""
    
    # Gerar críticas positivas
    criticas_pos = gerar_criticas_variadas(criticas_positivas, num_positivas)
    
    # Gerar críticas negativas
    criticas_neg = gerar_criticas_variadas(criticas_negativas, num_negativas)
    
    # Criar DataFrame
    dados = []
    
    for critica in criticas_pos:
        # Nota entre 3.5 e 5.0
        nota = round(random.uniform(3.5, 5.0), 1)
        dados.append({
            'texto': critica,
            'label': 'Positivo',
            'nota': nota
        })
    
    for critica in criticas_neg:
        # Nota entre 0.0 e 3.4
        nota = round(random.uniform(0.0, 3.4), 1)
        dados.append({
            'texto': critica,
            'label': 'Negativo',
            'nota': nota
        })
    
    # Embaralhar os dados
    random.shuffle(dados)
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    return df

if __name__ == "__main__":
    print("Gerando dataset de exemplo...")
    df = criar_dataset_exemplo(num_positivas=200, num_negativas=200)
    
    # Salvar em CSV
    df.to_csv('dados_criticas.csv', index=False, encoding='utf-8')
    
    print(f"\nDataset gerado com sucesso!")
    print(f"Total de amostras: {len(df)}")
    print(f"\nDistribuição por classe:")
    print(df['label'].value_counts())
    print(f"\nPrimeiras linhas:")
    print(df.head())
