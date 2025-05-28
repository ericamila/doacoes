# Instruções para Configuração e Teste do Sistema de Notificações por Email

Este documento detalha os passos para configurar e testar o sistema de notificações por email para propostas no projeto Doacoes.

## 1. Arquivos Criados/Modificados

Os seguintes arquivos foram criados ou modificados para implementar as notificações:

1.  **`proposals/email_utils.py`**: Contém as funções para buscar representantes e enviar emails.
2.  **`proposals/views.py`**: Integração das chamadas de notificação nos eventos de criação de proposta e remoção de aceite.
3.  **`proposals/templates/emails/new_proposal_pending.html`**: Template de email para nova proposta pendente.
4.  **`proposals/templates/emails/deadline_approaching.html`**: Template de email para prazo de aceite se aproximando.
5.  **`proposals/templates/emails/acceptance_removed.html`**: Template de email para aceite removido.
6.  **`proposals/management/commands/notificar_prazos_aceite.py`**: Comando de gerenciamento para verificar e notificar sobre prazos de aceite próximos.

## 2. Estrutura de Diretórios

Certifique-se de que a seguinte estrutura de diretórios exista em seu app `proposals`:

```
proposals/
├── management/
│   └── commands/
│       └── notificar_prazos_aceite.py
├── templates/
│   └── emails/
│       ├── new_proposal_pending.html
│       ├── deadline_approaching.html
│       └── acceptance_removed.html
├── email_utils.py
├── views.py
└── ... (outros arquivos do app)
```

## 3. Configuração do Ambiente (`settings.py`)

Adicione ou modifique as seguintes configurações no seu arquivo `settings.py`:

```python
# Configurações de Email (Exemplo usando Gmail - ajuste para seu provedor)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "seu_email@gmail.com"  # Seu endereço de email
EMAIL_HOST_PASSWORD = "sua_senha_de_app"  # Use senha de aplicativo se usar Gmail com 2FA
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER # Email que aparecerá como remetente

# URL Base do Site (Usada nos links dos emails)
# Certifique-se de que esta URL esteja correta para o seu ambiente
SITE_URL = "http://localhost:8000" # Ou o domínio de produção
```

**Importante**: 
*   Substitua as credenciais de email pelas suas.
*   Se usar Gmail com autenticação de dois fatores (2FA), você precisará gerar uma "Senha de aplicativo".
*   Ajuste `SITE_URL` para a URL correta onde seu sistema está acessível.

## 4. Testando as Notificações

### 4.1. Notificação de Nova Proposta Pendente

1.  Crie um usuário do tipo "Representante de Município" (tipo_usuario=1), situação "Ativo" (situacao=0), associado a um município específico e com um email válido cadastrado.
2.  Crie uma nova proposta (`Proposal`) associada a este mesmo município.
3.  Após salvar a proposta, o representante associado deve receber um email baseado no template `new_proposal_pending.html`.

### 4.2. Notificação de Aceite Removido

1.  Registre a ciência (`ciente=True`) em uma proposta existente que tenha um representante associado ao município.
2.  Como administrador, utilize a funcionalidade para remover a ciência (`remover_ciencia`).
3.  Após remover a ciência, o representante associado deve receber um email baseado no template `acceptance_removed.html`.

### 4.3. Notificação de Prazo Próximo (Comando Manual)

Como tarefas agendadas não estão disponíveis neste ambiente, você precisará executar um comando manualmente para verificar os prazos.

1.  Certifique-se de que existam propostas com `ciente=False` e cuja data final de aceite (`Project.data_final_ciencia`) esteja próxima (por exemplo, nos próximos 7 dias).
2.  Execute o seguinte comando no terminal, na pasta raiz do seu projeto Django:
    ```bash
    python manage.py notificar_prazos_aceite --days=7 
    ```
    (Você pode ajustar o número de dias com o parâmetro `--days`)
3.  Os representantes dos municípios das propostas encontradas devem receber um email baseado no template `deadline_approaching.html`.

## 5. Solução de Problemas

*   **Emails não chegam**: Verifique as configurações de SMTP em `settings.py`, as credenciais, e se o firewall ou antivírus não está bloqueando a conexão. Verifique a pasta de spam.
*   **Erro no comando `notificar_prazos_aceite`**: Verifique os logs do Django para mensagens de erro. Certifique-se de que os modelos e relacionamentos estão corretos.
*   **Links quebrados nos emails**: Verifique a configuração `SITE_URL` em `settings.py`.
*   **Templates não encontrados**: Confirme se a estrutura de diretórios dos templates está correta.

Por favor, siga estas instruções para configurar e testar o sistema de notificações em seu ambiente.
