from flask import Flask, render_template, request, jsonify
import json
import os
import time
import api_client
import prompt_engine

app = Flask(__name__)

def carregar_perfis():
    try:
        with open('profiles.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados.get('alunos', [])
    except FileNotFoundError:
        return []

def limpar_resposta_json(texto):
    inicio = texto.find('{')
    fim = texto.rfind('}')
    
    if inicio != -1 and fim != -1:
        return texto[inicio:fim+1]
    
    return texto.strip()

def salvar_resultado(aluno_nome, tipo_conteudo, topico, conteudo_ia):
    os.makedirs('samples', exist_ok=True)
    timestamp = int(time.time())
    
    nome_seguro = aluno_nome.lower().replace(" ", "_")
    tipo_seguro = tipo_conteudo.lower().replace(" ", "_")
    nome_arquivo = f"samples/resultado_{nome_seguro}_{tipo_seguro}_{timestamp}.json"

    try:
        texto_json_limpo = limpar_resposta_json(conteudo_ia)
        dados_ia = json.loads(texto_json_limpo)
    except json.JSONDecodeError:
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
        
    return dados_ia

@app.route('/')
def index():
    alunos = carregar_perfis()
    return render_template('index.html', alunos=alunos)

@app.route('/gerar', methods=['POST'])
def gerar_conteudo():
    dados = request.json
    aluno_id = int(dados.get('aluno_id'))
    topico = dados.get('topico')
    tipo_conteudo = dados.get('tipo_conteudo')

    alunos = carregar_perfis()
    aluno_selecionado = next((a for a in alunos if a['id'] == aluno_id), None)

    if not aluno_selecionado or not topico:
        return jsonify({"erro": "Dados inválidos"}), 400

    prompt = ""
    if tipo_conteudo == '1':
        prompt = prompt_engine.gerar_prompt_explicacao_conceitual(aluno_selecionado, topico)
        tipo_nome = "Explicacao_Conceitual"
    elif tipo_conteudo == '2':
        prompt = prompt_engine.gerar_prompt_exemplos_praticos(aluno_selecionado, topico)
        tipo_nome = "Exemplos_Praticos"
    elif tipo_conteudo == '3':
        prompt = prompt_engine.gerar_prompt_perguntas_reflexao(aluno_selecionado, topico)
        tipo_nome = "Perguntas_Reflexao"
    elif tipo_conteudo == '4':
        prompt = prompt_engine.gerar_prompt_resumo_visual(aluno_selecionado, topico)
        tipo_nome = "Resumo_Visual"
    else:
        return jsonify({"erro": "Tipo de conteúdo inválido"}), 400

    resposta_bruta = api_client.chamar_api_gemini(prompt)
    dados_ia = salvar_resultado(aluno_selecionado['nome'], tipo_nome, topico, resposta_bruta)

    return jsonify({"sucesso": True, "dados": dados_ia})

if __name__ == '__main__':
    app.run(debug=True)