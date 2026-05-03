@echo off
echo ===============================================
echo  INSTRUCOES LM STUDIO - INSTALACAO NO K:
echo ===============================================
echo.
echo 1. Baixe o LM Studio de: https://lmstudio.ai
echo    (Instale normalmente, pode ser no C: - os modelos ficarao no K:)
echo.
echo 2. Abra o LM Studio
echo.
echo 3. Va em: Developer -> Local Server
echo.
echo 4. Configure:
echo    - Porta: 1234
echo    - Modelo: escolha um modelo leve (ex: Llama 3.2 3B)
echo    - Load Model
echo.
echo 5. Defina a pasta de modelos para:
echo    K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\lmstudio
echo    (No LM Studio: Settings -> Models path)
echo.
echo 6. Teste se esta funcionando:
echo    curl http://localhost:1234/v1/models
echo.
echo ===============================================
echo  PRESSIONE QUALQUER TECLA PARA ABRIR A DOCUMENTACAO
echo ===============================================
pause >nul
start "" "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\docs\INSTALAR_LM_STUDIO_K.md"
