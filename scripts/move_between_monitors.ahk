; move_between_monitors.ahk – Uso: move_between_monitors.ahk <TítuloJanela> <NumMonitor>
if (%0% < 2) {
    MsgBox, %0%
    MsgBox, Erro: uso correto: %A_ScriptName% "TítuloJanela" NumMonitor
    ExitApp
}
janela = %1%
monitor := %2% + 0

; Verifica existência de janelas
if (!WinExist(janela)) {
    MsgBox, Erro: janela "%janela%" não encontrada.
    ExitApp
}

; Obtém número total de monitores
SysGet, MonCount, MonitorCount
if (monitor < 1 || monitor > MonCount) {
    MsgBox, Erro: monitor inválido (1 - %MonCount%).
    ExitApp
}

; Obtém coordenadas do monitor destino
SysGet, MonDest, Monitor, %monitor%
; Move mantendo tamanho atual
WinGetPos, curX, curY, curW, curH, %janela%
WinMove, %janela%, , %MonDestLeft%, %MonDestTop%, %curW%, %curH%
ExitApp
