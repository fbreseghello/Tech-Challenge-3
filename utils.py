"""
Script auxiliar para exploração rápida dos dados
Tech Challenge - Análise de Atrasos de Voos

Este script fornece funções úteis para análise exploratória dos dados.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carrega os três datasets principais.
    
    Returns:
        Tuple contendo (flights, airlines, airports)
    """
    print("Carregando dados...")
    
    airlines = pd.read_csv('airlines.csv')
    airports = pd.read_csv('airports.csv')
    flights = pd.read_csv('flights.csv')
    
    print(f"✓ Airlines: {airlines.shape}")
    print(f"✓ Airports: {airports.shape}")
    print(f"✓ Flights: {flights.shape}")
    
    return flights, airlines, airports


def get_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Retorna estatísticas resumidas de um DataFrame.
    
    Args:
        df: DataFrame para análise
        
    Returns:
        Dicionário com estatísticas
    """
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing': df.isnull().sum().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }


def plot_delay_distribution(flights: pd.DataFrame, delay_col: str = 'ARRIVAL_DELAY'):
    """
    Plota a distribuição de atrasos.
    
    Args:
        flights: DataFrame de voos
        delay_col: Nome da coluna de atraso
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histograma
    flights[delay_col].dropna().hist(bins=100, ax=axes[0], edgecolor='black')
    axes[0].set_title(f'Distribuição de {delay_col}', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Atraso (minutos)')
    axes[0].set_ylabel('Frequência')
    axes[0].axvline(x=0, color='r', linestyle='--', label='Sem atraso')
    axes[0].legend()
    
    # Boxplot
    flights[delay_col].dropna().plot(kind='box', ax=axes[1])
    axes[1].set_title(f'Boxplot de {delay_col}', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Atraso (minutos)')
    
    plt.tight_layout()
    plt.show()


def get_top_airports(flights: pd.DataFrame, 
                     airports: pd.DataFrame, 
                     n: int = 10,
                     by: str = 'volume') -> pd.DataFrame:
    """
    Retorna os top N aeroportos.
    
    Args:
        flights: DataFrame de voos
        airports: DataFrame de aeroportos
        n: Número de aeroportos a retornar
        by: Critério ('volume', 'delay', 'cancellation')
        
    Returns:
        DataFrame com top N aeroportos
    """
    if by == 'volume':
        top = flights['ORIGIN_AIRPORT'].value_counts().head(n)
        result = pd.DataFrame({
            'AIRPORT': top.index,
            'FLIGHTS': top.values
        })
    elif by == 'delay':
        avg_delay = flights.groupby('ORIGIN_AIRPORT')['ARRIVAL_DELAY'].mean()
        flight_counts = flights['ORIGIN_AIRPORT'].value_counts()
        
        # Filtrar aeroportos com pelo menos 100 voos
        valid_airports = flight_counts[flight_counts >= 100].index
        avg_delay = avg_delay[avg_delay.index.isin(valid_airports)]
        
        top = avg_delay.nlargest(n)
        result = pd.DataFrame({
            'AIRPORT': top.index,
            'AVG_DELAY': top.values
        })
    elif by == 'cancellation':
        cancel_rate = flights.groupby('ORIGIN_AIRPORT')['CANCELLED'].mean() * 100
        flight_counts = flights['ORIGIN_AIRPORT'].value_counts()
        
        valid_airports = flight_counts[flight_counts >= 100].index
        cancel_rate = cancel_rate[cancel_rate.index.isin(valid_airports)]
        
        top = cancel_rate.nlargest(n)
        result = pd.DataFrame({
            'AIRPORT': top.index,
            'CANCELLATION_RATE': top.values
        })
    
    # Merge com informações do aeroporto
    result = result.merge(airports[['IATA_CODE', 'AIRPORT', 'CITY', 'STATE']], 
                         left_on='AIRPORT', right_on='IATA_CODE', 
                         how='left', suffixes=('', '_NAME'))
    
    return result


def get_airline_performance(flights: pd.DataFrame, 
                            airlines: pd.DataFrame) -> pd.DataFrame:
    """
    Analisa a performance de cada companhia aérea.
    
    Args:
        flights: DataFrame de voos
        airlines: DataFrame de companhias
        
    Returns:
        DataFrame com métricas por companhia
    """
    airline_stats = flights.groupby('AIRLINE').agg({
        'FLIGHT_NUMBER': 'count',
        'ARRIVAL_DELAY': ['mean', 'median'],
        'CANCELLED': 'sum',
        'DIVERTED': 'sum'
    })
    
    airline_stats.columns = ['TOTAL_FLIGHTS', 'AVG_DELAY', 'MEDIAN_DELAY', 
                             'CANCELLED', 'DIVERTED']
    airline_stats = airline_stats.reset_index()
    
    # Taxas
    airline_stats['CANCEL_RATE'] = (airline_stats['CANCELLED'] / 
                                    airline_stats['TOTAL_FLIGHTS'] * 100)
    airline_stats['DIVERT_RATE'] = (airline_stats['DIVERTED'] / 
                                    airline_stats['TOTAL_FLIGHTS'] * 100)
    
    # Merge com nomes
    airline_stats = airline_stats.merge(airlines, 
                                        left_on='AIRLINE', 
                                        right_on='IATA_CODE', 
                                        how='left')
    
    return airline_stats.sort_values('TOTAL_FLIGHTS', ascending=False)


def analyze_temporal_patterns(flights: pd.DataFrame):
    """
    Analisa padrões temporais nos dados.
    
    Args:
        flights: DataFrame de voos
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Voos por mês
    if 'MONTH' in flights.columns:
        flights['MONTH'].value_counts().sort_index().plot(kind='bar', ax=axes[0, 0])
        axes[0, 0].set_title('Voos por Mês', fontweight='bold')
        axes[0, 0].set_xlabel('Mês')
        axes[0, 0].set_ylabel('Número de Voos')
    
    # Voos por dia da semana
    if 'DAY_OF_WEEK' in flights.columns:
        flights['DAY_OF_WEEK'].value_counts().sort_index().plot(kind='bar', 
                                                                 ax=axes[0, 1], 
                                                                 color='orange')
        axes[0, 1].set_title('Voos por Dia da Semana', fontweight='bold')
        axes[0, 1].set_xlabel('Dia (1=Segunda)')
        axes[0, 1].set_ylabel('Número de Voos')
    
    # Atraso médio por mês
    if 'MONTH' in flights.columns and 'ARRIVAL_DELAY' in flights.columns:
        flights.groupby('MONTH')['ARRIVAL_DELAY'].mean().plot(kind='line', 
                                                               marker='o', 
                                                               ax=axes[1, 0])
        axes[1, 0].set_title('Atraso Médio por Mês', fontweight='bold')
        axes[1, 0].set_xlabel('Mês')
        axes[1, 0].set_ylabel('Atraso (minutos)')
        axes[1, 0].grid(True, alpha=0.3)
    
    # Atraso médio por dia da semana
    if 'DAY_OF_WEEK' in flights.columns and 'ARRIVAL_DELAY' in flights.columns:
        flights.groupby('DAY_OF_WEEK')['ARRIVAL_DELAY'].mean().plot(kind='line', 
                                                                     marker='s', 
                                                                     ax=axes[1, 1],
                                                                     color='green')
        axes[1, 1].set_title('Atraso Médio por Dia da Semana', fontweight='bold')
        axes[1, 1].set_xlabel('Dia (1=Segunda)')
        axes[1, 1].set_ylabel('Atraso (minutos)')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def create_delay_flag(flights: pd.DataFrame, 
                     threshold: int = 15,
                     delay_col: str = 'ARRIVAL_DELAY') -> pd.DataFrame:
    """
    Cria flag binária para atraso.
    
    Args:
        flights: DataFrame de voos
        threshold: Threshold em minutos para considerar atraso
        delay_col: Nome da coluna de atraso
        
    Returns:
        DataFrame com nova coluna IS_DELAYED
    """
    flights = flights.copy()
    flights['IS_DELAYED'] = (flights[delay_col] > threshold).astype(int)
    
    print(f"Threshold de atraso: {threshold} minutos")
    print(f"Voos atrasados: {flights['IS_DELAYED'].sum():,}")
    print(f"Taxa de atraso: {flights['IS_DELAYED'].mean()*100:.2f}%")
    
    return flights


if __name__ == "__main__":
    # Exemplo de uso
    print("=" * 80)
    print("ANÁLISE RÁPIDA DOS DADOS DE VOOS")
    print("=" * 80)
    
    # Carregar dados
    flights, airlines, airports = load_data()
    
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS GERAIS")
    print("=" * 80)
    
    # Resumo
    summary = get_summary_stats(flights)
    print(f"\nShape: {summary['shape']}")
    print(f"Uso de memória: {summary['memory_usage']:.2f} MB")
    
    print("\n" + "=" * 80)
    print("TOP 10 AEROPORTOS POR VOLUME")
    print("=" * 80)
    top_airports = get_top_airports(flights, airports, n=10, by='volume')
    print(top_airports[['AIRPORT', 'AIRPORT_NAME', 'CITY', 'FLIGHTS']])
    
    print("\n" + "=" * 80)
    print("PERFORMANCE DAS COMPANHIAS AÉREAS")
    print("=" * 80)
    airline_perf = get_airline_performance(flights, airlines)
    print(airline_perf[['AIRLINE_x', 'AIRLINE_y', 'TOTAL_FLIGHTS', 
                        'AVG_DELAY', 'CANCEL_RATE']].head(10))
