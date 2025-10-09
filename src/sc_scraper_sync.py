"""
Módulo de Sincronización entre Search Console y Scraper
Facilita la integración automática entre ambas fuentes de datos
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from search_console_api import SearchConsoleAPI
from hybrid_analyzer import HybridAnalyzer
from project_manager import ProjectManager


class SearchConsoleScraperSync:
    """
    Gestiona la sincronización automática entre Search Console y el Scraper
    """

    def __init__(self, project_manager: ProjectManager):
        self.logger = logging.getLogger(__name__)
        self.sc_api = SearchConsoleAPI()
        self.hybrid_analyzer = HybridAnalyzer()
        self.project_manager = project_manager

    def sync_keywords_to_project(
        self,
        project_id: str,
        days: int = 30,
        min_impressions: int = 10,
        auto_add: bool = False
    ) -> Dict:
        """
        Sincroniza keywords de Search Console a un proyecto

        Args:
            project_id: ID del proyecto
            days: Días de datos a obtener
            min_impressions: Mínimo de impresiones para incluir keyword
            auto_add: Si True, añade automáticamente las keywords al proyecto

        Returns:
            Diccionario con estadísticas de sincronización
        """
        try:
            # Obtener proyecto
            project = self.project_manager.get_project(project_id)
            if not project:
                raise ValueError(f"Proyecto {project_id} no encontrado")

            site_url = project.get('search_console_property')
            if not site_url:
                raise ValueError("El proyecto no tiene configurada la URL de Search Console")

            # Verificar autenticación
            if not self.sc_api.is_authenticated():
                raise Exception("No autenticado con Search Console")

            self.logger.info(f"Sincronizando keywords desde Search Console para {site_url}")

            # Obtener datos de Search Console
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            sc_data = self.sc_api.get_search_analytics(
                site_url=site_url,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                dimensions=['query'],
                row_limit=1000
            )

            if not sc_data or 'rows' not in sc_data:
                self.logger.warning("No se obtuvieron datos de Search Console")
                return {
                    'success': False,
                    'message': 'No hay datos disponibles en Search Console'
                }

            # Procesar keywords
            keywords_data = []
            for row in sc_data.get('rows', []):
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0] if isinstance(keys, list) else keys
                impressions = row.get('impressions', 0)
                clicks = row.get('clicks', 0)
                position = row.get('position', 100)

                # Filtrar por impresiones mínimas
                if impressions >= min_impressions:
                    keywords_data.append({
                        'keyword': keyword,
                        'impressions': impressions,
                        'clicks': clicks,
                        'position': round(position, 1),
                        'ctr': round(row.get('ctr', 0) * 100, 2)
                    })

            # Ordenar por impresiones
            keywords_data.sort(key=lambda x: x['impressions'], reverse=True)

            # Obtener keywords actuales del proyecto
            current_keywords = self.project_manager.get_project_keywords(project_id)

            # Identificar nuevas keywords
            new_keywords = []
            existing_kw_lower = set(kw.lower().strip() for kw in current_keywords)

            for kw_data in keywords_data:
                keyword = kw_data['keyword']
                if keyword.lower().strip() not in existing_kw_lower:
                    new_keywords.append(keyword)

            # Auto-añadir si está habilitado
            added_count = 0
            if auto_add and new_keywords:
                added_count = self.project_manager.add_keywords_to_project(
                    project_id,
                    new_keywords
                )

            result = {
                'success': True,
                'total_sc_keywords': len(keywords_data),
                'new_keywords_found': len(new_keywords),
                'keywords_added': added_count,
                'keywords_data': keywords_data[:50],  # Top 50 para preview
                'new_keywords_list': new_keywords[:50],
                'sync_date': datetime.now().isoformat()
            }

            self.logger.info(
                f"Sincronización completada: {len(keywords_data)} keywords de SC, "
                f"{len(new_keywords)} nuevas, {added_count} añadidas"
            )

            return result

        except Exception as e:
            self.logger.error(f"Error sincronizando keywords: {e}")
            return {
                'success': False,
                'message': str(e)
            }

    def get_smart_scraping_list(
        self,
        project_id: str,
        strategy: str = 'opportunities',
        limit: int = 100
    ) -> List[str]:
        """
        Genera una lista inteligente de keywords para scrapear

        Args:
            project_id: ID del proyecto
            strategy: Estrategia de selección:
                - 'opportunities': Keywords con más potencial de mejora
                - 'top_volume': Keywords con más impresiones
                - 'low_hanging': Posiciones 4-10 (fáciles de mejorar)
                - 'all': Todas las keywords del proyecto
            limit: Máximo de keywords a retornar

        Returns:
            Lista de keywords para scrapear
        """
        try:
            project = self.project_manager.get_project(project_id)
            if not project:
                return []

            # Obtener datos de Search Console
            site_url = project.get('search_console_property')
            if not site_url or not self.sc_api.is_authenticated():
                # Fallback: usar keywords del proyecto
                return project.get('keywords', [])[:limit]

            # Obtener datos recientes de SC
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)

            sc_data = self.sc_api.get_search_analytics(
                site_url=site_url,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                dimensions=['query'],
                row_limit=500
            )

            if not sc_data or 'rows' not in sc_data:
                return project.get('keywords', [])[:limit]

            rows = sc_data.get('rows', [])

            # Aplicar estrategia
            if strategy == 'opportunities':
                # Keywords con más potencial
                opportunities = self.hybrid_analyzer.find_keyword_opportunities(
                    sc_data=rows,
                    min_impressions=50,
                    max_position=20.0,
                    min_position=4.0
                )
                return [opp['keyword'] for opp in opportunities[:limit]]

            elif strategy == 'top_volume':
                # Keywords con más impresiones
                sorted_rows = sorted(
                    rows,
                    key=lambda x: x.get('impressions', 0),
                    reverse=True
                )
                keywords = []
                for row in sorted_rows[:limit]:
                    keys = row.get('keys', [])
                    if keys:
                        keyword = keys[0] if isinstance(keys, list) else keys
                        keywords.append(keyword)
                return keywords

            elif strategy == 'low_hanging':
                # Posiciones 4-10 (low-hanging fruit)
                low_hanging = []
                for row in rows:
                    position = row.get('position', 100)
                    if 4 <= position <= 10:
                        keys = row.get('keys', [])
                        if keys:
                            keyword = keys[0] if isinstance(keys, list) else keys
                            low_hanging.append({
                                'keyword': keyword,
                                'position': position,
                                'impressions': row.get('impressions', 0)
                            })

                # Ordenar por impresiones
                low_hanging.sort(key=lambda x: x['impressions'], reverse=True)
                return [item['keyword'] for item in low_hanging[:limit]]

            else:  # 'all'
                keywords = []
                for row in rows[:limit]:
                    keys = row.get('keys', [])
                    if keys:
                        keyword = keys[0] if isinstance(keys, list) else keys
                        keywords.append(keyword)
                return keywords

        except Exception as e:
            self.logger.error(f"Error generando lista de scraping: {e}")
            return []

    def analyze_scraping_session_with_sc(
        self,
        project_id: str,
        scraper_results: List[Dict],
        save_to_project: bool = True
    ) -> Dict:
        """
        Analiza una sesión de scraping comparándola con datos de Search Console

        Args:
            project_id: ID del proyecto
            scraper_results: Resultados del scraper
            save_to_project: Si guardar el análisis en el proyecto

        Returns:
            Análisis completo combinado
        """
        try:
            project = self.project_manager.get_project(project_id)
            if not project:
                return {}

            site_url = project.get('search_console_property')
            target_domain = project.get('domain')

            # Obtener datos de SC si está disponible
            sc_data = []
            if site_url and self.sc_api.is_authenticated():
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=30)

                sc_response = self.sc_api.get_search_analytics(
                    site_url=site_url,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    dimensions=['query'],
                    row_limit=1000
                )

                sc_data = sc_response.get('rows', []) if sc_response else []

            # Realizar análisis híbrido
            analysis = {
                'project_id': project_id,
                'project_name': project.get('name'),
                'analysis_date': datetime.now().isoformat(),
                'scraper_summary': {
                    'total_keywords': len(set(r.get('keyword') for r in scraper_results)),
                    'total_results': len(scraper_results),
                    'average_position': round(
                        sum(r.get('position', 0) for r in scraper_results) / len(scraper_results)
                        if scraper_results else 0,
                        2
                    )
                }
            }

            if sc_data:
                # Enriquecer resultados del scraper
                enriched_results = self.hybrid_analyzer.enrich_scraper_results_with_sc_data(
                    scraper_results,
                    sc_data
                )

                # Encontrar oportunidades
                opportunities = self.hybrid_analyzer.find_keyword_opportunities(
                    sc_data,
                    min_impressions=50
                )

                # Comparar posiciones
                comparisons = self.hybrid_analyzer.compare_positions(
                    sc_data,
                    scraper_results
                )

                # Gaps de contenido
                gaps = self.hybrid_analyzer.find_missing_content_gaps(
                    sc_data,
                    scraper_results,
                    target_domain
                )

                # Visibility score
                visibility = self.hybrid_analyzer.calculate_visibility_score(
                    scraper_results,
                    sc_data,
                    target_domain
                )

                # Reporte combinado
                combined_report = self.hybrid_analyzer.generate_combined_report(
                    sc_data,
                    scraper_results,
                    opportunities,
                    comparisons
                )

                # Agregar al análisis
                analysis.update({
                    'enriched_results': enriched_results[:100],  # Limitar para no saturar
                    'opportunities': opportunities[:20],
                    'position_comparisons': comparisons[:50],
                    'content_gaps': gaps[:30],
                    'visibility_score': visibility,
                    'combined_report': combined_report,
                    'has_sc_data': True
                })
            else:
                analysis['has_sc_data'] = False
                analysis['message'] = 'No hay datos de Search Console disponibles'

            # Guardar en proyecto si se solicita
            if save_to_project:
                self.project_manager.add_report_to_project(
                    project_id,
                    {
                        'type': 'hybrid_analysis',
                        'data': analysis,
                        'created_at': datetime.now().isoformat()
                    }
                )

            return analysis

        except Exception as e:
            self.logger.error(f"Error analizando sesión: {e}")
            return {}

    def get_recommended_actions(
        self,
        project_id: str,
        analysis: Dict = None
    ) -> List[Dict]:
        """
        Genera recomendaciones accionables basadas en el análisis

        Args:
            project_id: ID del proyecto
            analysis: Análisis previo (opcional, se genera si no se proporciona)

        Returns:
            Lista de acciones recomendadas
        """
        recommendations = []

        try:
            if not analysis:
                # Realizar análisis si no se proporciona
                project = self.project_manager.get_project(project_id)
                if not project:
                    return []

                # Este sería un análisis sin sesión de scraping
                # Por ahora retornar recomendaciones básicas
                pass

            # Analizar oportunidades
            if analysis.get('opportunities'):
                top_opps = analysis['opportunities'][:5]
                if top_opps:
                    recommendations.append({
                        'priority': '🔴 Alta',
                        'category': 'Optimización de Contenido',
                        'action': f'Optimizar contenido para {len(top_opps)} keywords de alta oportunidad',
                        'details': [opp['keyword'] for opp in top_opps],
                        'potential_impact': f"+{sum(opp.get('potential_additional_clicks', 0) for opp in top_opps)} clicks/mes estimados"
                    })

            # Analizar gaps
            if analysis.get('content_gaps'):
                top_gaps = analysis['content_gaps'][:5]
                if top_gaps:
                    recommendations.append({
                        'priority': '🟡 Media',
                        'category': 'Creación de Contenido',
                        'action': f'Crear contenido nuevo para {len(top_gaps)} keywords sin cobertura',
                        'details': [gap['keyword'] for gap in top_gaps],
                        'potential_impact': f"{sum(gap.get('sc_impressions', 0) for gap in top_gaps)} impresiones mensuales sin capturar"
                    })

            # Analizar visibilidad
            if analysis.get('visibility_score'):
                score = analysis['visibility_score'].get('overall_visibility_score', 0)
                if score < 60:
                    recommendations.append({
                        'priority': '🟠 Media-Alta',
                        'category': 'Estrategia SEO General',
                        'action': 'Mejorar visibilidad general del sitio',
                        'details': [
                            f"Score actual: {score}/100",
                            "Enfocarse en mejorar posiciones de keywords existentes",
                            "Incrementar cobertura de temas relevantes"
                        ],
                        'potential_impact': 'Mejora general del tráfico orgánico'
                    })

            # Analizar comparaciones
            if analysis.get('position_comparisons'):
                differing = [
                    c for c in analysis['position_comparisons']
                    if c.get('status') == '⚠️ Difiere' and c.get('difference', 0) > 10
                ]

                if differing:
                    recommendations.append({
                        'priority': '🟢 Baja',
                        'category': 'Monitoreo',
                        'action': f'Investigar {len(differing)} discrepancias grandes entre SC y posiciones reales',
                        'details': [f"{c['keyword']}: SC={c['sc_position']}, Real={c['scraper_position']}" for c in differing[:3]],
                        'potential_impact': 'Mejor comprensión del ranking real'
                    })

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generando recomendaciones: {e}")
            return []
