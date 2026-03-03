import json
import os
import time
import api_client
import prompt_engine

def carregar_perfis():
    # Carrega os perfis dos alunos do arquivo JSON.
    try:
        with open('profiles.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados.get('alunos', [])
    except FileNotFoundError:
        print("Erro: Arquivo profiles.json não encontrado.")
        return []

def limpar_resposta_json(texto):
    # Remove marcações Markdown que a IA costuma adicionar.
    texto_limpo = texto.strip()
    if texto_limpo.startswith("```json"):
        texto_limpo = texto_limpo[7:]
    elif texto_limpo.startswith("```"):
        texto_limpo = texto_limpo[3:]
    
    if texto_limpo.endswith("```"):
        texto_limpo = texto_limpo[:-3]
        
    return texto_limpo.strip()

def salvar_resultado(aluno_nome, tipo_conteudo, topico, conteudo_ia):
    # Salva a resposta em um arquivo JSON estruturado com timestamp.
    os.makedirs('samples', exist_ok=True)
    timestamp = int(time.time())
    
    # Formata o nome do arquivo para não ter espaços ou caracteres estranhos
    nome_seguro = aluno_nome.lower().replace(" ", "_")
    tipo_seguro = tipo_conteudo.lower().replace(" ", "_")
    nome_arquivo = f"samples/resultado_{nome_seguro}_{tipo_seguro}_{timestamp}.json"

    # Tenta converter o texto da IA para um dicionário Python real
    try:
        texto_json_limpo = limpar_resposta_json(conteudo_ia)
        dados_ia = json.loads(texto_json_limpo)
    except json.JSONDecodeError:
        print("\n*AVISO* A IA não retornou um JSON perfeito. Salvando como texto bruto para análise.")
        dados_ia = {"texto_bruto": conteudo_ia}

    dados_finais = {
        "metadata": {
            "aluno": aluno_nome,
            "topico": topico,
            "tipo_conteudo": tipo_conteudo,
            "timestamp": timestamp
        },
        "conteudo_gerado": dados_ia
    }

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False, indent=4)
    
    print(f"\n*SUCESSO* Conteúdo salvo em: {nome_arquivo}")

def main():
    alunos = carregar_perfis()
    if not alunos:
        return

    while True:
        print("\n" + "="*40)
        print(" PLATAFORMA EDUCATIVA - GERADOR IA ")
        print("="*40)
        
        # Seleciona Aluno
        print("\nEscolha um aluno:")
        for i, aluno in enumerate(alunos):
            print(f"{i+1}. {aluno['nome']} ({aluno['idade']} anos, {aluno['nivel_conhecimento']})")
        print("0. Sair")
        
        escolha_aluno = input("\nOpção: ")
        if escolha_aluno == '0':
            break
            
        try:
            aluno_selecionado = alunos[int(escolha_aluno) - 1]
        except (ValueError, IndexError):
            print("Opção inválida.")
            continue

        # Define Tópico
        topico = input("\nDigite o tópico a ser ensinado (ex: Fotossíntese, Segunda Guerra, Python): ")
        if not topico.strip():
            print("O tópico não pode ser vazio.")
            continue

        # Seleciona Tipo de Conteúdo
        print("\nEscolha o tipo de conteúdo a gerar:")
        print("1. Explicação Conceitual")
        print("2. Exemplos Práticos")
        print("3. Perguntas de Reflexão")
        print("4. Resumo Visual (Diagrama ASCII)")
        
        escolha_tipo = input("\nOpção: ")
        
        prompt = ""
        tipo_nome = ""

        if escolha_tipo == '1':
            prompt = prompt_engine.gerar_prompt_explicacao_conceitual(aluno_selecionado, topico)
            tipo_nome = "Explicacao_Conceitual"
        elif escolha_tipo == '2':
            prompt = prompt_engine.gerar_prompt_exemplos_praticos(aluno_selecionado, topico)
            tipo_nome = "Exemplos_Praticos"
        elif escolha_tipo == '3':
            prompt = prompt_engine.gerar_prompt_perguntas_reflexao(aluno_selecionado, topico)
            tipo_nome = "Perguntas_Reflexao"
        elif escolha_tipo == '4':
            prompt = prompt_engine.gerar_prompt_resumo_visual(aluno_selecionado, topico)
            tipo_nome = "Resumo_Visual"
        else:
            print("Opção inválida.")
            continue

        # Executa e Salva
        print(f"\nGerando '{tipo_nome}' para {aluno_selecionado['nome']} sobre '{topico}'...")
        resposta = api_client.chamar_api_gemini(prompt)
        
        salvar_resultado(aluno_selecionado['nome'], tipo_nome, topico, resposta)

if __name__ == "__main__":
    main()