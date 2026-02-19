import pandas as pd
import numpy as np
import warnings

warnings.simplefilter("ignore")

arquivo_excel = 'BASEDEDADOSPEDE2024-DATATHON.xlsx'
print(f"🔄 Lendo arquivo: {arquivo_excel}")

try:
    xls = pd.ExcelFile(arquivo_excel)
    abas = xls.sheet_names
    aba_22 = next(s for s in abas if '2022' in s)
    aba_23 = next(s for s in abas if '2023' in s)
    aba_24 = next(s for s in abas if '2024' in s)
    
    df_2022 = pd.read_excel(xls, sheet_name=aba_22)
    df_2023 = pd.read_excel(xls, sheet_name=aba_23)
    df_2024 = pd.read_excel(xls, sheet_name=aba_24)
except Exception as e:
    print(f"❌ Erro ao ler Excel: {e}")
    exit()

def processar_ano(df_orig, ano):
    df_orig.columns = df_orig.columns.str.strip()
    df_novo = pd.DataFrame()
    df_novo['ANO'] = [ano] * len(df_orig) # Mantemos como número para ordenar o histórico
    
    # PEGAR A COLUNA RA (Nosso ID Único)
    if 'RA' in df_orig.columns:
        df_novo['RA'] = df_orig['RA']
    else:
        df_novo['RA'] = np.nan
        
    # Mapeamento
    if ano == 2022:
        mapa = {'INDE 22': 'INDE', 'Pedra 22': 'PEDRA', 'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN'}
    elif ano == 2023:
        mapa = {'INDE 2023': 'INDE', 'Pedra 2023': 'PEDRA', 'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN', 'IPP': 'IPP'}
    elif ano == 2024:
        mapa = {'INDE 2024': 'INDE', 'Pedra 2024': 'PEDRA', 'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN', 'IPP': 'IPP'}
    
    for col_orig, col_dest in mapa.items():
        if col_orig in df_orig.columns:
            df_novo[col_dest] = df_orig[col_orig]
        else:
            col_encontrada = next((c for c in df_orig.columns if c.lower() == col_orig.lower()), None)
            if col_encontrada:
                df_novo[col_dest] = df_orig[col_encontrada]
            else:
                df_novo[col_dest] = 0.0
    
    if 'IPP' not in df_novo.columns: df_novo['IPP'] = 0.0

    cols_numericas = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
    for col in cols_numericas:
        if df_novo[col].dtype == 'object':
             df_novo[col] = df_novo[col].astype(str).str.replace(',', '.')
        df_novo[col] = pd.to_numeric(df_novo[col], errors='coerce').fillna(0)

    if 'PEDRA' not in df_novo.columns:
         df_novo['PEDRA'] = 'Não Informado'
    else:
         df_novo['PEDRA'] = df_novo['PEDRA'].fillna('Não Informado').astype(str)

    return df_novo

print("🛠️ Processando dados base...")
df_22_ok = processar_ano(df_2022, 2022)
df_23_ok = processar_ano(df_2023, 2023)
df_24_ok = processar_ano(df_2024, 2024)

df_total = pd.concat([df_22_ok, df_23_ok, df_24_ok], ignore_index=True)

# ==========================================
# INÍCIO DA SUA LÓGICA DE FEATURES AVANÇADAS
# ==========================================
print("📈 Gerando features de evolução histórica (Deltas e Tendências)...")

# 1. Ordenar por Aluno (RA) e Ano para calcular as diferenças corretamente
df_total = df_total.sort_values(by=['RA', 'ANO'])

features_chave = ['IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN', 'INDE']

for feature in features_chave:
    # LAG: Qual era o valor no ano anterior?
    df_total[f'{feature}_AnoAnterior'] = df_total.groupby('RA')[feature].shift(1)
    
    # DELTA: Quanto variou do ano passado para cá?
    df_total[f'Delta_{feature}'] = df_total[feature] - df_total[f'{feature}_AnoAnterior']
    
    # TENDÊNCIA: Variação percentual
    df_total[f'Tendencia_{feature}'] = (df_total[feature] - df_total[f'{feature}_AnoAnterior']) / (df_total[f'{feature}_AnoAnterior'] + 0.01)

# Tratamento de Nulos gerados (Ex: o primeiro ano do aluno não tem ano anterior)
# Preenchemos com 0 assumindo que não houve variação no primeiro registro
df_total = df_total.fillna(0)

# Criar Target (Ponto de Virada)
pedras_ruins = ['Quartzo', 'Ágata', '#NULO!', 'nan', '0', '0.0', 'Não Informado']
df_total['Ponto_Virada'] = df_total['PEDRA'].apply(lambda x: 0 if x in pedras_ruins else 1)

# Salvar
df_total.to_csv('dados_unificados.csv', index=False)

print("\n✅ SUCESSO! Base enriquecida com histórico.")
# Mostrando algumas das novas colunas para confirmar
print("Algumas das novas colunas:", [c for c in df_total.columns if 'Delta' in c][:5])