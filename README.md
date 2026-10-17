# IA e Medicina: do vocabulário à leitura crítica

O livro do curso IA e Medicina do [IA.med](https://iamed.cc): 14 capítulos, das Aulas 00 a 13, do básico ao avançado, para entender, avaliar e usar ferramentas de inteligência artificial na prática clínica. Não é preciso saber programar.

Por Fabiano Novaes Barcellos Filho. Edição de outubro de 2026, 108 páginas.

**Baixar o PDF:** na página [Releases](https://github.com/Medicina-IA/livro-ia-e-medicina/releases/latest). Quem assina o IA.med também encontra o livro em [app.iamed.cc/aulas](https://app.iamed.cc/aulas), ao lado dos vídeos.

## O que tem no livro

| Parte | Aulas |
|---|---|
| I · Básico | 00 IA e Medicina (abertura) · 01 Por que a IA entrou na medicina · 02 O léxico da IA · 03 Dados em saúde · 04 A matriz de dados |
| II · Intermediário | 05 Modelos lineares · 06 Árvores e ensembles · 07 SVM, KNN e Naive Bayes · 08 Sem rótulo e com tempo · 09 Redes neurais e CNN |
| III · Avançado | 10 Sequência e linguagem · 11 Discriminação · 12 Calibração e utilidade clínica · 13 Quando o modelo falha |

Cada capítulo traz as figuras dos slides da aula, caixas "Na prática", "Para ler um artigo" e "Cuidado", um resumo no fim e as referências citadas. No fim do livro há a lista de referências por aula e um glossário com os termos de todas as aulas.

É material educacional e não substitui o julgamento clínico. Exemplos marcados como ilustrativos não vêm de estudos.

## Como o livro é feito

```
cap/        capítulos em HTML (capNN.html), glossário por aula (glosNN.json) e referências (refs.json)
fig/        figuras: os slides das aulas renderizados em PNG
ebook.css   o design das páginas (A4)
tools/      build.py monta o HTML do livro e gera o PDF
docs/       como escrever ou corrigir um capítulo
```

Para gerar o PDF (Python 3, testado no 3.13):

```bash
pip install -r requirements.txt
playwright install chromium
python3 tools/build.py
```

O PDF sai em `dist/IAmed-Curso-IA-e-Medicina.pdf`. As fontes (Geist, Instrument Serif e JetBrains Mono) vêm do Google Fonts, então a geração precisa de internet. O build se recusa a gerar o PDF se algum capítulo ainda tiver um `[CONFERIR]`.

## Correções

Achou um erro, uma referência quebrada ou uma passagem confusa? Abra uma [issue](https://github.com/Medicina-IA/livro-ia-e-medicina/issues) dizendo a aula, a página do PDF e o trecho. Mudança de texto segue as regras de `docs/escrever-um-capitulo.md`: nada de número, estudo ou citação sem fonte conferida.

## Licença

- Texto e figuras: [Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br) (CC BY-NC-SA 4.0), em `LICENSE`. Você pode copiar e adaptar, dando o crédito, sem uso comercial e compartilhando a adaptação sob a mesma licença.
- Código (`tools/`): MIT, em `LICENSE-CODE`.

Para citar: Barcellos Filho FN. IA e Medicina: do vocabulário à leitura crítica. IA.med; 2026. Disponível em: https://github.com/Medicina-IA/livro-ia-e-medicina
