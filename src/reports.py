#!/usr/bin/env python3
"""
📊 Sistema de Reportes Avanzado para Keyword Position Scraper
🚀 Generación de informes detallados con almacenamiento JSON

Características:
• 📈 Análisis de posiciones y tendencias
• 💾 Almacenamiento automático en JSON
• 📋 Reportes HTML y PDF
• 🎯 Métricas de rendimiento SEO
• 📊 Visualizaciones interactivas
"""

import json
import os
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import uuid
from collections import defaultdict, Counter
import numpy as np

class ReportManager:
    def __init__(self, data_dir: str = "data", reports_dir: str = "reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        
        # Crear directorios necesarios
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        (self.reports_dir / "json").mkdir(exist_ok=True)
        (self.reports_dir / "html").mkdir(exist_ok=True)
        (self.reports_dir / "images").mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        
        # Configurar matplotlib para mejor visualización
        plt.style.use('dark_background')
        sns.set_palette("husl")

    def save_scraping_session(self, results: List[Dict], session_info: Dict, project_id: str = None) -> str:
        """
        Guarda una sesión completa de scraping con metadatos

        Args:
            results: Lista de resultados del scraping
            session_info: Información de la sesión (keywords, dominio, etc.)
            project_id: ID del proyecto (opcional)

        Returns:
            str: ID único de la sesión guardada
        """
        session_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()

        session_data = {
            "session_id": session_id,
            "timestamp": timestamp,
            "project_id": project_id,
            "session_info": session_info,
            "results": results,
            "total_keywords": len(set([r.get('keyword', '') for r in results])),
            "total_results": len(results),
            "domains_found": list(set([r.get('domain', '') for r in results if r.get('domain')])),
            "average_position": self._calculate_average_position(results),
            "top_10_count": len([r for r in results if r.get('position', 999) <= 10]),
            "top_3_count": len([r for r in results if r.get('position', 999) <= 3])
        }

        # Determinar carpeta de guardado
        if project_id:
            json_dir = self.reports_dir.parent / "projects" / project_id / "reports" / "json"
            json_dir.mkdir(parents=True, exist_ok=True)
        else:
            json_dir = self.reports_dir / "json"

        # Guardar archivo JSON
        filename = f"session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = json_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"✅ Sesión guardada: {filename} (proyecto: {project_id or 'general'})")
        return session_id

    def load_session(self, session_id: str) -> Optional[Dict]:
        """Carga una sesión específica por ID"""
        json_files = list((self.reports_dir / "json").glob(f"session_{session_id}*.json"))
        
        if not json_files:
            return None
            
        with open(json_files[0], 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_sessions(self) -> List[Dict]:
        """Obtiene información de todas las sesiones guardadas"""
        sessions = []
        json_files = list((self.reports_dir / "json").glob("session_*.json"))
        
        for file_path in sorted(json_files, key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "session_id": data.get("session_id"),
                        "timestamp": data.get("timestamp"),
                        "filename": file_path.name,
                        "total_keywords": data.get("total_keywords", 0),
                        "total_results": data.get("total_results", 0),
                        "average_position": data.get("average_position", 0),
                        "top_10_count": data.get("top_10_count", 0),
                        "domains_found": len(data.get("domains_found", [])),
                        "target_domain": data.get("session_info", {}).get("target_domain", "N/A")
                    })
            except Exception as e:
                self.logger.error(f"Error cargando sesión {file_path}: {e}")
                
        return sessions

    def generate_detailed_report(self, session_id: str) -> Dict:
        """
        Genera un reporte detallado de una sesión específica
        
        Args:
            session_id: ID de la sesión a analizar
            
        Returns:
            Dict: Reporte completo con análisis y métricas
        """
        session_data = self.load_session(session_id)
        if not session_data:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        results = session_data["results"]
        df = pd.DataFrame(results)
        
        if df.empty:
            return {"error": "No hay datos para analizar"}
        
        # Análisis básico
        report = {
            "session_info": session_data["session_info"],
            "timestamp": session_data["timestamp"],
            "summary": self._generate_summary_stats(df),
            "keyword_analysis": self._analyze_keywords(df),
            "position_analysis": self._analyze_positions(df),
            "domain_analysis": self._analyze_domains(df),
            "competitive_analysis": self._analyze_competition(df),
            "recommendations": self._generate_recommendations(df)
        }
        
        # Generar visualizaciones
        charts_info = self._generate_charts(df, session_id)
        report["charts"] = charts_info
        
        return report

    def _calculate_average_position(self, results: List[Dict]) -> float:
        """Calcula la posición promedio de los resultados"""
        positions = [r.get('position') for r in results if r.get('position') is not None]
        return sum(positions) / len(positions) if positions else 0

    def _generate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Genera estadísticas resumen"""
        return {
            "total_keywords": df['keyword'].nunique() if 'keyword' in df.columns else 0,
            "total_results": len(df),
            "unique_domains": df['domain'].nunique() if 'domain' in df.columns else 0,
            "avg_position": df['position'].mean() if 'position' in df.columns else 0,
            "median_position": df['position'].median() if 'position' in df.columns else 0,
            "top_3_results": len(df[df['position'] <= 3]) if 'position' in df.columns else 0,
            "top_10_results": len(df[df['position'] <= 10]) if 'position' in df.columns else 0,
            "page_1_results": len(df[df['position'] <= 10]) if 'position' in df.columns else 0,
            "page_2_results": len(df[(df['position'] > 10) & (df['position'] <= 20)]) if 'position' in df.columns else 0,
            "beyond_page_2": len(df[df['position'] > 20]) if 'position' in df.columns else 0
        }

    def _analyze_keywords(self, df: pd.DataFrame) -> Dict:
        """Analiza las keywords y su rendimiento"""
        if 'keyword' not in df.columns:
            return {}
            
        keyword_stats = df.groupby('keyword').agg({
            'position': ['count', 'mean', 'min'],
            'domain': 'nunique'
        }).round(2)
        
        keyword_stats.columns = ['total_results', 'avg_position', 'best_position', 'unique_domains']
        
        return {
            "top_performing_keywords": keyword_stats.nsmallest(10, 'avg_position').to_dict('index'),
            "most_competitive_keywords": keyword_stats.nlargest(10, 'unique_domains').to_dict('index'),
            "keyword_difficulty_distribution": self._calculate_keyword_difficulty(df),
            "long_tail_vs_short_tail": self._analyze_keyword_length(df)
        }

    def _analyze_positions(self, df: pd.DataFrame) -> Dict:
        """Analiza la distribución de posiciones"""
        if 'position' not in df.columns:
            return {}
            
        position_ranges = {
            "top_3": len(df[df['position'] <= 3]),
            "positions_4_10": len(df[(df['position'] >= 4) & (df['position'] <= 10)]),
            "positions_11_20": len(df[(df['position'] >= 11) & (df['position'] <= 20)]),
            "positions_21_50": len(df[(df['position'] >= 21) & (df['position'] <= 50)]),
            "beyond_50": len(df[df['position'] > 50])
        }
        
        return {
            "position_distribution": position_ranges,
            "position_percentiles": {
                "25th": df['position'].quantile(0.25),
                "50th": df['position'].quantile(0.50),
                "75th": df['position'].quantile(0.75),
                "90th": df['position'].quantile(0.90)
            }
        }

    def _analyze_domains(self, df: pd.DataFrame) -> Dict:
        """Analiza los dominios encontrados"""
        if 'domain' not in df.columns:
            return {}
            
        domain_stats = df.groupby('domain').agg({
            'position': ['count', 'mean', 'min'],
            'keyword': 'nunique'
        }).round(2)
        
        domain_stats.columns = ['total_appearances', 'avg_position', 'best_position', 'unique_keywords']
        
        return {
            "top_domains": domain_stats.nlargest(15, 'total_appearances').to_dict('index'),
            "best_positioned_domains": domain_stats.nsmallest(10, 'avg_position').to_dict('index'),
            "domain_market_share": self._calculate_market_share(df)
        }

    def _analyze_competition(self, df: pd.DataFrame) -> Dict:
        """Analiza la competencia por keyword"""
        if not all(col in df.columns for col in ['keyword', 'domain', 'position']):
            return {}
            
        competition_analysis = {}
        
        for keyword in df['keyword'].unique():
            keyword_data = df[df['keyword'] == keyword]
            competition_analysis[keyword] = {
                "total_competitors": len(keyword_data),
                "top_3_domains": keyword_data.nsmallest(3, 'position')['domain'].tolist(),
                "avg_competition_position": keyword_data['position'].mean(),
                "position_gap": keyword_data['position'].max() - keyword_data['position'].min()
            }
        
        return competition_analysis

    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        if 'position' in df.columns:
            avg_position = df['position'].mean()
            
            if avg_position > 20:
                recommendations.append("🎯 Enfócate en mejorar el contenido y SEO on-page para las keywords principales")
                recommendations.append("🔗 Considera una estrategia de link building más agresiva")
            elif avg_position > 10:
                recommendations.append("📈 Estás cerca de la primera página, optimiza títulos y meta descripciones")
                recommendations.append("🎨 Mejora la experiencia de usuario y velocidad de carga")
            else:
                recommendations.append("🏆 ¡Excelente posicionamiento! Mantén y expande tu estrategia actual")
        
        if 'keyword' in df.columns:
            keyword_count = df['keyword'].nunique()
            if keyword_count < 10:
                recommendations.append("📝 Considera expandir tu lista de keywords objetivo")
            
        return recommendations

    def _calculate_keyword_difficulty(self, df: pd.DataFrame) -> Dict:
        """Calcula la dificultad estimada de las keywords"""
        if not all(col in df.columns for col in ['keyword', 'domain']):
            return {}
            
        difficulty_dist = {}
        
        for keyword in df['keyword'].unique():
            keyword_data = df[df['keyword'] == keyword]
            competitor_count = len(keyword_data)
            
            if competitor_count <= 5:
                difficulty = "Baja"
            elif competitor_count <= 15:
                difficulty = "Media"
            else:
                difficulty = "Alta"
                
            difficulty_dist[difficulty] = difficulty_dist.get(difficulty, 0) + 1
        
        return difficulty_dist

    def _analyze_keyword_length(self, df: pd.DataFrame) -> Dict:
        """Analiza la longitud de las keywords (long tail vs short tail)"""
        if 'keyword' not in df.columns:
            return {}
            
        keyword_lengths = df['keyword'].str.split().str.len()
        
        return {
            "short_tail_1_2_words": len(keyword_lengths[keyword_lengths <= 2]),
            "medium_tail_3_4_words": len(keyword_lengths[(keyword_lengths >= 3) & (keyword_lengths <= 4)]),
            "long_tail_5_plus_words": len(keyword_lengths[keyword_lengths >= 5]),
            "average_length": keyword_lengths.mean()
        }

    def _calculate_market_share(self, df: pd.DataFrame) -> Dict:
        """Calcula la cuota de mercado por dominio"""
        if 'domain' not in df.columns:
            return {}
            
        total_results = len(df)
        domain_counts = df['domain'].value_counts()
        
        market_share = {}
        for domain, count in domain_counts.head(10).items():
            market_share[domain] = {
                "appearances": count,
                "market_share_percentage": round((count / total_results) * 100, 2)
            }
        
        return market_share

    def _generate_charts(self, df: pd.DataFrame, session_id: str) -> Dict:
        """Genera gráficos y visualizaciones"""
        charts_info = {}
        
        try:
            # Gráfico de distribución de posiciones
            if 'position' in df.columns:
                plt.figure(figsize=(12, 6))
                plt.hist(df['position'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                plt.title('Distribución de Posiciones', fontsize=16, fontweight='bold')
                plt.xlabel('Posición')
                plt.ylabel('Frecuencia')
                plt.grid(True, alpha=0.3)
                
                chart_path = self.reports_dir / "images" / f"position_distribution_{session_id}.png"
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts_info["position_distribution"] = str(chart_path)
            
            # Gráfico de top dominios
            if 'domain' in df.columns:
                plt.figure(figsize=(12, 8))
                top_domains = df['domain'].value_counts().head(10)
                top_domains.plot(kind='barh', color='lightcoral')
                plt.title('Top 10 Dominios por Apariciones', fontsize=16, fontweight='bold')
                plt.xlabel('Número de Apariciones')
                plt.tight_layout()
                
                chart_path = self.reports_dir / "images" / f"top_domains_{session_id}.png"
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts_info["top_domains"] = str(chart_path)
            
            # Heatmap de keywords vs posiciones
            if all(col in df.columns for col in ['keyword', 'position']):
                keyword_positions = df.groupby('keyword')['position'].mean().head(15)
                
                plt.figure(figsize=(10, 8))
                sns.heatmap(keyword_positions.values.reshape(-1, 1), 
                           yticklabels=keyword_positions.index,
                           cmap='RdYlGn_r', annot=True, fmt='.1f')
                plt.title('Posición Promedio por Keyword', fontsize=16, fontweight='bold')
                plt.tight_layout()
                
                chart_path = self.reports_dir / "images" / f"keyword_heatmap_{session_id}.png"
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts_info["keyword_heatmap"] = str(chart_path)
                
        except Exception as e:
            self.logger.error(f"Error generando gráficos: {e}")
        
        return charts_info

    def export_to_html(self, report_data: Dict, session_id: str) -> str:
        """Exporta el reporte a HTML"""
        html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte SEO - Keyword Position Analysis</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .metric-card {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #3498db; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #2980b9; }}
        .chart-container {{ text-align: center; margin: 20px 0; }}
        .chart-container img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .recommendations {{ background: #d5f4e6; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60; }}
        .recommendations ul {{ margin: 0; padding-left: 20px; }}
        .recommendations li {{ margin: 8px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Reporte de Análisis SEO - Keyword Positions</h1>
        <p><strong>Fecha:</strong> {timestamp}</p>
        <p><strong>Sesión ID:</strong> {session_id}</p>
        
        <h2>📈 Resumen Ejecutivo</h2>
        <div class="metric-card">
            <div class="metric-value">{total_keywords}</div>
            <div>Keywords Analizadas</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{avg_position:.1f}</div>
            <div>Posición Promedio</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{top_10_results}</div>
            <div>Resultados en Top 10</div>
        </div>
        
        <h2>🎯 Recomendaciones</h2>
        <div class="recommendations">
            <ul>
                {recommendations_html}
            </ul>
        </div>
        
        <h2>📊 Visualizaciones</h2>
        {charts_html}
        
    </div>
</body>
</html>"""
        
        # Preparar datos para el template
        summary = report_data.get("summary", {})
        recommendations = report_data.get("recommendations", [])
        charts = report_data.get("charts", {})
        
        recommendations_html = "".join([f"<li>{rec}</li>" for rec in recommendations])
        
        charts_html = ""
        for chart_name, chart_path in charts.items():
            if os.path.exists(chart_path):
                charts_html += f'<div class="chart-container"><img src="{chart_path}" alt="{chart_name}"></div>'
        
        html_content = html_template.format(
            timestamp=report_data.get("timestamp", "N/A"),
            session_id=session_id,
            total_keywords=summary.get("total_keywords", 0),
            avg_position=summary.get("avg_position", 0),
            top_10_results=summary.get("top_10_results", 0),
            recommendations_html=recommendations_html,
            charts_html=charts_html
        )
        
        # Guardar archivo HTML
        html_path = self.reports_dir / "html" / f"report_{session_id}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)

    def cleanup_old_reports(self, days_to_keep: int = 30):
        """Limpia reportes antiguos para ahorrar espacio"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for directory in [self.reports_dir / "json", self.reports_dir / "html", self.reports_dir / "images"]:
            for file_path in directory.glob("*"):
                if file_path.stat().st_mtime < cutoff_date.timestamp():
                    file_path.unlink()
                    self.logger.info(f"🗑️ Archivo eliminado: {file_path.name}")