#Requires AutoHotkey v2.0

LaunchApp(appExe) {
    if ProcessExist(appExe)
        return false  ; já está rodando
    try {
        pid := Run(appExe)  ; executa o aplicativo e obtém o PID
        return pid
    } catch {
        MsgBox "Erro: não foi possível executar " appExe
        return false
    }
}

MoveWindow(appExe, left, top, width, height) {
    pid := ProcessExist(appExe)             ; retorna PID do processo ou 0 se não existir
    if !pid
        return false  ; processo não encontrado
    hwnd := WinExist("ahk_pid " pid)      ; obtém o HWND da janela
    if hwnd
        WinMove(left, top, width, height, "ahk_id " hwnd)
    return hwnd      ; retorna HWND movido ou false
}

appExe1 := A_Args[1]
appExe2 := A_Args[2]
monitorIndex := A_Args[3] ? A_Args[3] : 1

if !ProcessExist(appExe1)
    LaunchApp(appExe1)
if !ProcessExist(appExe2)
    LaunchApp(appExe2)

Sleep 500
try {
    MonitorGetWorkArea(monitorIndex, &left, &top, &right, &bottom)
} catch {
    MsgBox "Erro: monitor " monitorIndex " não encontrado."
}
width := right - left
height := bottom - top
; define orientação
if (width >= height) {
    ; paisagem: divide verticalmente
    sizeA := width // 2
    sizeB := width - sizeA    ; cobre remainder
    MoveWindow(appExe1, left, top, sizeA, height)
    MoveWindow(appExe2, left + sizeA, top, sizeB, height)
} else {
    ; retrato: divide horizontalmente
    sizeA := height // 2
    sizeB := height - sizeA
    MoveWindow(appExe1, left, top, width, sizeA)
    MoveWindow(appExe2, left, top + sizeA, width, sizeB)
}
ExitApp