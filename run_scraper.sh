#!/bin/bash
# Script de lanzamiento para Keyword Position Scraper
# Este script puede ejecutarse desde cualquier ubicación

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
"$SCRIPT_DIR/linux/dist/KeywordPositionScraper"
