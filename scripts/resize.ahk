; resize.ahk – Uso: resize.ahk <TítuloJanela> <Largura> <Altura>
if %0% < 3 {
    MsgBox, Erro: uso correto: %A_ScriptName% "TítuloJanela" Larg Alt
    ExitApp
}
janela = %1%
novaLargura := %2%
novaAltura := %3%
; Obtém posição atual para não mover a janela
WinGetPos, curX, curY,,, %janela%
WinMove, %janela%, , %curX%, %curY%, %novaLargura%, %novaAltura%
ExitApp