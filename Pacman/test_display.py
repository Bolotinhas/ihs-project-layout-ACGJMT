#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do display de 7 segmentos
com diferentes valores de pontuação do Pacman.
"""

import time
import sys
import os

# Adicionar o diretório pai ao path para importar integracao
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from integracao import IO

def test_score_display():
    """Testa o display de 7 segmentos com diferentes pontuações"""
    try:
        print("Inicializando hardware...")
        io_device = IO()
        print("Hardware inicializado com sucesso!")
        
        # Teste com diferentes pontuações
        test_scores = [
            0,          # Início do jogo
            10,         # Primeiro dot
            100,        # Vários dots
            1000,       # Primeira power pellet
            5000,       # Pontuação média
            12345,      # Pontuação com todos os dígitos
            99999,      # Pontuação alta
            999999,     # Pontuação muito alta
            9999999,    # Pontuação máxima de 7 dígitos
            12345678    # Pontuação máxima de 8 dígitos
        ]
        
        print("\nTestando diferentes pontuações no display:")
        print("=" * 50)
        
        for score in test_scores:
            print(f"Exibindo pontuação: {score:8d}")
            
            # Converter pontuação para string de 8 dígitos
            score_str = str(score).zfill(8)
            
            # Separar em displays direito e esquerdo
            right_digits = score_str[-4:]  # Últimos 4 dígitos
            left_digits = score_str[-8:-4]  # 4 dígitos anteriores
            
            print(f"  Display esquerdo: {left_digits}")
            print(f"  Display direito:  {right_digits}")
            
            # Atualizar displays
            io_device.put_DP(0, right_digits)  # Display direito
            io_device.put_DP(1, left_digits)   # Display esquerdo
            
            # Aguardar 2 segundos para visualizar
            time.sleep(2)
            print()
        
        print("Limpando display...")
        io_device.put_DP(0, "0000")  # Display direito
        io_device.put_DP(1, "0000")  # Display esquerdo
        
        print("Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        print("Certifique-se de que o hardware está conectado e o driver carregado.")
        return False
    
    return True

def test_digit_mapping():
    """Testa o mapeamento individual de dígitos"""
    try:
        print("\nTestando mapeamento individual de dígitos...")
        io_device = IO()
        
        # Testar cada dígito de 0-9
        for digit in range(10):
            print(f"Exibindo dígito: {digit}")
            digit_str = str(digit)
            
            # Exibir o dígito em todas as posições
            io_device.put_DP(0, digit_str * 4)  # Display direito
            io_device.put_DP(1, digit_str * 4)  # Display esquerdo
            
            time.sleep(1)
        
        # Limpar
        io_device.put_DP(0, "0000")
        io_device.put_DP(1, "0000")
        
        print("Teste de dígitos concluído!")
        
    except Exception as e:
        print(f"Erro no teste de dígitos: {e}")

if __name__ == "__main__":
    print("=== Teste do Display de 7 Segmentos para Pacman ===")
    
    if test_score_display():
        test_digit_mapping()
    
    print("\nTeste finalizado!")
