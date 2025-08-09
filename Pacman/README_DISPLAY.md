# Display de 7 Segmentos - Pacman Score

Esta implementação adiciona suporte para exibir o placar do jogo Pacman em displays de 7 segmentos conectados ao hardware.

## Funcionalidades Implementadas

### 1. Exibição do Placar em Tempo Real

- O placar é atualizado automaticamente no display de 7 segmentos durante o jogo
- Suporta pontuações de até 8 dígitos (99.999.999 pontos)
- Utiliza dois displays de 4 dígitos cada:
  - **Display Direito**: Últimos 4 dígitos (unidades)
  - **Display Esquerdo**: 4 dígitos anteriores (milhares)

### 2. Otimização de Performance

- Só atualiza o display quando a pontuação muda
- Evita writes desnecessários no hardware
- Logging detalhado para debug

### 3. Tratamento de Erros

- Funciona mesmo se o hardware não estiver disponível
- Logs de erro informativos
- Inicialização graceful

## Arquivos Modificados

### `src/runner.py`

- Adicionado import da classe `IO` de `integracao.py`
- Inicialização do hardware no construtor
- Método `update_score_display()` para atualizar o placar
- Método `clear_display()` para limpar o display
- Integração no loop principal do jogo

### `test_display.py` (Novo)

- Script de teste independente
- Testa diferentes valores de pontuação
- Verifica o mapeamento de dígitos
- Útil para debug e validação

## Como Usar

### Executar o Jogo

```bash
cd Pacman
python main.py
```

O placar será automaticamente exibido no display de 7 segmentos durante o jogo.

### Testar o Display

```bash
cd Pacman
python test_display.py
```

Este comando executa uma sequência de testes para verificar se o display está funcionando corretamente.

## Formato de Exibição

### Exemplo de Pontuações:

- **123 pontos**: Display mostra `00000123`
- **5.678 pontos**: Display mostra `00005678`
- **12.345.678 pontos**: Display mostra `12345678`

### Layout dos Displays:

```
Display Esquerdo    Display Direito
    [1][2][3][4]       [5][6][7][8]
```

Para 12345678:

- Display Esquerdo: `1234`
- Display Direito: `5678`

## Integração com Hardware

### Conexões Necessárias:

- Device `/dev/mydev` deve estar disponível
- Driver carregado corretamente
- Displays de 7 segmentos conectados aos registradores:
  - `DIS_L` (24931): Display esquerdo
  - `DIS_R` (24932): Display direito

### Comandos ioctl Utilizados:

- `DIS_L`: Controla display esquerdo (milhares)
- `DIS_R`: Controla display direito (unidades)

## Troubleshooting

### Problema: Display não atualiza

- Verificar se o dispositivo `/dev/mydev` existe
- Confirmar se o driver está carregado
- Executar `test_display.py` para diagnosticar

### Problema: Erro de importação

- Certificar-se de que `integracao.py` está no diretório correto
- Verificar se todas as dependências estão instaladas

### Problema: Valores incorretos no display

- Verificar mapeamento de dígitos no `integracao.py`
- Executar teste de dígitos individuais

## Logs

O sistema gera logs detalhados:

- `INFO`: Inicialização e operações normais
- `DEBUG`: Atualizações de pontuação
- `WARNING`: Hardware não disponível
- `ERROR`: Problemas de comunicação com hardware

## Extensões Futuras

- Exibir high score em modo alternado
- Animações de pontuação especial
- Indicadores visuais para power-ups
- Contagem regressiva de vidas
