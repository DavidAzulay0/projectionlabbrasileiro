-- Base de dados relacional para simulação financeira de casal estilo ProjectionLab (versão MVP atualizada)
-- Autor: David Azulay + ChatGPT

-- TABELA 1: Anos da simulação
CREATE TABLE Anos (
    id INTEGER PRIMARY KEY,
    ano INTEGER NOT NULL
);

-- TABELA 2: Eventos de Vida (alteram premissas)
CREATE TABLE EventosDeVida (
    id INTEGER PRIMARY KEY,
    ano_id INTEGER REFERENCES Anos(id),
    descricao TEXT,
    tipo_evento TEXT CHECK(tipo_evento IN ('entrada', 'saida', 'bem')),
    alvo_id INTEGER, -- ID na tabela de destino (Entrada, Saída, Bem)
    efeito TEXT -- ex: 'on', 'off', 'aumentar_25%', 'trocar_valor'
);

-- TABELA 3: Objetivos Financeiros
CREATE TABLE ObjetivosFinanceiros (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    prioridade INTEGER, -- quanto menor, mais prioritário
    tipo_alocacao TEXT CHECK(tipo_alocacao IN ('maximizacao', 'alocacao_parcial')),
    percentual_alocacao REAL DEFAULT NULL, -- usado se tipo_alocacao = 'alocacao_parcial'
    valor_necessario REAL,
    valor_acumulado REAL DEFAULT 0
);

-- TABELA 4: Entradas
CREATE TABLE Entradas (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    valor_anual REAL,
    fonte TEXT, -- opcional: parceiro1, parceiro2, casal
    ativo BOOLEAN DEFAULT TRUE
);

-- TABELA 5: Saídas
CREATE TABLE Saidas (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    valor_anual REAL,
    tipo TEXT, -- ex: moradia, transporte, filhos
    ativo BOOLEAN DEFAULT TRUE
);

-- TABELA 6: Bens (ativos financeiros ou reais)
CREATE TABLE Bens (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    tipo TEXT CHECK(tipo IN ('imovel', 'reserva_emergencia', 'investimento', 'divida')),
    valor REAL,
    rendimento_esperado REAL, -- usado para investimentos
    passivo BOOLEAN DEFAULT FALSE, -- usado para diferenciar ativo vs passivo
    ativo BOOLEAN DEFAULT TRUE
);

-- TABELA 7: Montantes Financeiros por Ano
CREATE TABLE MontantesFinanceiros (
    id INTEGER PRIMARY KEY,
    ano_id INTEGER REFERENCES Anos(id),
    entrada_total REAL,
    saida_total REAL,
    impostos REAL,
    saldo_ano REAL,
    patrimonio_liquido REAL,
    divida_total REAL,
    valor_investido REAL,
    reserva_emergencia REAL,
    entrada_casa_propria REAL
);

-- TABELA 8: Alocação para Objetivos (por ano)
CREATE TABLE AlocacaoObjetivos (
    id INTEGER PRIMARY KEY,
    ano_id INTEGER REFERENCES Anos(id),
    objetivo_id INTEGER REFERENCES ObjetivosFinanceiros(id),
    valor_alocado REAL
);

-- TABELA 9: Premissas Gerais (crescimento e taxas)
CREATE TABLE PremissasGerais (
    id INTEGER PRIMARY KEY,
    ano_inicial INTEGER,
    taxa_inflacao REAL,
    taxa_crescimento_entradas REAL,
    taxa_crescimento_saidas REAL,
    taxa_juros_dividas REAL,
    taxa_rendimento_investimentos REAL
    
);
ALTER TABLE Premissas ADD COLUMN ativo INTEGER DEFAULT 1;

