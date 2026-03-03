def gerar_prompt_explicacao_conceitual(aluno, topico):
    # Persona Prompting
    persona = "Você é um professor experiente em Pedagogia, especialista em adaptar conteúdos complexos de forma didática e acessível."
    
    # Context Setting
    contexto = f"O aluno se chama {aluno['nome']}, tem {aluno['idade']} anos. Seu nível de conhecimento no assunto é {aluno['nivel_conhecimento']} e seu estilo de aprendizado é predominantemente {aluno['estilo_aprendizado']}."
    
    # Chain-of-Thought
    cot = f"Para ensinar o tópico '{topico}', pense passo a passo: primeiro identifique os conceitos base necessários para essa idade, depois conecte com o estilo de aprendizado do aluno e, por fim, elabore a explicação."
    
    # Output Formatting
    formato = "Retorne apenas um objeto JSON válido com a chave 'explicacao_conceitual' contendo o texto final."
    
    prompt = f"{persona}\n\nContexto do Aluno: {contexto}\n\nInstruções: {cot}\n\nFormato de Saída: {formato}"
    
    return prompt

def gerar_prompt_exemplos_praticos(aluno, topico):
    persona = "Você é um professor especialista em criar analogias precisas e exemplos do mundo real."
    contexto = f"O aluno {aluno['nome']} tem {aluno['idade']} anos. Seu nível é {aluno['nivel_conhecimento']}."
    
    # Contextualização estrita focada na idade
    instrucao = f"Crie 3 exemplos práticos sobre o tópico '{topico}'. Os exemplos devem ser estritamente baseados na realidade de uma pessoa de {aluno['idade']} anos, garantindo que a linguagem seja apropriada para o nível {aluno['nivel_conhecimento']}."
    formato = "Retorne APENAS um objeto JSON válido com a chave \"exemplos\" contendo uma lista de strings."
    
    return f"{persona}\n\nContexto: {contexto}\n\nInstrução: {instrucao}\n\nFormato: {formato}"

def gerar_prompt_perguntas_reflexao(aluno, topico):
    persona = "Você é um tutor socrático, focado em desenvolver o pensamento crítico profundo dos seus alunos."
    contexto = f"O aluno é nível {aluno['nivel_conhecimento']} e prefere aprender de forma {aluno['estilo_aprendizado']}."
    
    # Chain-of-Thought voltada para formulação de problemas
    cot = f"Para o tópico '{topico}', pense passo a passo: avalie o nível {aluno['nivel_conhecimento']} do aluno, identifique os maiores dilemas ou contra-sensos deste tópico, e então elabore 2 perguntas abertas que o forcem a refletir criticamente sobre o assunto em vez de apenas memorizar."
    formato = "Retorne APENAS um objeto JSON válido com a chave \"perguntas\" contendo uma lista de strings."
    
    return f"{persona}\n\nContexto: {contexto}\n\nInstrução: {cot}\n\nFormato: {formato}"

def gerar_prompt_resumo_visual(aluno, topico):
    persona = "Você é um designer instrucional e professor especializado em síntese de informações."
    contexto = f"O aluno {aluno['nome']} possui estilo de aprendizado {aluno['estilo_aprendizado']}."
    
    # Output Formating estrito para Arte/Diagrama ASCII
    instrucao = f"Crie um resumo visual em formato de diagrama ASCII ou mapa mental sobre o tópico '{topico}'. A complexidade da estrutura deve respeitar o fato de o aluno ter nível {aluno['nivel_conhecimento']}."
    formato = "Retorne APENAS um objeto JSON válido com a chave \"diagrama_ascii\" contendo a representação visual em formato de string (use caracteres como | - + para formar o desenho)."
    
    return f"{persona}\n\nContexto: {contexto}\n\nInstrução: {instrucao}\n\nFormato: {formato}"