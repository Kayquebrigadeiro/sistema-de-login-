# Sistema de Login Flask

Sistema de autenticação completo desenvolvido em Flask com interface moderna e funcionalidades de segurança.

## 🚀 Funcionalidades

- ✅ Registro de usuários
- ✅ Login/Logout seguro
- ✅ Hash de senhas com bcrypt
- ✅ Bloqueio por tentativas excessivas
- ✅ Recuperação de senha
- ✅ Interface responsiva e moderna
- ✅ Validação de dados

## 🛠️ Tecnologias

- **Flask** - Framework web
- **bcrypt** - Hash de senhas
- **JSON** - Armazenamento de dados
- **HTML/CSS** - Interface moderna

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd flask-auth-json
```

2. Instale as dependências:
```bash
pip install -r requisitos.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse: `http://127.0.0.1:5000`

## 🔧 Configuração

- Altere a `secret_key` em produção
- Configure variáveis de ambiente para dados sensíveis
- Ajuste as configurações de bloqueio conforme necessário

## 📁 Estrutura

```
flask-auth-json/
├── app.py              # Aplicação principal
├── utils.py            # Funções utilitárias
├── requisitos.txt      # Dependências
├── user.json          # Dados dos usuários
└── templates/         # Templates HTML
    ├── base.html
    ├── login.html
    ├── registro.html
    ├── dashboard.html
    └── recuperar-*.html
```

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- Proteção contra força bruta
- Validação de entrada
- Sessões seguras

## 📝 Licença

MIT License