"""
Generador de Reportes Híbridos
Crea reportes HTML profesionales combinando datos de Search Console y Scraper
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging


class HybridReportGenerator:
    """
    Genera reportes HTML profesionales con datos combinados de SC y Scraper
    """

    def __init__(self, output_dir: str = "data/html_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def generate_html_report(
        self,
        analysis: Dict,
        project_name: str = "Proyecto SEO"
    ) -> str:
        """
        Genera un reporte HTML completo

        Args:
            analysis: Datos del análisis híbrido
            project_name: Nombre del proyecto

        Returns:
            Ruta del archivo HTML generado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hybrid_report_{timestamp}.html"
            filepath = self.output_dir / filename

            html_content = self._build_html(analysis, project_name)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info(f"Reporte HTML generado: {filepath}")
            return str(filepath)

        except Exception as e:
            self.logger.error(f"Error generando reporte HTML: {e}")
            return ""

    def _build_html(self, analysis: Dict, project_name: str) -> str:
        """Construye el HTML completo del reporte"""

        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Híbrido SEO - {project_name}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        {self._build_header(analysis, project_name)}
        {self._build_summary_section(analysis)}
        {self._build_visibility_section(analysis)}
        {self._build_opportunities_section(analysis)}
        {self._build_comparisons_section(analysis)}
        {self._build_gaps_section(analysis)}
        {self._build_recommendations_section(analysis)}
        {self._build_footer()}
    </div>
</body>
</html>
"""
        return html

    def _get_css(self) -> str:
        """CSS moderno para el reporte"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
        }

        .header .date {
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .section {
            padding: 2rem;
            border-bottom: 1px solid #e5e7eb;
        }

        .section:last-child {
            border-bottom: none;
        }

        .section-title {
            font-size: 1.8rem;
            color: #667eea;
            margin-bottom: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }

        .metric-card.success {
            border-left-color: #10b981;
        }

        .metric-card.warning {
            border-left-color: #f59e0b;
        }

        .metric-card.danger {
            border-left-color: #ef4444;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1f2937;
        }

        .metric-subtext {
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: 0.25rem;
        }

        .table-container {
            overflow-x: auto;
            margin-top: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        thead {
            background: #f3f4f6;
        }

        th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #374151;
            border-bottom: 2px solid #e5e7eb;
        }

        td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #f3f4f6;
        }

        tr:hover {
            background: #f9fafb;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .badge-success {
            background: #d1fae5;
            color: #065f46;
        }

        .badge-warning {
            background: #fef3c7;
            color: #92400e;
        }

        .badge-danger {
            background: #fee2e2;
            color: #991b1b;
        }

        .badge-info {
            background: #dbeafe;
            color: #1e40af;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }

        .recommendation-card {
            background: #f9fafb;
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
        }

        .recommendation-priority {
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .recommendation-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 0.5rem;
        }

        .recommendation-details {
            color: #6b7280;
            margin-top: 0.5rem;
        }

        .footer {
            background: #f9fafb;
            padding: 2rem;
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
        }

        .visibility-score {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 2rem;
        }

        .visibility-score-value {
            font-size: 4rem;
            font-weight: 700;
            margin: 1rem 0;
        }

        .visibility-score-rating {
            font-size: 1.5rem;
            opacity: 0.9;
        }

        .empty-state {
            text-align: center;
            padding: 3rem;
            color: #9ca3af;
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        """

    def _build_header(self, analysis: Dict, project_name: str) -> str:
        """Construye el header del reporte"""
        analysis_date = analysis.get('analysis_date', datetime.now().isoformat())
        date_formatted = datetime.fromisoformat(analysis_date).strftime("%d/%m/%Y %H:%M")

        return f"""
        <div class="header">
            <h1>📊 Reporte Híbrido SEO</h1>
            <div class="subtitle">{project_name}</div>
            <div class="date">Generado el {date_formatted}</div>
        </div>
        """

    def _build_summary_section(self, analysis: Dict) -> str:
        """Construye la sección de resumen"""
        combined = analysis.get('combined_report', {})
        sc_data = combined.get('search_console', {})
        scraper_data = combined.get('scraper', {})

        return f"""
        <div class="section">
            <h2 class="section-title">📈 Resumen General</h2>

            <div class="metrics-grid">
                <div class="metric-card success">
                    <div class="metric-label">Total Keywords (SC)</div>
                    <div class="metric-value">{sc_data.get('total_queries', 0):,}</div>
                    <div class="metric-subtext">Search Console</div>
                </div>

                <div class="metric-card info">
                    <div class="metric-label">Total Impresiones</div>
                    <div class="metric-value">{sc_data.get('total_impressions', 0):,}</div>
                </div>

                <div class="metric-card success">
                    <div class="metric-label">Total Clicks</div>
                    <div class="metric-value">{sc_data.get('total_clicks', 0):,}</div>
                </div>

                <div class="metric-card warning">
                    <div class="metric-label">CTR Promedio</div>
                    <div class="metric-value">{sc_data.get('average_ctr', 0):.2f}%</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Posición Promedio (SC)</div>
                    <div class="metric-value">{sc_data.get('average_position', 0):.1f}</div>
                </div>

                <div class="metric-card success">
                    <div class="metric-label">En Top 10 (Scraper)</div>
                    <div class="metric-value">{scraper_data.get('top_10_count', 0)}</div>
                    <div class="metric-subtext">de {scraper_data.get('total_keywords_checked', 0)} keywords</div>
                </div>
            </div>
        </div>
        """

    def _build_visibility_section(self, analysis: Dict) -> str:
        """Construye la sección de visibility score"""
        visibility = analysis.get('visibility_score', {})

        if not visibility:
            return ""

        score = visibility.get('overall_visibility_score', 0)
        rating = visibility.get('rating', 'N/A')

        return f"""
        <div class="section">
            <h2 class="section-title">🎯 Score de Visibilidad</h2>

            <div class="visibility-score">
                <div>Tu Score de Visibilidad</div>
                <div class="visibility-score-value">{score:.1f}</div>
                <div class="visibility-score-rating">{rating}</div>
                <div class="progress-bar" style="max-width: 400px; margin: 1rem auto;">
                    <div class="progress-fill" style="width: {min(score, 100)}%;"></div>
                </div>
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Top 3 Posiciones</div>
                    <div class="metric-value">{visibility.get('scraper_metrics', {}).get('top_3_positions', 0)}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Top 10 Posiciones</div>
                    <div class="metric-value">{visibility.get('scraper_metrics', {}).get('top_10_positions', 0)}</div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Top 20 Posiciones</div>
                    <div class="metric-value">{visibility.get('scraper_metrics', {}).get('top_20_positions', 0)}</div>
                </div>
            </div>
        </div>
        """

    def _build_opportunities_section(self, analysis: Dict) -> str:
        """Construye la sección de oportunidades"""
        opportunities = analysis.get('opportunities', [])[:10]

        if not opportunities:
            return ""

        rows = ""
        for i, opp in enumerate(opportunities, 1):
            priority_class = "danger" if opp.get('priority') == "🔴 Alta" else "warning"
            rows += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{opp.get('keyword', '')}</strong></td>
                <td>{opp.get('current_position', 0):.1f}</td>
                <td>{opp.get('impressions', 0):,}</td>
                <td>{opp.get('clicks', 0)}</td>
                <td>{opp.get('ctr', 0):.2f}%</td>
                <td><span class="badge badge-{priority_class}">{opp.get('priority', '')}</span></td>
                <td><strong>+{opp.get('potential_additional_clicks', 0)}</strong> clicks/mes</td>
            </tr>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">🚀 Oportunidades de Mejora</h2>
            <p style="color: #6b7280; margin-bottom: 1rem;">
                Keywords con alto volumen de impresiones y potencial de mejora en posición
            </p>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Keyword</th>
                            <th>Posición</th>
                            <th>Impresiones</th>
                            <th>Clicks</th>
                            <th>CTR</th>
                            <th>Prioridad</th>
                            <th>Potencial</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def _build_comparisons_section(self, analysis: Dict) -> str:
        """Construye la sección de comparaciones SC vs Scraper"""
        comparisons = analysis.get('position_comparisons', [])[:15]

        if not comparisons:
            return ""

        rows = ""
        for i, comp in enumerate(comparisons, 1):
            status_class = "success" if comp.get('status') == '✅ Coincide' else "warning"
            rows += f"""
            <tr>
                <td>{i}</td>
                <td>{comp.get('keyword', '')}</td>
                <td>{comp.get('sc_position', 0):.1f}</td>
                <td>{comp.get('scraper_position', 0)}</td>
                <td>{comp.get('difference', 0):.1f}</td>
                <td><span class="badge badge-{status_class}">{comp.get('status', '')}</span></td>
                <td>{comp.get('impressions', 0):,}</td>
            </tr>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">🔍 Comparación de Posiciones</h2>
            <p style="color: #6b7280; margin-bottom: 1rem;">
                Comparación entre posiciones de Search Console y resultados del scraper en tiempo real
            </p>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Keyword</th>
                            <th>Pos. SC</th>
                            <th>Pos. Real</th>
                            <th>Diferencia</th>
                            <th>Estado</th>
                            <th>Impresiones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def _build_gaps_section(self, analysis: Dict) -> str:
        """Construye la sección de gaps de contenido"""
        gaps = analysis.get('content_gaps', [])[:10]

        if not gaps:
            return ""

        rows = ""
        for i, gap in enumerate(gaps, 1):
            rows += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{gap.get('keyword', '')}</strong></td>
                <td>{gap.get('sc_position', 0):.1f}</td>
                <td>{gap.get('sc_impressions', 0):,}</td>
                <td>{gap.get('sc_clicks', 0)}</td>
                <td><span class="badge badge-warning">{gap.get('gap_type', '')}</span></td>
                <td>{gap.get('action_needed', '')}</td>
            </tr>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">📝 Gaps de Contenido</h2>
            <p style="color: #6b7280; margin-bottom: 1rem;">
                Keywords con tráfico en Search Console donde no apareces en las primeras posiciones
            </p>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Keyword</th>
                            <th>Posición SC</th>
                            <th>Impresiones</th>
                            <th>Clicks</th>
                            <th>Tipo de Gap</th>
                            <th>Acción Necesaria</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def _build_recommendations_section(self, analysis: Dict) -> str:
        """Construye la sección de recomendaciones"""
        # Por ahora, generar recomendaciones básicas
        opportunities = analysis.get('opportunities', [])
        gaps = analysis.get('content_gaps', [])

        if not opportunities and not gaps:
            return ""

        recommendations_html = ""

        if opportunities:
            top_opps = opportunities[:5]
            recommendations_html += f"""
            <div class="recommendation-card">
                <div class="recommendation-priority">🔴 Prioridad Alta</div>
                <div class="recommendation-title">Optimizar contenido para keywords de alta oportunidad</div>
                <div class="recommendation-details">
                    <p>Enfócate en mejorar las posiciones de estas {len(top_opps)} keywords que ya tienen tráfico:</p>
                    <ul>
                        {"".join([f"<li><strong>{opp['keyword']}</strong> - Posición {opp['current_position']:.1f} → Potencial: +{opp.get('potential_additional_clicks', 0)} clicks/mes</li>" for opp in top_opps])}
                    </ul>
                </div>
            </div>
            """

        if gaps:
            top_gaps = gaps[:5]
            recommendations_html += f"""
            <div class="recommendation-card">
                <div class="recommendation-priority">🟡 Prioridad Media</div>
                <div class="recommendation-title">Crear contenido nuevo para gaps identificados</div>
                <div class="recommendation-details">
                    <p>Estas {len(top_gaps)} keywords tienen tráfico pero no estás bien posicionado:</p>
                    <ul>
                        {"".join([f"<li><strong>{gap['keyword']}</strong> - {gap.get('sc_impressions', 0):,} impresiones mensuales sin capturar</li>" for gap in top_gaps])}
                    </ul>
                </div>
            </div>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">💡 Recomendaciones Accionables</h2>
            {recommendations_html}
        </div>
        """

    def _build_footer(self) -> str:
        """Construye el footer del reporte"""
        return f"""
        <div class="footer">
            <p><strong>Keyword Position Scraper - Hybrid Report</strong></p>
            <p>Generado automáticamente el {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                Este reporte combina datos de Google Search Console con scraping en tiempo real
                para proporcionar insights SEO accionables
            </p>
        </div>
        """
