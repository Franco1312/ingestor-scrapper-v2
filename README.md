# ingestor-scrapper

Un proyecto de Scrapy con Clean Architecture (Ports & Adapters) para aprender web scraping desde cero, pero con una estructura escalable y ordenada desde el inicio.

## 📋 Descripción

Este proyecto implementa un scaffold mínimo pero funcional de Scrapy siguiendo los principios de Clean Architecture (Hexagonal Architecture). La estructura está diseñada para crecer sin necesidad de reestructurar todo el proyecto cuando se agreguen nuevas funcionalidades.

## 🏗️ Arquitectura

El proyecto está organizado en capas siguiendo Clean Architecture:

```
ingestor_scrapper/
├─ core/                    # Dominio (framework-agnóstico)
│  ├─ entities.py          # Modelos del dominio (Item, Page)
│  └─ ports.py             # Interfaces (HtmlFetcher, Parser, OutputPort)
│
├─ application/            # Casos de uso (orquestan puertos)
│  └─ scrape_this_site_use_case.py  # ScrapeThisSiteUseCase
│
├─ adapters/               # Implementaciones (dependientes de frameworks)
│  ├─ fetcher_scrapy.py    # Adapter de HtmlFetcher usando Scrapy
│  ├─ parser_scrapethissite.py  # Parser específico para scrapethissite.com
│  └─ output_stdout.py     # OutputPort que imprime/loguea
│
└─ interface/              # Entrada/Delivery (spiders, CLI)
   └─ spiders/
      └─ scrapethissite_spider.py  # Spider para scrapethissite.com
```

### Patrón Puertos y Adaptadores

- **Puertos (Ports)**: Interfaces/Protocolos definidos en `core/ports.py` que representan contratos abstractos.
- **Adaptadores (Adapters)**: Implementaciones concretas en `adapters/` que implementan esos puertos usando frameworks específicos (Scrapy, BeautifulSoup, etc.).

Esto permite que la lógica de negocio (`application/`) permanezca independiente de frameworks externos.

## 🚀 Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Uso

### Ejecutar el spider de scrapethissite

```bash
scrapy crawl scrapethissite
```

Este comando ejecutará el `scrapethissite_spider` que extrae los links de sesiones de `https://www.scrapethissite.com/pages/` con sus descripciones.

### Crear un nuevo spider

Puedes usar el comando de Scrapy para generar un nuevo spider:

```bash
scrapy genspider mi_spider example.com
```

Luego edita el spider generado en `ingestor_scrapper/interface/spiders/mi_spider.py` para seguir el patrón de Clean Architecture:

```python
from ingestor_scrapper.application.scrape_this_site_use_case import ScrapeThisSiteUseCase
from ingestor_scrapper.adapters.fetcher_scrapy import AdapterScrapyFetcher
from ingestor_scrapper.adapters.parser_scrapethissite import AdapterScrapeThisSiteParser
from ingestor_scrapper.adapters.output_stdout import AdapterStdoutOutput

class MiSpider(scrapy.Spider):
    name = "mi_spider"
    start_urls = ["https://www.scrapethissite.com/pages/"]
    
    def parse(self, response):
        # Wire dependencies
        fetcher = AdapterScrapyFetcher(response)
        parser = AdapterScrapeThisSiteParser()
        output = AdapterStdoutOutput()
        
        # Create and execute use case
        use_case = ScrapeThisSiteUseCase(fetcher, parser, output)
        items = use_case.execute(response.url)
```

## 📦 Estructura del Proyecto

- **`core/`**: Capa de dominio con entidades y puertos (interfaces). Framework-agnóstico.
- **`application/`**: Casos de uso que orquestan los puertos para cumplir requisitos de negocio.
- **`adapters/`**: Implementaciones concretas de los puertos usando frameworks externos (Scrapy, BeautifulSoup, etc.).
- **`interface/`**: Puntos de entrada (spiders de Scrapy, futuros CLI, APIs, etc.).

## 🗺️ Roadmap

### Próximos pasos sugeridos:

1. **Parser por proveedor**: Se usa parser específico por sitio web
   - `AdapterScrapeThisSiteParser`: Parser específico para scrapethissite.com
   - Agregar nuevos parsers por sitio según sea necesario (cada sitio tiene su parser)

2. **Pipelines de Scrapy**: Activar pipelines para procesamiento de items
   - Descomentar sección de pipelines en `settings.py`
   - Crear pipelines para validación, limpieza, almacenamiento

3. **Storage**: Agregar adaptadores de salida a archivos/base de datos
   - `AdapterFileOutput` para guardar en JSON/CSV
   - `AdapterDatabaseOutput` para persistir en DB

4. **Configuración avanzada**: Ajustar settings de Scrapy
   - Rate limiting, delays, concurrent requests
   - Middlewares personalizados

5. **Tests**: Agregar tests unitarios para cada capa
   - Tests de use cases
   - Tests de adaptadores (mocks)
   - Tests de integración

## 📝 Notas

- El parser específico (`AdapterScrapeThisSiteParser`) está optimizado para la estructura de scrapethissite.com.
- El proyecto sigue el patrón de **parser por proveedor/sitio** para máxima flexibilidad.
- Para scrapear un nuevo sitio, crear un nuevo parser específico que implemente el port `Parser`.
- Todos los archivos incluyen **TODOs** donde se puede expandir la funcionalidad.

## 📚 Referencias

- [Scrapy Documentation](https://docs.scrapy.org/)
- [Clean Architecture (Hexagonal Architecture)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports & Adapters Pattern](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
