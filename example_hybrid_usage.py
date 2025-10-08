#!/usr/bin/env python3
"""
📚 Ejemplo de Uso de Funcionalidades Híbridas
Demuestra cómo usar las nuevas capacidades de análisis combinado

Este script muestra ejemplos prácticos de:
1. Sincronización automática de keywords
2. Análisis híbrido de datos
3. Generación de reportes
4. Detección de oportunidades
"""

import sys
import os
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from project_manager import ProjectManager
from search_console_api import SearchConsoleAPI
from stealth_scraper import StealthSerpScraper
from sc_scraper_sync import SearchConsoleScraperSync
from hybrid_analyzer import HybridAnalyzer
from hybrid_report_generator import HybridReportGenerator
from config.settings import config


def example_1_sync_keywords():
    """
    Ejemplo 1: Sincronizar keywords de Search Console a un proyecto
    """
    print("\n" + "="*60)
    print("📥 EJEMPLO 1: Sincronización Automática de Keywords")
    print("="*60)

    pm = ProjectManager()
    sync = SearchConsoleScraperSync(pm)

    # Obtener proyecto activo (o crear uno nuevo)
    active_project = pm.get_active_project()

    if not active_project:
        print("❌ No hay proyecto activo. Crea uno primero en la GUI.")
        return

    project_id = active_project['id']
    print(f"\n✅ Usando proyecto: {active_project['name']}")

    # Sincronizar keywords
    print("\n🔄 Sincronizando keywords de Search Console...")

    result = sync.sync_keywords_to_project(
        project_id=project_id,
        days=30,              # Últimos 30 días
        min_impressions=50,   # Mínimo 50 impresiones
        auto_add=False        # No añadir automáticamente (solo mostrar)
    )

    if result['success']:
        print(f"\n✅ Sincronización completada:")
        print(f"   • Keywords en Search Console: {result['total_sc_keywords']}")
        print(f"   • Nuevas keywords encontradas: {result['new_keywords_found']}")

        if result['new_keywords_list']:
            print(f"\n📋 Top 10 nuevas keywords recomendadas:")
            for i, kw in enumerate(result['new_keywords_list'][:10], 1):
                print(f"   {i}. {kw}")

        # Mostrar preview de datos
        if result['keywords_data']:
            print(f"\n📊 Preview de keywords con más impresiones:")
            for kw_data in result['keywords_data'][:5]:
                print(f"   • {kw_data['keyword']}")
                print(f"     Impresiones: {kw_data['impressions']:,} | Clicks: {kw_data['clicks']} | Pos: {kw_data['position']:.1f}")
    else:
        print(f"\n❌ Error: {result.get('message', 'Error desconocido')}")


def example_2_smart_scraping_list():
    """
    Ejemplo 2: Generar lista inteligente de keywords para scrapear
    """
    print("\n" + "="*60)
    print("🎯 EJEMPLO 2: Lista Inteligente de Scraping")
    print("="*60)

    pm = ProjectManager()
    sync = SearchConsoleScraperSync(pm)

    active_project = pm.get_active_project()
    if not active_project:
        print("❌ No hay proyecto activo.")
        return

    project_id = active_project['id']

    # Probar diferentes estrategias
    strategies = {
        'opportunities': 'Keywords con más potencial de mejora',
        'top_volume': 'Keywords con más impresiones',
        'low_hanging': 'Quick wins (posiciones 4-10)'
    }

    for strategy, description in strategies.items():
        print(f"\n📍 Estrategia: {strategy}")
        print(f"   {description}")

        keywords = sync.get_smart_scraping_list(
            project_id=project_id,
            strategy=strategy,
            limit=10
        )

        if keywords:
            print(f"   Keywords recomendadas ({len(keywords)}):")
            for i, kw in enumerate(keywords[:5], 1):
                print(f"     {i}. {kw}")
        else:
            print("   ⚠️ No hay keywords disponibles (verifica autenticación de SC)")


def example_3_find_opportunities():
    """
    Ejemplo 3: Encontrar oportunidades de mejora
    """
    print("\n" + "="*60)
    print("🚀 EJEMPLO 3: Detección de Oportunidades")
    print("="*60)

    # Nota: Este ejemplo requiere datos reales de Search Console
    # En un caso real, obtendrías los datos así:

    sc_api = SearchConsoleAPI()

    if not sc_api.is_authenticated():
        print("❌ No autenticado con Search Console.")
        print("   Autentica primero en la GUI (pestaña Configuración)")
        return

    pm = ProjectManager()
    active_project = pm.get_active_project()

    if not active_project:
        print("❌ No hay proyecto activo.")
        return

    site_url = active_project.get('search_console_property')
    if not site_url:
        print("❌ Proyecto no tiene URL de Search Console configurada.")
        return

    print(f"\n✅ Obteniendo datos de Search Console para: {site_url}")

    from datetime import datetime, timedelta
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    sc_response = sc_api.get_search_analytics(
        site_url=site_url,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        dimensions=['query'],
        row_limit=500
    )

    if not sc_response or 'rows' not in sc_response:
        print("❌ No hay datos disponibles en Search Console")
        return

    sc_data = sc_response['rows']
    print(f"✅ Obtenidos {len(sc_data)} queries de Search Console")

    # Analizar oportunidades
    analyzer = HybridAnalyzer()

    opportunities = analyzer.find_keyword_opportunities(
        sc_data=sc_data,
        min_impressions=100,
        max_position=20.0,
        min_position=4.0
    )

    print(f"\n🎯 Encontradas {len(opportunities)} oportunidades de mejora\n")

    if opportunities:
        print("Top 10 Oportunidades:")
        print("-" * 100)
        print(f"{'#':<3} {'Keyword':<30} {'Posición':<10} {'Impres.':<12} {'Clicks':<8} {'CTR':<8} {'Potencial':<15}")
        print("-" * 100)

        for i, opp in enumerate(opportunities[:10], 1):
            print(
                f"{i:<3} "
                f"{opp['keyword'][:28]:<30} "
                f"{opp['current_position']:<10.1f} "
                f"{opp['impressions']:<12,} "
                f"{opp['clicks']:<8} "
                f"{opp['ctr']:<8.2f} "
                f"+{opp['potential_additional_clicks']} clicks/mes"
            )
    else:
        print("ℹ️  No se encontraron oportunidades con los criterios especificados")


def example_4_full_analysis():
    """
    Ejemplo 4: Análisis completo con generación de reporte
    """
    print("\n" + "="*60)
    print("📊 EJEMPLO 4: Análisis Completo + Reporte HTML")
    print("="*60)

    pm = ProjectManager()
    sync = SearchConsoleScraperSync(pm)

    active_project = pm.get_active_project()
    if not active_project:
        print("❌ No hay proyecto activo.")
        return

    project_id = active_project['id']
    target_domain = active_project.get('domain')

    print(f"\n✅ Proyecto: {active_project['name']}")
    print(f"   Dominio: {target_domain}")

    # 1. Obtener keywords inteligentes
    print("\n🎯 Generando lista inteligente de keywords...")
    smart_keywords = sync.get_smart_scraping_list(
        project_id=project_id,
        strategy='opportunities',
        limit=20  # Solo 20 para el ejemplo (no gastar muchas llamadas API)
    )

    if not smart_keywords:
        print("⚠️ No hay keywords disponibles. Usando keywords del proyecto...")
        smart_keywords = pm.get_project_keywords(project_id)[:20]

    if not smart_keywords:
        print("❌ No hay keywords para scrapear.")
        return

    print(f"✅ {len(smart_keywords)} keywords seleccionadas")

    # 2. Hacer scraping
    print(f"\n🔍 Scrapeando posiciones...")
    scraper = StealthSerpScraper(config)

    results = scraper.batch_position_check(
        keywords=smart_keywords,
        target_domain=target_domain,
        pages=1  # Solo 1 página para el ejemplo
    )

    print(f"✅ Scraping completado: {len(results)} resultados")

    if not results:
        print("❌ No se obtuvieron resultados del scraping.")
        return

    # 3. Analizar con datos de SC
    print(f"\n🔬 Analizando con datos de Search Console...")

    analysis = sync.analyze_scraping_session_with_sc(
        project_id=project_id,
        scraper_results=results,
        save_to_project=True
    )

    if not analysis:
        print("❌ Error en el análisis.")
        return

    # Mostrar resumen
    print(f"\n📊 Resumen del Análisis:")
    print(f"   • Keywords scrapeadas: {analysis['scraper_summary']['total_keywords']}")
    print(f"   • Resultados totales: {analysis['scraper_summary']['total_results']}")

    if analysis.get('has_sc_data'):
        print(f"   • ✅ Datos de Search Console disponibles")

        if 'visibility_score' in analysis:
            score = analysis['visibility_score']['overall_visibility_score']
            rating = analysis['visibility_score']['rating']
            print(f"   • Score de Visibilidad: {score:.1f}/100 - {rating}")

        if 'opportunities' in analysis:
            print(f"   • Oportunidades encontradas: {len(analysis['opportunities'])}")

        if 'content_gaps' in analysis:
            print(f"   • Gaps de contenido: {len(analysis['content_gaps'])}")
    else:
        print(f"   • ⚠️ Sin datos de Search Console")

    # 4. Generar reporte HTML
    print(f"\n📄 Generando reporte HTML...")

    generator = HybridReportGenerator()
    report_path = generator.generate_html_report(
        analysis=analysis,
        project_name=active_project['name']
    )

    if report_path:
        print(f"✅ Reporte generado: {report_path}")
        print(f"\n💡 Abre el reporte en tu navegador para ver el análisis completo")
    else:
        print("❌ Error generando reporte HTML")


def main():
    """Menú principal"""
    print("\n" + "="*60)
    print("🚀 EJEMPLOS DE FUNCIONALIDADES HÍBRIDAS")
    print("   Search Console + Scraper")
    print("="*60)

    print("\nElige un ejemplo para ejecutar:")
    print("1. Sincronizar keywords de Search Console")
    print("2. Generar listas inteligentes de scraping")
    print("3. Detectar oportunidades de mejora")
    print("4. Análisis completo + Reporte HTML")
    print("5. Ejecutar todos los ejemplos")
    print("0. Salir")

    try:
        choice = input("\nOpción: ").strip()

        if choice == '1':
            example_1_sync_keywords()
        elif choice == '2':
            example_2_smart_scraping_list()
        elif choice == '3':
            example_3_find_opportunities()
        elif choice == '4':
            example_4_full_analysis()
        elif choice == '5':
            example_1_sync_keywords()
            example_2_smart_scraping_list()
            example_3_find_opportunities()
            example_4_full_analysis()
        elif choice == '0':
            print("\n👋 ¡Hasta luego!")
            return
        else:
            print("\n❌ Opción inválida")

        print("\n" + "="*60)
        print("✅ Ejemplo completado")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\n👋 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
