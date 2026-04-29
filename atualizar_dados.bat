@echo off
:: Garantir que caracteres especiais e acentos apareçam
chcp 65001 > null

:: ================================================================================
:: SCRIPT DE ATUALIZAÇÃO: COMMIT AUTOMÁTICO PARA GITHUB AGROROBÓTIICA -> STREAMLIT
:: ================================================================================

echo.
echo [1/2] Preparando o commit para o GitHub:
git add .
git commit -m "Sincronização Automática: %date% %time%"

echo.
echo [2/2] Enviando para o Streamlit
git push origin main

echo.
echo ===================================================================
echo SUCESSO! O dashboard será atualizado em aproximadamente 1 minuto
echo ===================================================================
exit