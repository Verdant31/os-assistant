#Requires AutoHotkey v2.0

if (A_Args.Length < 2) {
    MsgBox("Uso: monitor_control.ahk enable|disable monitor_number")
    ExitApp
}

action := A_Args[1]
monitorNumber := A_Args[2]

if !(action = "enable" || action = "disable") {
    MsgBox("Erro: ação deve ser 'enable' ou 'disable'")
    ExitApp
}

if !IsNumber(monitorNumber) || monitorNumber < 1 {
    MsgBox("Erro: número do monitor deve ser um número positivo")
    ExitApp
}

command := (action = "enable") ? "Enable-display " . monitorNumber : "Disable-display " . monitorNumber

RunWait(
    'cmd.exe /c powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden ' . command
    , "", "Hide"
)