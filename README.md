<!-- ============================= -->
<!-- HEADER / THUMBNAIL -->
<!-- ============================= -->

<div align="center">
  
<pre>
  
██    ██ ███████  █████  ██████   ██████      █████  ██████  ██████   ██████ 
 ██    ██ ██      ██   ██ ██   ██ ██          ██   ██ ██   ██ ██   ██ ██    ██ 
 ██    ██ █████   ███████ ██████  ██          ███████ ██████  ██████  ██    ██ 
 ██    ██ ██      ██   ██ ██   ██ ██          ██   ██ ██   ██ ██   ██ ██    ██ 
██████  ██      ██   ██ ██████   ██████     ██   ██ ██   ██ ██████   ██████

</pre>

</div>
  
</pre>

<div align="center">
   <h1>🌳 UFABC ARBO</font></h1>
</div>

<div align="center">
  
<p><strong>RPG de texto para exploração do campus SA da UFABC</strong></p>

</div>

<hr>

<!-- ============================= -->
<!-- SOBRE -->
<!-- ============================= -->

<h2>📌 Sobre o Projeto </h2>

<p>
O <strong>UFABC ARBO</strong> é um jogo desenvolvido em Python para a disciplina de Processamento da Informação ministrada pelo Prof. Amaury Budri.
O projeto aplica conceitos fundamentais de programação, modelagem de dados e lógica computacional.
</p>

<p>
O jogador assume o papel de um estudante que percorre o campus de Santo andré da UFABC, 
descobrindo itens ocultos e interagindo com o ambiente para conseguir completar as missões.
</p>

<hr>

<!-- ============================= -->
<!-- OBJETIVO -->
<!-- ============================= -->

<h2>🎯 Objetivo do Projeto</h2>

<ul>
<li>Aplicar estruturas de dados na prática</li>
<li>Modelar um sistema baseado em grafos</li>
<li>Implementar persistência de dados com JSON</li>
<li>Desenvolver um sistema interativo via terminal</li>
<li>Promover maior integração da comunidade acadêmica</li>
</ul>

<hr>

<!-- ============================= -->
<!-- TECNOLOGIAS -->
<!-- ============================= -->

<h2>🧠 Tecnologias e Estruturas Utilizadas</h2>

<h3>🔹 Linguagem</h3>
<ul>
<li>Python 3</li>
</ul>

<h3>🔹 Bibliotecas</h3>
<ul>
<li><code>random</code> — inicialização e eventos</li>
<li><code>json</code> — persistência de dados</li>
<li><code>os</code> — manipulação de arquivos</li>
<li><code>pyfiglet</code> — geração de ASCII ART</li>
</ul>

<h3>🔹 Estruturas de Dados</h3>
<ul>
<li><strong>Dicionários</strong> → representação do grafo (ambientes e conexões)</li>
<li><strong>Listas</strong> → inventário, eventos e itens</li>
<li><strong>Variáveis globais</strong> → controle do estado do jogo</li>
<li><strong>Objetos estruturados</strong> → modelagem dos itens com atributos e regras</li>
</ul>

<hr>

<!-- ============================= -->
<!-- GRAFO -->
<!-- ============================= -->

<h2>🗺️ Modelagem do Espaço</h2>

<p>
O campus é representado como um <strong>grafo não-direcionado</strong>, utilizando lista de adjacência:
</p>

<pre>
conexoes = {
    1: [2,8,11,13],
    2: [1,3],
    3: [2,11,4],
    ...
}
</pre>

<hr>

<!-- ============================= -->
<!-- FUNCIONALIDADES -->
<!-- ============================= -->

<h2>🎮 Funcionalidades</h2>

<h3>✔️ Implementadas</h3>
<ul>
<li>Menu interativo</li>
<li>Navegação entre ambientes</li>
<li>Sistema de exploração</li>
<li>Sistema de itens com regras de descoberta</li>
<li>Inventário</li>
<li>Salvar e carregar jogo (JSON)</li>
<li>Reset do jogo</li>
<li>Interface com ASCII ART</li>
</ul>

<h3>🚧 Em desenvolvimento</h3>
<ul>
<li>Funcionalidades avançadas dos itens</li>
<li>Interações entre itens</li>
<li>Sistema de missões</li>
<li>Conclusão de missões</li>
</ul>

<hr>

<!-- ============================= -->
<!-- MECÂNICAS -->
<!-- ============================= -->

<h2>🧩 Mecânicas do Jogo</h2>

<h3>🔍 Exploração</h3>
<ul>
<li>Itens são inicialmente ocultos</li>
<li>Descoberta depende de ambiente e repetição do comando explorar</li>
<li>Progressão não-linear</li>
</ul>

<h3>🎒 Inventário</h3>
<ul>
<li>Itens podem ser coletáveis ou fixos</li>
<li>Itens coletados persistem entre sessões</li>
</ul>

<h3>🔐 Restrições</h3>
<ul>
<li>Ambientes com acesso condicionado</li>
<li>Regras específicas por item</li>
</ul>

<hr>

<!-- ============================= -->
<!-- DESAFIOS -->
<!-- ============================= -->

<h2>🧪 Desafios Técnicos</h2>

<ul>
<li>Gerenciamento de estado complexo</li>
<li>Persistência consistente com JSON</li>
<li>Lógica condicional por item</li>
<li>Modelagem espacial com grafos</li>
<li>Sistema de descoberta progressiva</li>
</ul>

<hr>

<!-- ============================= -->
<!-- CONTRIBUIÇÃO -->
<!-- ============================= -->

<h2>🤝 Contribuições são bem-vindas!</h2>
