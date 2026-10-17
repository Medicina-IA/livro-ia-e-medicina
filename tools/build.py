import glob, json, os, re, sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright
import pdfplumber
from pypdf import PdfReader, PdfWriter

# Raiz do repositório (a pasta acima de tools/). O PDF sai em dist/.
E = str(Path(__file__).resolve().parent.parent)
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{E}/dist/IAmed-Curso-IA-e-Medicina.pdf"
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)

NIVEIS = [
    ("I", "Básico", "O vocabulário, os dados em saúde e o raciocínio clínico por trás de um modelo.", range(0, 5)),
    ("II", "Intermediário", "As famílias de algoritmos, uma a uma, com indicação clínica e limitação.", range(5, 10)),
    ("III", "Avançado", "Linguagem, avaliação de desempenho, equidade, drift e regulação.", range(10, 14)),
]

caps = {}
for n in range(14):
    f = f"{E}/cap/cap{n:02d}.html"
    if os.path.exists(f):
        caps[n] = open(f, encoding="utf-8").read()

def titulo(h):
    m = re.search(r"<h1>(.*?)</h1>", h, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""

titulos = {n: titulo(h) for n, h in caps.items()}

def capa():
    return """<div class="full capa">
<p class="marca">IA.med · curso IA e Medicina</p>
<svg width="300" height="300" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
<circle cx="150" cy="150" r="140" fill="none" stroke="#1d3527" stroke-width="2"/>
<circle cx="150" cy="175" r="105" fill="none" stroke="#2c4a38" stroke-width="2"/>
<circle cx="150" cy="200" r="70" fill="#13261b" stroke="#7ff0b0" stroke-width="2"/>
<circle cx="150" cy="222" r="34" fill="#7ff0b0"/>
</svg>
<h1>IA e Medicina</h1>
<p class="serif">do vocabulário à leitura crítica</p>
<p class="lede">O livro que acompanha o curso: 14 capítulos, do básico ao avançado, para entender, avaliar e usar ferramentas de inteligência artificial na prática clínica.</p>
<p class="autor">Fabiano Novaes Barcellos Filho<span>outubro de 2026</span></p>
</div>"""

def como_usar(paginas):
    linhas = []
    for num, nome, _, rng in NIVEIS:
        linhas.append(f'<p class="nivel">Parte {num} · {nome}</p>')
        for n in rng:
            if n in caps:
                pg = paginas.get(n, "")
                linhas.append(f'<div class="item"><span>{n:02d}</span><a href="#cap{n:02d}">{html.escape(titulos[n])}</a><span style="margin-left:auto;width:auto">{pg}</span></div>')
    pg_r = paginas.get("referencias", "")
    pg_g = paginas.get("glossario", "")
    linhas.append(f'<p class="nivel">Apoio</p><div class="item"><span>·</span><a href="#referencias">Referências</a><span style="margin-left:auto;width:auto">{pg_r}</span></div>'
                  f'<div class="item"><span>·</span><a href="#glossario">Glossário</a><span style="margin-left:auto;width:auto">{pg_g}</span></div>')
    return f"""<div class="pagina">
<h1>Como usar este livro</h1>
<p>Este livro acompanha o curso IA e Medicina do IA.med. Cada capítulo corresponde a uma aula e pode ser lido antes, durante ou depois do vídeo. Os capítulos seguem a ordem do curso: os do nível básico preparam o vocabulário para os do intermediário, e estes preparam o avançado.</p>
<p>As figuras são as mesmas dos slides das aulas, e os estudos citados no texto estão listados, aula por aula, na página de referências. As caixas verdes trazem situações da prática clínica; as cinzas, o que procurar ao ler um artigo; as amarelas, armadilhas comuns. Cada capítulo termina com um resumo, e no fim do livro há um glossário com os termos de todas as aulas.</p>
<p>Não é preciso saber programar. O objetivo é entender o raciocínio por trás de um modelo para decidir quando confiar nele.</p>
<div class="sumario"><h1 style="margin-top:9mm">Sumário</h1>{''.join(linhas)}</div>
</div>"""

def parte(num, nome, desc, rng):
    itens = "".join(f"<li>{n:02d} · {html.escape(titulos[n])}</li>" for n in rng if n in caps)
    return f'<div class="full parte"><p class="num">Parte {num}</p><h1>{nome}</h1><p>{desc}</p><ul>{itens}</ul></div>'

def referencias():
    refs = json.load(open(f"{E}/cap/refs.json", encoding="utf-8"))
    blocos = "".join(f'<h2>Aula {k} · {html.escape(titulos[int(k)])}</h2><ol>'
                     + "".join(f"<li>{html.escape(r)}</li>" for r in v) + "</ol>"
                     for k, v in sorted(refs.items()))
    return f'<div class="pagina referencias" id="referencias"><h1>Referências</h1>{blocos}</div>'

def glossario():
    termos = {}
    for n in range(14):
        f = f"{E}/cap/glos{n:02d}.json"
        if not os.path.exists(f):
            continue
        for t in json.load(open(f, encoding="utf-8")):
            k = t["termo"].strip()
            if k.lower() not in {x.lower() for x in termos}:
                termos[k] = (t["def"].strip(), n)
    itens = "".join(f"<dt>{html.escape(k)}</dt><dd>{html.escape(d)} <span>Aula {n:02d}</span></dd>"
                    for k, (d, n) in sorted(termos.items(), key=lambda x: x[0].lower()))
    return f'<div class="pagina glossario" id="glossario"><h1>Glossário</h1><dl>{itens}</dl></div>'

def pendencias():
    itens = []
    for n, h in caps.items():
        for m in re.finditer(r'<span class="conferir">(.*?)</span>', h, re.S):
            itens.append(f"<li><b>Aula {n:02d}</b> {re.sub('<[^>]+>', '', m.group(1))}</li>")
    # figuras com o marcador desenhado dentro do próprio slide
    marcadas = ["aula00/aproveitar", "aula01/linha", "aula01/evidencia", "aula01/complexidades",
                "aula01/distribuido", "aula13/regulacao"]
    usadas = "".join(caps.values())
    figs = [f"<li><b>{m}.png</b> resolver no slide e renderizar a figura de novo</li>"
            for m in marcadas if f"fig/{m}.png" in usadas]
    if not itens and not figs:
        return ""
    return ('<div class="pagina revisao"><h1>Pendências de revisão</h1>'
            '<p>Lista interna para a versão de revisão. Resolver cada item e remover esta página antes de enviar aos assinantes.</p>'
            f'<ul>{"".join(itens)}</ul>'
            + (f'<h2 style="font-size:13pt;font-weight:500;margin:6mm 0 2mm">Figuras com marcador dentro da imagem</h2><ul>{"".join(figs)}</ul>' if figs else "")
            + '</div>')

def colofao():
    return ('<div class="pagina colofao"><h1>Sobre este livro</h1>'
            '<p>IA e Medicina: do vocabulário à leitura crítica. Material de apoio do curso do IA.med, por Fabiano Novaes Barcellos Filho.</p>'
            '<p>Exemplos marcados como ilustrativos não vêm de estudos e servem só para explicar o conceito. Este material é educacional e não substitui o julgamento clínico.</p>'
            '<p>Edição de outubro de 2026. A seção sobre regulação retrata a situação nesse mês.</p>'
            '<p>Texto e figuras sob a licença Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional (<span style="white-space:nowrap;hyphens:none">CC BY-NC-SA 4.0</span>): você pode copiar e adaptar, com crédito, sem uso comercial e compartilhando do mesmo jeito. Fonte, correções e novas edições em <span style="white-space:nowrap;hyphens:none">github.com/Medicina-IA/livro-ia-e-medicina</span>.</p></div>')

def montar(paginas):
    corpo = [capa(), como_usar(paginas)]
    for num, nome, desc, rng in NIVEIS:
        corpo.append(parte(num, nome, desc, rng))
        corpo += [caps[n] for n in rng if n in caps]
    corpo += [referencias(), glossario(), colofao()]
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>IA e Medicina · IA.med</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="ebook.css"></head><body>{''.join(corpo)}</body></html>"""

FOOTER = '<div style="width:100%;font-family:Arial;font-size:7.5pt;color:#8fa898;padding:0 18mm;display:flex;justify-content:space-between"><span>IA e Medicina · IA.med</span><span class="pageNumber"></span></div>'

def render(htmltxt, out):
    src = f"{E}/ebook.html"
    open(src, "w", encoding="utf-8").write(htmltxt)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + src, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=out, print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template="<div></div>", footer_template=FOOTER)
        b.close()

def achar_paginas(pdf):
    achados = {}
    with pdfplumber.open(pdf) as d:
        textos = [(pg.extract_text() or "") for pg in d.pages]
    for n in caps:
        alvo = f"Aula {n:02d}"
        for i, t in enumerate(textos):
            if t.strip().startswith(alvo) or ("\n" + alvo + "\n") in ("\n" + t) and titulos[n][:20] in t.replace("\n", " "):
                achados[n] = i + 1
                break
    for i, t in enumerate(textos):
        if t.strip().startswith("Glossário"):
            achados["glossario"] = i + 1
        if t.strip().startswith("Referências"):
            achados["referencias"] = i + 1
    return achados, len(textos)

if any('class="conferir"' in h for h in caps.values()):
    sys.exit("Ainda há [CONFERIR] nos capítulos: resolver antes de gerar a versão final.")
render(montar({}), OUT)
paginas, total = achar_paginas(OUT)
render(montar(paginas), OUT)
# marcadores do PDF
r = PdfReader(OUT); w = PdfWriter(); w.append(r)
for n in sorted(k for k in paginas if isinstance(k, int)):
    w.add_outline_item(f"{n:02d} · {titulos[n]}", paginas[n] - 1)
if "referencias" in paginas:
    w.add_outline_item("Referências", paginas["referencias"] - 1)
if "glossario" in paginas:
    w.add_outline_item("Glossário", paginas["glossario"] - 1)
w.add_metadata({"/Title": "IA e Medicina: do vocabulário à leitura crítica", "/Author": "Fabiano Novaes Barcellos Filho"})
with open(OUT, "wb") as f:
    w.write(f)
print("paginas", total, paginas)
