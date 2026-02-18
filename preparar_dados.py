import pandas as pd
import numpy as np
import warnings

# Ignorar avisos irrelevantes
warnings.simplefilter("ignore")

arquivo_excel = 'BASEDEDADOSPEDE2024-DATATHON.xlsx'
print(f"🔄 Lendo arquivo: {arquivo_excel}")

try:
    xls = pd.ExcelFile(arquivo_excel)
    abas = xls.sheet_names
    
    # Busca das abas
    aba_22 = next(s for s in abas if '2022' in s)
    aba_23 = next(s for s in abas if '2023' in s)
    aba_24 = next(s for s in abas if '2024' in s)
    
    print(f"   Abas encontradas: {aba_22}, {aba_23}, {aba_24}")
    
    df_2022 = pd.read_excel(xls, sheet_name=aba_22)
    df_2023 = pd.read_excel(xls, sheet_name=aba_23)
    df_2024 = pd.read_excel(xls, sheet_name=aba_24)
    
except Exception as e:
    print(f"❌ Erro crítico ao ler Excel: {e}")
    exit()

def processar_ano(df_orig, ano):
    # 1. Limpar nomes das colunas (tira espaços extras)
    df_orig.columns = df_orig.columns.str.strip()
    
    # 2. Criar novo DataFrame limpo apenas com o que precisamos
    # Isso evita conflito com colunas duplicadas ou históricas
    df_novo = pd.DataFrame()
    df_novo['ANO'] = [str(ano)] * len(df_orig)
    
    # 3. Mapeamento manual exato para cada ano
    # (Nome na planilha) -> (Nome final no sistema)
    if ano == 2022:
        mapa = {
            'INDE 22': 'INDE', 'Pedra 22': 'PEDRA',
            'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 
            'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN'
            # 2022 não tem IPP
        }
    elif ano == 2023:
        mapa = {
            'INDE 2023': 'INDE', 'Pedra 2023': 'PEDRA',
            'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 
            'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN', 'IPP': 'IPP'
        }
    elif ano == 2024:
        mapa = {
            'INDE 2024': 'INDE', 'Pedra 2024': 'PEDRA',
            'IAA': 'IAA', 'IEG': 'IEG', 'IPS': 'IPS', 
            'IDA': 'IDA', 'IPV': 'IPV', 'IAN': 'IAN', 'IPP': 'IPP'
        }
    
    # 4. Preencher as colunas
    for col_orig, col_dest in mapa.items():
        if col_orig in df_orig.columns:
            df_novo[col_dest] = df_orig[col_orig]
        else:
            # Tenta procurar ignorando maiúsculas/minúsculas
            col_encontrada = next((c for c in df_orig.columns if c.lower() == col_orig.lower()), None)
            if col_encontrada:
                df_novo[col_dest] = df_orig[col_encontrada]
            else:
                df_novo[col_dest] = 0.0 # Se não achar, preenche com 0
    
    # Garante que IPP existe em 2022 (preenchendo com 0)
    if 'IPP' not in df_novo.columns:
        df_novo['IPP'] = 0.0

    # 5. Tratamento numérico (Vírgula -> Ponto)
    cols_numericas = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
    
    for col in cols_numericas:
        # Se for texto, troca vírgula por ponto
        if df_novo[col].dtype == 'object':
             df_novo[col] = df_novo[col].astype(str).str.replace(',', '.')
        
        # Converte para número, forçando erros a virarem NaN (depois 0)
        df_novo[col] = pd.to_numeric(df_novo[col], errors='coerce').fillna(0)

    # 6. Tratamento da coluna PEDRA
    if 'PEDRA' not in df_novo.columns:
         df_novo['PEDRA'] = 'Não Informado'
    else:
         df_novo['PEDRA'] = df_novo['PEDRA'].fillna('Não Informado').astype(str)

    return df_novo

print("🛠️ Processando dados...")
df_22_ok = processar_ano(df_2022, 2022)
df_23_ok = processar_ano(df_2023, 2023)
df_24_ok = processar_ano(df_2024, 2024)

# Unificar
df_final = pd.concat([df_22_ok, df_23_ok, df_24_ok], ignore_index=True)

# Criar Target
pedras_ruins = ['Quartzo', 'Ágata', '#NULO!', 'nan', '0', '0.0', 'Não Informado']
df_final['Ponto_Virada'] = df_final['PEDRA'].apply(lambda x: 0 if x in pedras_ruins else 1)

# Salvar
df_final.to_csv('dados_unificados.csv', index=False)

print("\n✅ SUCESSO! Base unificada criada.")
print("-" * 30)
print("Médias por Ano (Confira se não estão zeradas):")
print(df_final.groupby('ANO')[['INDE', 'IAA']].mean())
print(f"\nTotal de alunos: {len(df_final)}")