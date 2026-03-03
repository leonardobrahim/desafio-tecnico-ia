# Notas de Engenharia de Prompt

Este documento detalha as estratégias e técnicas de engenharia de prompt aplicadas no desenvolvimento desta plataforma educativa, visando maximizar a qualidade e a personalização do conteúdo gerado.

## Persona Prompting

Em todas as gerações, a IA assume um papel específico antes de receber as instruções.

**Exemplo Prático:** Utilizamos "Você é um professor experiente em Pedagogia" para a explicação conceitual e "Você é um tutor socrático" para as perguntas de reflexão.
**Justificativa:** Isso ancora o modelo linguístico em um espaço latente focado em educação, garantindo que o tom de voz, o vocabulário e a didática sejam adequados à tarefa, reduzindo alucinações.

## Context Setting (Injeção de Contexto)

Os prompts não são estáticos. Eles recebem as variáveis do perfil do aluno (idade, nível de conhecimento e estilo de aprendizado) dinamicamente.

**Justificativa:** Sem essa injeção, a IA geraria uma explicação de "Fotossíntese" igual para uma criança de 10 anos e um adulto de 25. O contexto força a adaptação lexical e estrutural do output.

## Chain-of-Thought (Cadeia de Pensamento)

Em vez de solicitar o resultado final diretamente, instruímos a IA a pensar "passo a passo".

**Exemplo Prático:** Na geração de perguntas de reflexão, o prompt pede: "pense passo a passo: avalie o nível do aluno, identifique dilemas e então elabore as perguntas".
**Justificativa:** Forçar o modelo a processar o racracínio intermediário antes de entregar a resposta final diminui drasticamente o erro lógico e aumenta a profundidade das respostas geradas.

## Output Formatting (Formatação Estrita)

Para garantir a integração sistêmica, os prompts exigem um formato de saída estrito.

**Exemplo Prático:** "Retorne APENAS um objeto JSON válido com a chave "explicacao_conceitual"..."
**Justificativa:** Como o sistema depende da persistência e leitura de dados estruturados via código (Python), respostas conversacionais quebrariam a aplicação. Esta técnica garante a previsibilidade do retorno.
