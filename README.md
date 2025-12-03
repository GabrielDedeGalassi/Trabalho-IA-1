# Trabalho-IA-1

Este projeto realiza a coleta de críticas de filmes do site Adorocinema para classificação de sentimentos (Positivo/Negativo).

## Descrição

O scraper coleta críticas/reviews de filmes do site Adorocinema e as classifica automaticamente como:
- **Positivo**: Críticas/reviews com nota >= 3.5
- **Negativo**: Críticas/reviews com nota < 3.5

## Requisitos

- Python 3.7 ou superior
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Usar

Execute o script principal:

```bash
python scraper.py
```

O script irá:
1. Coletar uma lista de filmes populares do site Adorocinema
2. Acessar cada filme e coletar críticas/reviews dos espectadores
3. Classificar automaticamente cada crítica/review como Positivo ou Negativo
4. Salvar os dados em um arquivo CSV (`dados_criticas.csv`)

## Parâmetros Configuráveis

No arquivo `scraper.py`, você pode ajustar os seguintes parâmetros na função `main()`:

- `max_movies`: Número máximo de filmes a processar (padrão: 200)
- `max_reviews_per_movie`: Número máximo de críticas/reviews por filme (padrão: 20)
- `min_samples_per_class`: Número mínimo de amostras por classe (padrão: 200)

## Estrutura dos Dados

O arquivo CSV gerado contém as seguintes colunas:

- `texto`: Texto completo da crítica
- `label`: Classificação (Positivo ou Negativo)
- `nota`: Nota atribuída pelo espectador (0.0 a 5.0)

## Observações

- Críticas/reviews muito curtas (menos de 50 caracteres) são automaticamente descartadas
- O processo pode levar alguns minutos dependendo do número de filmes processados

## Dados de Exemplo (Alternativa)

Caso o scraping encontre dificuldades (mudanças na estrutura do site), você pode usar o script `gerar_dados_exemplo.py` para criar um dataset simulado:

```bash
python gerar_dados_exemplo.py
```

Este script gera um arquivo `dados_criticas.csv` com 200 amostras de cada classe (Positivo e Negativo), baseado em padrões reais de críticas.

## Próximos Passos

1. Execute o scraper ou o gerador de dados de exemplo
2. Faça upload do arquivo `dados_criticas.csv` para o Google Colab
3. Abra o notebook `notebook_treinamento.ipynb` no Colab
4. Execute todas as células do notebook
5. Preencha o relatório técnico com os resultados obtidos

## Links

- Google Drive: https://drive.google.com/drive/folders/1VPCEzfycox31KVCuF6roEBADyABc7J_E?usp=sharing
- Google Colab: https://colab.research.google.com/drive/1yBQ73Zd6MSkBszm4ZSrsaYzovtoa4hKa?authuser=1#scrollTo=Ahq8gCLHXpMd
- Apresentação do YouTube: https://youtu.be/l7Qo3wqs_cY?si=m7hrVosIGtAEfpUd
