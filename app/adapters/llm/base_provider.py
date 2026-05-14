"""
Base class for all LLM providers.
"""
import abc
from typing import Dict, List, Optional

class BaseLLMProvider(abc.ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, name: str):
        self.name = name
        self.available = False
        self.last_error = None
        self.last_response_time = 0
    
    @abc.abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass
    
    @abc.abstractmethod
    def generate(self, prompt: str, timeout: int = 10) -> Optional[str]:
        """Generate text from prompt."""
        pass
    
    def validate_response(self, response: str) -> bool:
        """Validate if response is usable."""
        if not response or len(response.strip()) < 50:
            return False
        # Check for robotic phrases
        bad_phrases = [
            "apresentamos", "solucao completa", "adquira agora",
            "pessoas que tem interesse", "produto de qualidade"
        ]
        response_lower = response.lower()
        for phrase in bad_phrases:
            if phrase in response_lower:
                return False
        return True


class TemplateProvider(BaseLLMProvider):
    """Fallback template provider - always works, no installation needed."""
    
    def __init__(self):
        super().__init__("TemplateProvider")
        self.available = True
        self.templates = self._load_templates()
    
    def is_available(self) -> bool:
        return True
    
    def generate(self, prompt: str, timeout: int = 10) -> Optional[str]:
        """Generate script using intelligent templates."""
        import time
        start = time.time()
        
        # Detect style from prompt
        style = self._detect_style(prompt)
        template = self.templates.get(style, self.templates["viral"])
        
        # Extract product info
        product = self._extract_product(prompt)
        
        result = template.format(
            product=product,
            style=style
        )
        
        self.last_response_time = time.time() - start
        return result
    
    def _detect_style(self, prompt: str) -> str:
        """Detect commercial style from briefing."""
        prompt_lower = prompt.lower()
        
        if any(w in prompt_lower for w in ["fantasia", "medieval", "cosplay", "personagem"]):
            return "fantasia"
        elif any(w in prompt_lower for w in ["futurista", "cyberpunk", "neon", "tecnolog"]):
            return "futurista"
        elif any(w in prompt_lower for w in ["geek", "colecionavel", "action figure", "boneco"]):
            return "geek"
        elif any(w in prompt_lower for w in ["premium", "luxo", "elegante", "sofisticad"]):
            return "premium"
        elif any(w in prompt_lower for w in ["impressao", "3d", "customizad"]):
            return "impressao3d"
        elif any(w in prompt_lower for w in ["servico", "loja", "local"]):
            return "servico_local"
        else:
            return "viral"
    
    # TODO(GAL-901, type=debt): TemplateProvider product extraction uses first 5 words only
    # Contexto: "Comercial de 30 segundos para produto generico, es" extracts "Comercial de 30 segundos para..."
    # Dependência: Nenhuma
    # Critério de aceite: extract meaningful product name (heuristic: last noun phrase, or after "para"/"de")
    # Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md#gal-901
    
    def _extract_product(self, prompt: str) -> str:
        """Extract product name from briefing."""
        words = prompt.split()
        if len(words) > 5:
            return " ".join(words[:5]) + "..."
        return prompt[:50] if len(prompt) <= 50 else prompt[:50] + "..."
    
    def _load_templates(self) -> Dict[str, str]:
        """Load template dictionary."""
        return {
            "viral": """
[Cena 1: Hook - 3s]
Foco dramatico no {product}. Luz neon contrastante.
Texto na tela: 'O que voce esta prestes a ver...'
Narracao: 'Voce conhece o {product}?'

[Cena 2: Problema - 5s]
Cliente frustrado com produtos comuns. Corte rapido.
Texto: 'Cansado do mesmo sempre?'
Narracao: 'Existem produtos... e existem solucoes.'

[Cena 3: Solucao - 10s]
{product} em acao. Close-ups dinamicos. Movimento de camera: zoom in/out.
Texto: '{product} - Diferencial que voce sente'
Narracao: 'Apresentamos o {product}, desenhado para quem nao aceita o mediocre.'
Prompt visual: cinematic shot of {product}, dramatic lighting, high contrast, dynamic angle, 4k
Prompt negativo: blurry, low quality, boring, static

[Cena 4: Prova Social - 7s]
Pessoas reagindo com surpresa e satisfacao. Cortes rapidos.
Texto: 'Mais de 10.000 clientes transformados'
Narracao: 'Join the revolution.'

[Cena 5: Oferta - 3s]
Urgencia visual. Relogio ou contador na tela.
Texto: 'Oferta por tempo limitado'
Narracao: 'Nao perca essa chance.'

[Cena 6: CTA - 2s]
Logo e botao de acao. Brilho especial.
Texto: 'Adquira seu {product} hoje!'
Narracao: 'O {product} esta esperando por voce.'
""",
            
            "fantasia": """
[Cena 1: Introducao - 5s]
Ambiente medieval sombrio. {product} em destaque com iluminacao seletiva. Fumaça sutil ao fundo.
Texto na tela: 'Em um mundo de sombras...'
Narracao: 'Ha lendas que desafiam o tempo...'

[Cena 2: O Produto - 12s]
{product} em detalhes artesanais. Close-ups das texturas, costuras, detalhes dourados. Movimento de camera: orbitando o produto lentamente.
Texto: '{product} - Feito a mao para guerreiros modernos'
Narracao: 'Conheca o {product}, onde a tradicao encontra a arte.'
Prompt visual: medieval fantasy {product}, artisanal craftsmanship, gold details, dark atmospheric lighting, cinematic shot, 4k, highly detailed
Prompt negativo: modern, plastic, cheap, low quality, bad anatomy

[Cena 3: Personagem - 8s]
Modelo vestindo {product}. Poses dramaticas. Vento movendo a capa/tecido.
Texto: 'Vista a lenda'
Narracao: 'Nao seja apenas mais um no evento.'

[Cena 4: Bastidores - 5s]
Artesao criando {product}. Maos trabalhando o material. Foco no processo.
Texto: 'Cada peca, uma obra unica'
Narracao: 'Feito especialmente para voce.'

[Cena 5: CTA - 5s]
{product} em apresentacao nobre. Selo de garantia.
Texto: 'Leve a magia para casa'
Narracao: 'O {product} esta esperando por voce.'
""",
            
            "futurista": """
[Cena 1: Hook - 3s]
Ambiente cyberpunk. {product} brilha com luzes neon. Visor verde ativado.
Texto na tela: 'Bem-vindo ao futuro'
Narracao: 'O ano e 2026, e a tecnologia... evoluiu.'

[Cena 2: Tecnologia - 12s]
{product} em acao. Interface holografica ao fundo. Movimento de camera: fly-through de dentro para fora.
Texto: '{product} - Tecnologia que voce sente'
Narracao: 'Apresentamos o {product}, com processamento neural avancado e design ergonomico.'
Prompt visual: futuristic {product}, neon lights, cyberpunk aesthetic, high tech, holographic interface, cinematic, 4k
Prompt negativo: outdated, retro, low tech, blurry

[Cena 3: Performance - 8s]
Testes de velocidade/resistencia. Cortes em slow motion.
Texto: 'Resistente. Rapido. Impar'
Narracao: 'Desenhado para quem vive no limite.'

[Cena 4: Estilo de Vida - 5s]
Jovem urbano usando {product} em ambiente moderno.
Texto: 'Seu dia, sua cidade, seu estilo'
Narracao: 'Integre o {product} ao seu mundo.'

[Cena 5: CTA - 2s]
Logo em estilo neon. Brilho pulsante.
Texto: 'Garanta o seu {product}'
Narracao: 'O futuro esta em suas maos.'
""",
            
            "geek": """
[Cena 1: Hook - 4s]
{product} em pedestal premium. Luz de spot dramatica. Fumaça leve.
Texto na tela: 'Para os verdadeiros colecionadores'
Narracao: 'Voce nao e apenas um fas...'

[Cena 2: Detalhes - 10s]
{product} em close-ups extremos. Pintura, articulacao, accessories. Movimento de camera: macro shots com dollying.
Texto: '{product} - Precisao em cada detalhe'
Narracao: 'O {product} traz fidelidade absoluta ao design original.'
Prompt visual: collectible {product}, macro shot, intricate details, studio lighting, premium quality, 4k
Prompt negativo: toy-like, cheap, low detail, bad paint

[Cena 3: Colecao - 8s]
Varias unidades de {product} em exposicao. Prateleira organizada.
Texto: 'Edicao limitada'
Narracao: 'Cada peca e numerada e certificada.'

[Cena 4: Unboxing - 5s]
Maos abrindo embalagem premium. Camada por camada revelando {product}.
Texto: 'Experiencia de unboxing inesquecivel'
Narracao: 'Nao e apenas um produto, e uma experiencia.'

[Cena 5: CTA - 3s]
{product} na caixa premium. Selo de garantia.
Texto: 'Adicione aa sua colecao'
Narracao: 'O {product} esta esperando por voce.'
""",
            
            "impressao3d": """
[Cena 1: Hook - 4s]
{product} sendo impresso em tempo real. Timelapse acelerado.
Texto na tela: 'Criado camada por camada'
Narracao: 'Ja imaginou ter qualquer coisa que voce sonhar?'

[Cena 2: Tecnologia - 12s]
Close-ups da impressora 3D trabalhando. Detalhes da textura da impressao. Camera: top-down view seguido de orbit.
Texto: '{product} - Precisao de micron'
Narracao: 'O {product} e criado com tecnologia de ponta, resolução de 50 microns.'
Prompt visual: 3D printed {product}, layer lines visible, high detail, studio lighting, technical precision, 4k
Prompt negativo: low poly, blurry, messy, stringing

[Cena 3: Personalizacao - 8s]
Cliente escolhendo cores e formatos no computador. Tela de design.
Texto: 'Personalize como quiser'
Narracao: 'Seu {product} unico, feito do seu jeito.'

[Cena 4: Aplicacao - 5s]
{product} em uso real. Funcionalidade demonstrada.
Texto: 'Perfeito para sua necessidade'
Narracao: 'Veja o {product} transformar seu dia a dia.'

[Cena 5: CTA - 3s]
{product} finalizado. Botao de pedido online.
Texto: 'Peça o seu {product} impresso'
Narracao: 'O {product} esta a um click de distancia.'
""",
        }