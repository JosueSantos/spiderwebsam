# Spider Web
#### Desenvolvido por [Josué.Santos](https://josuesantos.github.io/)

---
> Raspagem de informações das matérias do Diário do Nordeste
>
> Endereços podem ser informados pelo arquivo **urls.csv**
>
> **O arquivo csv deve possuir cabeçalho**
>
> Clicando no ATUALIZAR_DADOS_DIARIO_DO_NORDESTE.py
>
> Após o carregamento, as informações estarão no arquivo **dados.csv**


## Raspador Web em Python

##### Utiliza o Scrapy
![](https://scrapy.org/favicons/apple-touch-icon-180x180.png)

Os comandos abaixo podem ser executados:

* scrapy runspider spider_web/spiders/diario_nordeste.py
> Raspagem de informações das materias do Diario do Nordeste
>
> Endereços podem ser informados pelo arquivo **urls.csv**
>
> **O arquivo csv deve possuir cabeçalho**
>
> Clicando no ATUALIZAR_DADOS_DIARIO_DO_NORDESTE.py
>
> Após o carregamento, as informações estarão no arquivo **dados.csv**

* scrapy runspider spider_web/spiders/placardefutebol.py
> Raspagem de informações sobre os jogos de todo o mundo de ontem, hoje e amanhã
>
> Após o carregamento, as informações estarão no arquivo **dados.csv**

* scrapy runspider spider_web/spiders/rede_globo.py
> Raspagem de informações sobre a programação da Rede Globo / Verdes Mares
>
> Após o carregamento, as informações estarão no arquivo **dados.csv**
