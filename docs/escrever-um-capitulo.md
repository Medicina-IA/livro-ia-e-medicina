# Como escrever ou corrigir um capítulo

Cada aula do curso IA e Medicina vira um capítulo em `cap/capNN.html`. Leitor: médico ou estudante, sem programação. O modelo é `cap/cap01.html`: copie a estrutura, o tom e a marcação.

## Estrutura de um capítulo
1. Abertura: número, título, subtítulo e "Nesta aula você vai" com 3 itens.
2. Corpo em prosa seguindo a ordem dos slides da aula. Cada slide de conteúdo vira um trecho com `<h2>` próprio (ou se junta ao vizinho quando for curto).
3. Figuras: de 3 a 6 por capítulo, só slides com desenho ou diagrama, em `fig/aulaNN/<slide>.png`. Nunca capa, próxima aula, encerramento ou frase de destaque. Legenda numerada "Figura NN.M" explicando o que olhar no desenho.
4. Caixas: pelo menos uma "Na prática" (situação clínica) e uma "Para ler um artigo" (o que procurar num estudo) por capítulo. "Cuidado" quando houver armadilha.
5. "Em resumo": de 3 a 5 frases curtas no fim.
6. Glossário: `cap/glosNN.json` com de 3 a 8 termos novos da aula: `[{"termo":"...","def":"uma frase"}]`.
7. Referências: todo estudo citado no texto entra em `cap/refs.json`, na chave da aula (`"09"`), no estilo Vancouver, com DOI.

## Regras de texto
- Português do Brasil, acentuação correta, segunda pessoa ("você"), frases diretas, tom de professor que é médico. Nada de abertura bajuladora, nada de "neste capítulo exploraremos".
- Proibido: travessão (em dash ou en dash), aspas tipográficas (use só aspas retas "), reticências Unicode (use ... se precisar), hífen decorativo em título.
- Escreva para quem lê, não para quem grava: nada de "câmera", "clipe", "pausar e perguntar".
- Nenhum número, estatística, citação ou referência sem fonte conferida (PubMed, DOI, site oficial). Exemplos ilustrativos são ditos como ilustrativos.
- Dúvida em aberto vai marcada como `<span class="conferir">[CONFERIR: ...]</span>`. O `tools/build.py` se recusa a gerar o PDF enquanto houver uma.
- Extensão: de 900 a 1.500 palavras de prosa por capítulo.

## Marcação HTML (só estas classes; o CSS está em `ebook.css`)
```html
<section class="cap" id="capNN">
  <div class="cap-abre">
    <p class="cap-num">Aula NN</p>
    <h1>Título</h1>
    <p class="cap-sub">Subtítulo</p>
    <div class="cap-objetivos"><p class="rot">Nesta aula você vai</p><ul><li>...</li></ul></div>
  </div>
  <h2>Seção</h2>
  <p>Texto...</p>
  <figure class="fig"><img src="fig/aulaNN/slide.png" alt="descrição curta"><figcaption><b>Figura NN.M</b> Legenda.</figcaption></figure>
  <aside class="box pratica"><p class="rot">Na prática</p><p>...</p></aside>
  <aside class="box artigo"><p class="rot">Para ler um artigo</p><p>...</p></aside>
  <aside class="box cuidado"><p class="rot">Cuidado</p><p>...</p></aside>
  <div class="resumo"><p class="rot">Em resumo</p><ul><li>...</li></ul></div>
</section>
```
- `NN` com dois dígitos (cap05, aula05, Figura 05.2). Sem estilos inline, sem scripts.
