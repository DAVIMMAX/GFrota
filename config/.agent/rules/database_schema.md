Aqui está a estrutura completa e revisada, já formatada em Markdown e otimizada com instruções claras de contexto para o agente do Antigravity entender perfeitamente o seu ecossistema. 

Você pode copiar todo o bloco abaixo e colar diretamente no seu arquivo de regras (ex: `.agent/rules/database_schema.md`):

```markdown
# Regra de Contexto: Estrutura do Banco de Dados do GFrota

Sempre que for criar um Model, View, Form ou Query no Django, utilize estritamente a seguinte estrutura de tabelas e relacionamentos. Não invente colunas que não estão listadas aqui. Compreenda que a tabela 'Usuário' deve estender o AbstractUser do Django.

## 1. Bloco de Efetivo e Instituição

**Órgãos**
- ID (PK)
- Órgão (CharField)

**Roles** (Papéis de Acesso ao Sistema)
- ID (PK)
- Role (CharField)

**Funções** (Papéis Operacionais na Escala)
- ID (PK)
- Nome_Função (CharField - Ex: Motorista, Comandante, Operador)

**Usuário** (Modelo Customizado - AbstractUser)
- ID (PK)
- Nome Completo (CharField)
- CPF (CharField)
- Matrícula (CharField)
- nº de Ordem (IntegerField/CharField)
- Nome de Guerra (CharField)
- Foto (ImageField)
- Cargo (CharField - Vínculo administrativo. Ex: 3º Sargento, Agente Administrativo)
- Órgão_ID (FK -> Órgãos)
- Role_ID (FK -> Roles)
- *Relacionamento:* Possui Many-to-Many nativo com "Funções" (gera a tabela intermediária "Usuários_Funções").

**Usuários_Funções** (Tabela Intermediária M2M gerada pelo Django)
- ID (PK)
- ID_Usuário (FK -> Usuário)
- ID_Função (FK -> Funções)

---

## 2. Bloco de Ativos (Frota e Comunicação)

**Status_Viaturas**
- ID (PK)
- Status (CharField)

**Viatura**
- ID (PK)
- Placa (CharField)
- Modelo (CharField)
- Prefixo (CharField)
- Foto (ImageField)
- Status_Viatura_ID (FK -> Status_Viaturas)

**Tipo_Radio**
- ID (PK)
- Tipo (CharField)

**Radio**
- ID (PK)
- Prefixo (CharField)
- Tipo_Radio_ID (FK -> Tipo_Radio)

**Aeronave**
- ID (PK)
- Prefixo (CharField)
- Recurso (CharField)
- Radio_ID (FK -> Radio)

---

## 3. Bloco Operacional (Escala, Vôos e Ocorrências)

**Apresentação** (O Serviço/Turno Base)
- ID (PK)
- Viatura_ID (FK -> Viatura, null=True, blank=True)
- Aeronave_ID (FK -> Aeronave, null=True, blank=True)
- Turno (CharField/TextChoices)
- Horário_Inicial (DateTimeField/TimeField)
- Horário_Final (DateTimeField/TimeField, null=True, blank=True)
- Observação (TextField)
- *Relacionamento:* Possui Many-to-Many nativo com "Usuário" para definir a guarnição/equipe (gera a tabela intermediária "Apresentação_Usuários").

**Apresentação_Usuários** (Tabela Intermediária M2M gerada pelo Django)
- ID (PK)
- ID_Apresentação (FK -> Apresentação)
- ID_Usuário (FK -> Usuário)

**Vôos**
- ID (PK)
- Data (DateField)
- Hora (TimeField)
- Destino (CharField)
- Aeronave_ID (FK -> Aeronave)
- Apresentação_ID (FK -> Apresentação)
- Hora_Retorno (TimeField/DateTimeField, null=True, blank=True)

**Ocorrência**
- ID (PK)
- Tipo_Ocorrência (CharField)
- Data_Ocorrência (DateField)
- Hora_Ocorrência (TimeField)
- Apresentação_ID (FK -> Apresentação)
- Observação (TextField)
```
