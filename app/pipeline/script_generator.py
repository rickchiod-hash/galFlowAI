import json
from app.logging_config import setup_logger

logger = setup_logger()

def generate_script(briefing, project_id=None, use_ollama=True):
    """Gera roteiro a partir do briefing usando templates ou Ollama."""
    msg = "Gerando roteiro para: %s" % str(briefing)[:50]
    logger.info(msg)
    
    # Tentar Ollama primeiro se disponivel
    if use_ollama:
        try:
            from app.adapters.ollama_adapter import check_ollama_available, generate_with_ollama
            if check_ollama_available():
                logger.info("Usando Ollama para gerar roteiro")
                result = generate_with_ollama(briefing)
                if result:
                    logger.info("Roteiro gerado via Ollama")
                    return result
        except Exception as e:
            logger.warning("Falha no Ollama: %s", e)
    
    # Fallback para template
    logger.info("Usando template fallback")
    words = briefing.lower().split()
    product = "produto"
    if "maquiagem" in words or "makeup" in words:
        product = "maquiagem"
    elif "boneco" in words or "action figure" in words:
        product = "boneco colecionavel"
    elif "impress" in words or "3d" in words:
        product = "produto impresso em 3D"
    
    template = (
        "[Cena 1: Introducao - 5s]\n"
        "Foco no %s em ambiente moderno. Luz suave destacando o produto.\n"
        "Texto na tela: 'Apresentamos o novo %s'\n\n"
        "[Cena 2: Beneficios - 15s]\n"
        "Demonstracao rapida dos diferenciais. Close-ups das caracteristicas.\n"
        "Texto: 'Qualidade premium, design unico'\n\n"
        "[Cena 3: Prova Social - 7s]\n"
        "Pessoas interagindo com o %s. Sorrisos e satisfacao.\n"
        "Texto: 'Amado por clientes'\n\n"
        "[Cena 4: Oferta - 3s]\n"
        "Preco e condicoes especiais. Urgencia.\n"
        "Texto: 'Oferta limitada'\n\n"
        "[Cena 5: Chamada - 5s]\n"
        "Logo da marca. Botao de acao.\n"
        "Texto: 'Adquira ja o seu %s!'"
    ) % (product, product, product, product)
    
    logger.info("Roteiro gerado com 5 cenas")
    return template

def save_script(project_id, script_text):
    """Salva roteiro no projeto."""
    from app.config import PROJECTS_DIR
    proj_dir = PROJECTS_DIR / project_id
    script_path = proj_dir / "script" / "script.txt"
    script_path.write_text(script_text, encoding="utf-8")
    proj_file = proj_dir / "project.json"
    content = proj_file.read_text(encoding="utf-8")
    proj = json.loads(content)
    proj["script"] = script_text
    proj["status"] = "script_generated"
    proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Roteiro salvo: %s", script_path.name)
    return str(script_path)
