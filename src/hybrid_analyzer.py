"""
Analizador Híbrido: Combina datos de Google Search Console con Scraper en tiempo real
Proporciona insights avanzados combinando métricas reales con posiciones scraped
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from collections import defaultdict


class HybridAnalyzer:
    """
    Combina datos de Google Search Console con scraping en tiempo real
    para análisis SEO avanzado
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def find_keyword_opportunities(
        self,
        sc_data: List[Dict],
        min_impressions: int = 100,
        max_position: float = 20.0,
        min_position: float = 4.0
    ) -> List[Dict]:
        """
        Encuentra keywords de oportunidad en Search Console:
        - Alto volumen de impresiones
        - Posición entre 4-20 (fáciles de mejorar)
        - Bajo CTR (indica potencial de mejora)

        Args:
            sc_data: Datos de Search Console (queries)
            min_impressions: Mínimo de impresiones para considerar
            max_position: Posición máxima (ej: 20)
            min_position: Posición mínima (ej: 4, para excluir top 3)

        Returns:
            Lista de keywords con potencial de mejora
        """
        opportunities = []

        try:
            for row in sc_data:
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0] if isinstance(keys, list) else keys
                impressions = row.get('impressions', 0)
                position = row.get('position', 100)
                clicks = row.get('clicks', 0)
                ctr = row.get('ctr', 0) * 100

                # Filtrar por criterios de oportunidad
                if (impressions >= min_impressions and
                    min_position <= position <= max_position):

                    # Calcular score de oportunidad
                    # Más impresiones + peor posición = mayor oportunidad
                    opportunity_score = (impressions / 100) * (position / 10)

                    # Calcular potencial de clicks (si mejoramos a posición 3)
                    # Posición 3 tiene ~15% CTR promedio
                    expected_ctr_top3 = 15.0
                    potential_clicks = int((impressions * expected_ctr_top3 / 100) - clicks)

                    opportunities.append({
                        'keyword': keyword,
                        'current_position': round(position, 1),
                        'impressions': impressions,
                        'clicks': clicks,
                        'ctr': round(ctr, 2),
                        'opportunity_score': round(opportunity_score, 1),
                        'potential_additional_clicks': max(0, potential_clicks),
                        'priority': self._calculate_priority(position, impressions, ctr)
                    })

            # Ordenar por opportunity_score descendente
            opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)

            self.logger.info(f"Encontradas {len(opportunities)} keywords de oportunidad")
            return opportunities

        except Exception as e:
            self.logger.error(f"Error encontrando oportunidades: {e}")
            return []

    def _calculate_priority(self, position: float, impressions: int, ctr: float) -> str:
        """Calcula prioridad de optimización"""
        if position <= 10 and impressions >= 500:
            return "🔴 Alta"
        elif position <= 15 and impressions >= 200:
            return "🟡 Media"
        else:
            return "🟢 Baja"

    def compare_positions(
        self,
        sc_data: List[Dict],
        scraper_results: List[Dict],
        tolerance: float = 5.0
    ) -> List[Dict]:
        """
        Compara posiciones de Search Console vs Scraper en tiempo real

        Args:
            sc_data: Datos de Search Console
            scraper_results: Resultados del scraper
            tolerance: Diferencia aceptable entre posiciones

        Returns:
            Lista de comparaciones con discrepancias
        """
        comparisons = []

        try:
            # Crear lookup de posiciones del scraper
            scraper_positions = {}
            for result in scraper_results:
                keyword = result.get('keyword', '').lower().strip()
                position = result.get('position', 0)

                if keyword and position:
                    if keyword not in scraper_positions:
                        scraper_positions[keyword] = []
                    scraper_positions[keyword].append(position)

            # Comparar con Search Console
            for row in sc_data:
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0].lower().strip() if isinstance(keys, list) else str(keys).lower().strip()
                sc_position = row.get('position', 0)

                if keyword in scraper_positions:
                    # Usar la mejor posición del scraper (mínima)
                    scraper_pos = min(scraper_positions[keyword])

                    difference = abs(sc_position - scraper_pos)

                    comparisons.append({
                        'keyword': keyword,
                        'sc_position': round(sc_position, 1),
                        'scraper_position': scraper_pos,
                        'difference': round(difference, 1),
                        'status': '✅ Coincide' if difference <= tolerance else '⚠️ Difiere',
                        'impressions': row.get('impressions', 0),
                        'clicks': row.get('clicks', 0)
                    })

            # Ordenar por diferencia descendente
            comparisons.sort(key=lambda x: x['difference'], reverse=True)

            self.logger.info(f"Comparadas {len(comparisons)} keywords")
            return comparisons

        except Exception as e:
            self.logger.error(f"Error comparando posiciones: {e}")
            return []

    def get_recommended_keywords(
        self,
        sc_data: List[Dict],
        current_keywords: List[str],
        limit: int = 50,
        min_impressions: int = 50
    ) -> List[Dict]:
        """
        Recomienda nuevas keywords para scrapear basándose en Search Console

        Args:
            sc_data: Datos de Search Console
            current_keywords: Keywords que ya se están scrapeando
            limit: Máximo de keywords a recomendar
            min_impressions: Mínimo de impresiones para considerar

        Returns:
            Lista de keywords recomendadas con métricas
        """
        recommendations = []
        current_kw_lower = set(kw.lower().strip() for kw in current_keywords)

        try:
            for row in sc_data:
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0] if isinstance(keys, list) else keys
                keyword_lower = keyword.lower().strip()

                # Saltar si ya está en la lista
                if keyword_lower in current_kw_lower:
                    continue

                impressions = row.get('impressions', 0)
                clicks = row.get('clicks', 0)
                position = row.get('position', 100)
                ctr = row.get('ctr', 0) * 100

                # Filtrar por impresiones mínimas
                if impressions < min_impressions:
                    continue

                # Calcular score de recomendación
                # Factores: impresiones, posición, CTR
                recommendation_score = (
                    (impressions / 10) +  # Más impresiones = mejor
                    (1 / (position + 1) * 100) +  # Mejor posición = mejor
                    (ctr * 2)  # Buen CTR = relevante
                )

                recommendations.append({
                    'keyword': keyword,
                    'impressions': impressions,
                    'clicks': clicks,
                    'position': round(position, 1),
                    'ctr': round(ctr, 2),
                    'recommendation_score': round(recommendation_score, 1),
                    'reason': self._get_recommendation_reason(position, impressions, ctr)
                })

            # Ordenar por score y limitar
            recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            recommendations = recommendations[:limit]

            self.logger.info(f"Generadas {len(recommendations)} recomendaciones de keywords")
            return recommendations

        except Exception as e:
            self.logger.error(f"Error generando recomendaciones: {e}")
            return []

    def _get_recommendation_reason(self, position: float, impressions: int, ctr: float) -> str:
        """Genera razón de recomendación"""
        reasons = []

        if impressions >= 500:
            reasons.append("Alto volumen")
        if position <= 10:
            reasons.append("Ya en top 10")
        if position > 10 and impressions >= 200:
            reasons.append("Oportunidad de mejora")
        if ctr >= 5:
            reasons.append("Buen CTR")

        return ", ".join(reasons) if reasons else "Keyword relevante"

    def detect_ranking_drops(
        self,
        historical_data: List[Dict],
        current_positions: List[Dict],
        threshold: float = 5.0
    ) -> List[Dict]:
        """
        Detecta caídas significativas de posiciones

        Args:
            historical_data: Posiciones anteriores (del último scraping)
            current_positions: Posiciones actuales
            threshold: Diferencia mínima para considerar caída

        Returns:
            Lista de keywords con caídas significativas
        """
        drops = []

        try:
            # Crear lookup de posiciones históricas
            historical_positions = {}
            for result in historical_data:
                keyword = result.get('keyword', '').lower().strip()
                position = result.get('position', 0)

                if keyword and position:
                    if keyword not in historical_positions:
                        historical_positions[keyword] = position
                    else:
                        # Usar la mejor posición histórica
                        historical_positions[keyword] = min(historical_positions[keyword], position)

            # Comparar con posiciones actuales
            for result in current_positions:
                keyword = result.get('keyword', '').lower().strip()
                current_pos = result.get('position', 0)

                if keyword in historical_positions:
                    historical_pos = historical_positions[keyword]
                    drop = current_pos - historical_pos

                    if drop >= threshold:
                        drops.append({
                            'keyword': keyword,
                            'previous_position': historical_pos,
                            'current_position': current_pos,
                            'drop': int(drop),
                            'severity': '🔴 Crítica' if drop >= 10 else '🟡 Moderada',
                            'url': result.get('url', ''),
                            'domain': result.get('domain', '')
                        })

            # Ordenar por severidad de caída
            drops.sort(key=lambda x: x['drop'], reverse=True)

            self.logger.info(f"Detectadas {len(drops)} caídas de posiciones")
            return drops

        except Exception as e:
            self.logger.error(f"Error detectando caídas: {e}")
            return []

    def generate_combined_report(
        self,
        sc_data: List[Dict],
        scraper_data: List[Dict],
        opportunities: List[Dict] = None,
        comparisons: List[Dict] = None
    ) -> Dict:
        """
        Genera un reporte combinado con todas las métricas

        Returns:
            Diccionario con estadísticas y análisis combinado
        """
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'search_console': {
                    'total_queries': len(sc_data),
                    'total_impressions': sum(row.get('impressions', 0) for row in sc_data),
                    'total_clicks': sum(row.get('clicks', 0) for row in sc_data),
                    'average_position': round(
                        sum(row.get('position', 0) for row in sc_data) / len(sc_data)
                        if sc_data else 0,
                        2
                    ),
                    'average_ctr': round(
                        sum(row.get('ctr', 0) for row in sc_data) / len(sc_data) * 100
                        if sc_data else 0,
                        2
                    )
                },
                'scraper': {
                    'total_keywords_checked': len(set(r.get('keyword') for r in scraper_data)),
                    'total_results_found': len(scraper_data),
                    'average_position': round(
                        sum(r.get('position', 0) for r in scraper_data) / len(scraper_data)
                        if scraper_data else 0,
                        2
                    ),
                    'top_10_count': len([r for r in scraper_data if r.get('position', 100) <= 10]),
                    'top_3_count': len([r for r in scraper_data if r.get('position', 100) <= 3])
                },
                'opportunities': {
                    'count': len(opportunities) if opportunities else 0,
                    'top_opportunities': opportunities[:10] if opportunities else []
                },
                'position_accuracy': {
                    'comparisons_count': len(comparisons) if comparisons else 0,
                    'matching_count': len([c for c in (comparisons or []) if c.get('status') == '✅ Coincide']),
                    'differing_count': len([c for c in (comparisons or []) if c.get('status') == '⚠️ Difiere'])
                }
            }

            # Calcular porcentaje de coincidencia
            if comparisons and len(comparisons) > 0:
                match_rate = (report['position_accuracy']['matching_count'] / len(comparisons)) * 100
                report['position_accuracy']['match_rate_percentage'] = round(match_rate, 1)

            return report

        except Exception as e:
            self.logger.error(f"Error generando reporte combinado: {e}")
            return {}

    def enrich_scraper_results_with_sc_data(
        self,
        scraper_results: List[Dict],
        sc_data: List[Dict]
    ) -> List[Dict]:
        """
        Enriquece resultados del scraper con datos de Search Console

        Args:
            scraper_results: Resultados del scraper
            sc_data: Datos de Search Console

        Returns:
            Resultados enriquecidos con métricas de SC
        """
        enriched = []

        try:
            # Crear lookup de datos de SC
            sc_lookup = {}
            for row in sc_data:
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0].lower().strip() if isinstance(keys, list) else str(keys).lower().strip()
                sc_lookup[keyword] = {
                    'sc_impressions': row.get('impressions', 0),
                    'sc_clicks': row.get('clicks', 0),
                    'sc_ctr': round(row.get('ctr', 0) * 100, 2),
                    'sc_position': round(row.get('position', 0), 1)
                }

            # Enriquecer resultados del scraper
            for result in scraper_results:
                keyword = result.get('keyword', '').lower().strip()
                enriched_result = result.copy()

                if keyword in sc_lookup:
                    enriched_result.update(sc_lookup[keyword])
                    enriched_result['has_sc_data'] = True
                else:
                    enriched_result['has_sc_data'] = False

                enriched.append(enriched_result)

            self.logger.info(f"Enriquecidos {len(enriched)} resultados con datos de SC")
            return enriched

        except Exception as e:
            self.logger.error(f"Error enriqueciendo resultados: {e}")
            return scraper_results

    def find_missing_content_gaps(
        self,
        sc_queries: List[Dict],
        scraper_results: List[Dict],
        target_domain: str
    ) -> List[Dict]:
        """
        Encuentra gaps de contenido: keywords donde SC tiene tráfico
        pero el scraper no encuentra el dominio objetivo en top posiciones

        Args:
            sc_queries: Queries de Search Console
            scraper_results: Resultados del scraper
            target_domain: Dominio objetivo a analizar

        Returns:
            Lista de keywords con gaps de contenido
        """
        gaps = []

        try:
            # Crear set de keywords donde aparece el dominio objetivo
            keywords_with_domain = set()
            for result in scraper_results:
                keyword = result.get('keyword', '').lower().strip()
                domain = result.get('domain', '').lower()
                position = result.get('position', 100)

                if target_domain.lower() in domain and position <= 20:
                    keywords_with_domain.add(keyword)

            # Buscar keywords de SC que no están en el scraper
            for row in sc_queries:
                keys = row.get('keys', [])
                if not keys:
                    continue

                keyword = keys[0].lower().strip() if isinstance(keys, list) else str(keys).lower().strip()
                impressions = row.get('impressions', 0)
                clicks = row.get('clicks', 0)

                # Si SC tiene tráfico pero no aparecemos en scraper
                if keyword not in keywords_with_domain and (clicks > 0 or impressions >= 50):
                    gaps.append({
                        'keyword': keyword,
                        'sc_impressions': impressions,
                        'sc_clicks': clicks,
                        'sc_ctr': round(row.get('ctr', 0) * 100, 2),
                        'sc_position': round(row.get('position', 0), 1),
                        'gap_type': 'No visible en top 20' if impressions >= 50 else 'Tráfico bajo',
                        'action_needed': 'Crear contenido optimizado' if clicks == 0 else 'Mejorar posición'
                    })

            # Ordenar por impresiones
            gaps.sort(key=lambda x: x['sc_impressions'], reverse=True)

            self.logger.info(f"Encontrados {len(gaps)} gaps de contenido")
            return gaps

        except Exception as e:
            self.logger.error(f"Error encontrando gaps: {e}")
            return []

    def calculate_visibility_score(
        self,
        scraper_results: List[Dict],
        sc_data: List[Dict],
        target_domain: str
    ) -> Dict:
        """
        Calcula un score de visibilidad combinando datos de scraper y SC

        Returns:
            Diccionario con métricas de visibilidad
        """
        try:
            # Métricas del scraper
            domain_results = [
                r for r in scraper_results
                if target_domain.lower() in r.get('domain', '').lower()
            ]

            top_3 = len([r for r in domain_results if r.get('position', 100) <= 3])
            top_10 = len([r for r in domain_results if r.get('position', 100) <= 10])
            top_20 = len([r for r in domain_results if r.get('position', 100) <= 20])

            # Métricas de SC
            total_clicks = sum(row.get('clicks', 0) for row in sc_data)
            total_impressions = sum(row.get('impressions', 0) for row in sc_data)
            avg_sc_position = (
                sum(row.get('position', 0) for row in sc_data) / len(sc_data)
                if sc_data else 0
            )

            # Calcular visibility score (0-100)
            # Ponderación: 40% scraper, 60% Search Console (datos reales)
            scraper_score = (top_3 * 10 + top_10 * 5 + top_20 * 2) / len(scraper_results) * 100 if scraper_results else 0
            sc_score = (total_clicks / (total_impressions + 1)) * 100  # CTR como proxy

            visibility_score = (scraper_score * 0.4) + (sc_score * 0.6)

            return {
                'overall_visibility_score': round(visibility_score, 1),
                'scraper_metrics': {
                    'top_3_positions': top_3,
                    'top_10_positions': top_10,
                    'top_20_positions': top_20,
                    'scraper_score': round(scraper_score, 1)
                },
                'search_console_metrics': {
                    'total_clicks': total_clicks,
                    'total_impressions': total_impressions,
                    'average_position': round(avg_sc_position, 1),
                    'sc_score': round(sc_score, 1)
                },
                'rating': self._get_visibility_rating(visibility_score)
            }

        except Exception as e:
            self.logger.error(f"Error calculando visibility score: {e}")
            return {}

    def _get_visibility_rating(self, score: float) -> str:
        """Convierte score numérico a rating cualitativo"""
        if score >= 80:
            return "🌟 Excelente"
        elif score >= 60:
            return "✅ Buena"
        elif score >= 40:
            return "🟡 Regular"
        elif score >= 20:
            return "🟠 Baja"
        else:
            return "🔴 Muy Baja"
