# Plataforma Educativa - Gerador de Conteúdo com IA

Uma plataforma em linha de comando (CLI) que utiliza Inteligência Artificial e técnicas avançadas de Engenharia de Prompt para gerar materiais educativos altamente personalizados com base no perfil do aluno.

## 🚀 Requisitos e Setup

**Clone o repositório:**

```bash
git clone https://github.com/leonardobrahim/desafio-tecnico-ia.git
cd projeto-ia
```

**Crie um ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv venv
source venv/bin/activate # (Linux/Mac) ou venv\Scripts\activate (Windows)
```

**Instale as dependências:**

```Bash
pip install -r requirements.txt
```

**Configuração de API:**

Renomeie o arquivo .env.example para .env.

Insira a sua chave de API do Google Gemini na variável GEMINI_API_KEY.

## 💻 Como Usar

Execute o arquivo principal:

```Bash
python main.py
```

Siga o menu interativo no terminal para selecionar um aluno, definir um tópico e gerar o conteúdo. Os resultados serão salvos automaticamente na pasta /samples em formato JSON.

## 🧠 Engenharia de Prompt

As técnicas detalhadas de elaboração de prompts (Persona, Context Setting, Chain-of-Thought e Output Formatting) estão documentadas no arquivo PROMPT_ENGINEERING_NOTES.md.
