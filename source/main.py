import pandas as pd
from pyproj import Transformer
import numpy as np

def executar_etl_acidentes(input_file, output_file):
    print(f"Iniciando ETL no arquivo: {input_file}")
    
    # CORREÇÃO 1: O separador correto é ponto e vírgula (;)
    # O encoding 'latin-1' costuma funcionar melhor para arquivos do governo brasileiro
    try:
        df = pd.read_csv(input_file, sep=';', encoding='utf-8', on_bad_lines='skip')
    except:
        df = pd.read_csv(input_file, sep=';', encoding='latin-1', on_bad_lines='skip')
    
    # Padronizar nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Limpeza de Strings
    cols_str = df.select_dtypes(include=['object']).columns
    for col in cols_str:
        df[col] = df[col].str.strip()
        
    # Conversão de Datas
    df['DATA_HORA'] = pd.to_datetime(df['DATA HORA_BOLETIM'], format='%d/%m/%Y %H:%M', errors='coerce')
    
    # Extrair componentes de data
    df['ANO'] = df['DATA_HORA'].dt.year
    df['MES'] = df['DATA_HORA'].dt.month
    df['DIA'] = df['DATA_HORA'].dt.day
    df['HORA'] = df['DATA_HORA'].dt.hour
    
    # Traduzir dias da semana
    dias_traducao = {
        'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    df['DIA_SEMANA'] = df['DATA_HORA'].dt.day_name().map(dias_traducao)
    
    # Conversão de Coordenadas
    transformer = Transformer.from_crs("epsg:31983", "epsg:4326")
    
    def converter_coords(row):
        if pd.notnull(row['COORDENADA_X']) and pd.notnull(row['COORDENADA_Y']):
            if row['COORDENADA_X'] > 1000 and row['COORDENADA_Y'] > 1000:
                try:
                    # O retorno padrão é (lat, lon) para EPSG:4326
                    lat, lon = transformer.transform(row['COORDENADA_X'], row['COORDENADA_Y'])
                    return pd.Series([lat, lon])
                except:
                    pass
        return pd.Series([np.nan, np.nan])

    print("Convertendo coordenadas (isso pode demorar um pouco)...")
    df[['LATITUDE', 'LONGITUDE']] = df.apply(converter_coords, axis=1)
    
    # Filtragem Final
    df_limpo = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
    
    colunas_finais = [
        'NUMERO_BOLETIM', 'DATA_HORA', 'ANO', 'MES', 'DIA', 'HORA', 'DIA_SEMANA',
        'DESC_TIPO_ACIDENTE', 'DESC_TEMPO', 'PAVIMENTO', 'DESC_REGIONAL', 
        'ORIGEM_BOLETIM', 'LOCAL_SINALIZADO', 'VELOCIDADE_PERMITIDA', 
        'INDICADOR_FATALIDADE', 'LATITUDE', 'LONGITUDE'
    ]
    
    # Garante que só seleciona colunas que existem
    cols_existentes = [c for c in colunas_finais if c in df_limpo.columns]
    df_final = df_limpo[cols_existentes]
    
    # Salvar
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Arquivo salvo com sucesso: {output_file}")

# CORREÇÃO 2: A chamada da função NÃO pode ter # na frente
# Certifique-se que o nome do arquivo de entrada é exatamente o que você baixou
executar_etl_acidentes('si-bol-2024.csv', 'acidentes_bh_limpo_v2.csv')