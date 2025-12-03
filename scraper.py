"""
Scraper para coletar críticas de filmes do site Adorocinema
Classificação: Positivo (nota >= 3.5) ou Negativo (nota < 3.5)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin
import re

class AdorocinemaScraper:
    def __init__(self):
        self.base_url = "https://www.adorocinema.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.reviews = []
        
    def get_movie_list(self, max_pages=20):
        """Coleta lista de filmes da página de filmes em cartaz com paginação"""
        movies = []
        seen_urls = set()  # Evita doubles
        
        # URL base com paginação
        base_url = f"{self.base_url}/filmes/numero-cinemas/"
        
        # Itera pelas páginas começando da página 1
        for page_num in range(1, max_pages + 1):
            try:
                # Constrói URL da página
                if page_num == 1:
                    # Página 1 pode ser sem o ?page=1 ou com o ?page=1
                    page_url = base_url
                else: page_url = f"{base_url}?page={page_num}"
                
                print(f"Coletando página {page_num}: {page_url}")
                response = requests.get(page_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Procura por todos os links na página
                all_links = soup.find_all('a', href=True)
                
                page_movies = []
                
                for link in all_links:
                    href = link.get('href', '')
                    link_text = link.get_text(strip=True)
                    
                    # Procura por links que contenham /filmes/ e sejam URLs de filmes específicos
                    if '/filmes/' in href:
                        # Remove query strings e fragments
                        href_clean = href.split('?')[0].split('#')[0]
                        
                        # Lista de padrões que indicam páginas de listagem (não filmes individuais)
                        exclude_patterns = [
                            '/filmes/numero-cinemas',
                            '/filmes/em-cartaz',
                            '/filmes/melhores',
                            '/filmes/notas',
                            '/filmes/estreias',
                            '/filmes/todos',
                            '/filmes/bilheterias',
                            '/filmes/agenda',
                            '/filmes/programacao',
                            '/filmes/filmes',  # Evita /filmes/filmes/...
                        ]
                        
                        # Verifica se não é uma página de listagem
                        is_listing_page = any(pattern in href_clean for pattern in exclude_patterns)
                        
                        if not is_listing_page:
                            # Constrói URL completa
                            if href_clean.startswith('/'): full_url = urljoin(self.base_url, href_clean)
                            elif href_clean.startswith('http'): full_url = href_clean
                            else: continue
                            
                            # Garante que é uma URL válida de filme
                            if full_url.startswith('http') and '/filmes/' in full_url:
                                # Verifica se parece ser uma URL de filme específico
                                parts = full_url.split('/filmes/')
                                if len(parts) > 1:
                                    movie_part = parts[1].split('/')[0]
                                    
                                    # Se tem algo após /filmes/ que não é outra listagem
                                    if movie_part and len(movie_part) > 2:
                                        # Verifica se não é uma página de listagem conhecida
                                        listing_keywords = [
                                            'numero-cinemas', 'em-cartaz', 'melhores', 'notas', 
                                            'estreias', 'todos', 'bilheterias', 'agenda', 
                                            'programacao', 'filmes', 'trailer', 'noticias'
                                        ]
                                        
                                        if movie_part not in listing_keywords:
                                            # Verifica se o link parece ser de um filme específico
                                            if full_url not in seen_urls:
                                                seen_urls.add(full_url)
                                                page_movies.append(full_url)

                                                # Mostra primeiros 3 para debug
                                                if len(page_movies) <= 3:  print(f"    Filme encontrado: {full_url}")
                
                movies.extend(page_movies)
                print(f"  Página {page_num}: {len(page_movies)} filmes encontrados")
                
                # Se não encontrou filmes nesta página, pode ter chegado ao fim
                if len(page_movies) == 0 and page_num > 1:
                    print(f"  Nenhum filme encontrado na página {page_num}. Parando a coleta.")
                    break
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Erro ao coletar página {page_num}: {e}")
                continue
        
        print(f"\nTotal de filmes únicos coletados: {len(movies)}")
        return list(set(movies))  # Remove doubles
    
    def extract_reviews(self, movie_url, max_reviews=20):
        # Extrai críticas/reviews de um filme específico
        try:
            # Tenta diferentes formatos de URL para críticas
            possible_urls = [
                movie_url.replace('.html', '/criticas-espectadores/'),
                movie_url + '/criticas-espectadores/',
                movie_url.replace('/filmes/', '/filmes/criticas-espectadores/'),
            ]
            
            reviews_found = False
            
            for reviews_url in possible_urls:
                try:
                    response = requests.get(reviews_url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Tenta diferentes seletores para encontrar críticas/reviews
                        review_elements = []
                        
                        # Estratégia 1: classe específica
                        review_elements = soup.find_all('div', class_='review-card')
                        
                        # Estratégia 2: se não encontrou, tenta outros seletores
                        if not review_elements: review_elements = soup.find_all('div', class_=lambda x: x and 'review' in x.lower())
                        
                        # Estratégia 3: busca por elementos com nota
                        if not review_elements: review_elements = soup.find_all('div', class_=lambda x: x and 'note' in x.lower())
                        
                        if review_elements:
                            reviews_found = True
                            
                            for review_elem in review_elements[:max_reviews]:
                                try:
                                    # Extrai a nota - tenta diferentes seletores
                                    rating = None
                                    rating_elem = None
                                    
                                    # Tenta diferentes seletores para nota
                                    for selector in ['span.stareval-note', 'span.note', 'div.note', '.rating']:
                                        rating_elem = review_elem.select_one(selector)
                                        if rating_elem: break
                                    
                                    if rating_elem:
                                        rating_text = rating_elem.get_text(strip=True)
                                        # Remove caracteres não numéricos exceto vírgula/ponto
                                        rating_text = re.sub(r'[^\d,.]', '', rating_text)
                                        rating_text = rating_text.replace(',', '.')

                                        try: rating = float(rating_text)
                                        except: continue
                                    else: continue
                                    
                                    # Extrai o texto da crítica - tenta diferentes seletores
                                    review_text = None
                                    for selector in ['div.content-txt', 'div.review-text', 'p.review-content', '.review-content']:
                                        text_elem = review_elem.select_one(selector)
                                        if text_elem:
                                            review_text = text_elem.get_text(strip=True)
                                            break
                                    
                                    # Se não encontrou com seletores, pega todo o texto
                                    if not review_text: review_text = review_elem.get_text(strip=True)
                                    
                                    # Remove críticas muito curtas
                                    if not review_text or len(review_text) < 50: continue
                                    
                                    # Classifica como Positivo ou Negativo
                                    label = "Positivo" if rating >= 3.5 else "Negativo"
                                    
                                    self.reviews.append({
                                        'texto': review_text,
                                        'nota': rating,
                                        'label': label,
                                        'url_filme': movie_url
                                    })
                                    
                                except Exception as e: continue
                            
                            break  # Se encontrou críticas/reviews, para de tentar outras URLs
                            
                except Exception as e: continue
            
            if not reviews_found: print(f"  Nenhuma review encontrada para {movie_url}")
            
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"  Erro ao acessar {movie_url}: {e}")
    
    def scrape(self, max_movies=50, max_reviews_per_movie=20, min_samples_per_class=200):
        # Executa o scraping completo
        print("Iniciando coleta de filmes...")
        movies = self.get_movie_list(max_pages=20)
        
        print(f"\nTotal de filmes encontrados: {len(movies)}")
        
        if len(movies) == 0:
            print("\nAVISO: Nenhum filme encontrado. O site pode ter mudado sua estrutura.")
            print("Recomendação: Use o script gerar_dados_exemplo.py para criar dados de exemplo.")
            return []
        
        print("Iniciando coleta de reviews...\n")
        
        for i, movie_url in enumerate(movies[:max_movies], 1):
            print(f"Processando filme {i}/{min(max_movies, len(movies))}: {movie_url[:80]}...")
            self.extract_reviews(movie_url, max_reviews_per_movie)
            
            # Para verificar já tem amostras o suficiente
            positive_count = sum(1 for r in self.reviews if r['label'] == 'Positivo')
            negative_count = sum(1 for r in self.reviews if r['label'] == 'Negativo')
            
            print(f"Reviews coletadas: {len(self.reviews)} (Positivo: {positive_count}, Negativo: {negative_count})")
            
            if positive_count >= min_samples_per_class and negative_count >= min_samples_per_class:
                print("\nNúmero mínimo de amostras por classe atingido!")
                break
        
        return self.reviews
    
    def save_to_csv(self, filename='dados_criticas.csv'):
        # Salva os dados coletados em um arquivo CSV
        if not self.reviews:
            print("Nenhuma review coletada!")
            return
        
        df = pd.DataFrame(self.reviews)
        df = df[['texto', 'label', 'nota']] 
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nDados salvos em {filename}")
        print(f"Total de reviews: {len(df)}")
        print(f"Distribuição por classe:")
        print(df['label'].value_counts())


def main():
    scraper = AdorocinemaScraper()
    reviews = scraper.scrape(
        max_movies=200,
        max_reviews_per_movie=20,
        min_samples_per_class=200
    )
    scraper.save_to_csv('dados_criticas.csv')


if __name__ == "__main__": main()
