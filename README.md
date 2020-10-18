# Pizzaria Hortência
**Pizzaria Hortência** se trata de um projeto desenvolvido durante o shehacks com o objetivo de melhorar a qualidade de vida de pessoas em situação de violência doméstica por todo Brasil, sobretudo, de mulheres.

Se passando de uma pizzaria comum, seu intuito é ser um botão de emergência escondido para que, dado um cenário de risco, uma comunicação indireta com contatos de segurança da vítima possa ser estabelecida

# Instruções de Uso
[Botar o link para o video aqui](linkparaovideo.com)

Para poder acessar o chat com o bot [clique aqui](https://t.me/PizzaHortaBot)

# Como colaborar
O projeto está completamente aberto para colaborações de terceiros, para isso basta contatar alguma das colaboradora ou, ainda, abrir um pull request utilizando a própria plataforma do github

# Problemas e ideias a serem implementadas

## Interpretador de aúdio
Já temos um arquivo que transcreve audios enviados pelo telegram, mas para tornar o módulo completamente funcional, seria necessário ter algum tipo de interprete para associar certas palavras com pedidos de ajuda

## Servidor
Atualmente, o bot roda no servidor local, mas a intenção é passar isso para o `heroku` assim que possível

## Banco de dados
Durante a hackton, devido a falta de tempo, a maneira que encontramos para lidar com os dados dos usuários cadastrados foi um simles arquivo json. Dito isso, seria necessário implementar algum banco de dados, de preferência não relacional, como MongoBD para que se torne viável hostear o bot em algum servidor online

## Mudanças nos temas
Para evitar a previsibilidade e/ou aproveitamento do bot por uma pessoa má intencionada, pretendemos fazer mudanças sazonais no bot. Um possível exemplo disso seria a mudança de uma pizzaria para uma hamburgueria.
