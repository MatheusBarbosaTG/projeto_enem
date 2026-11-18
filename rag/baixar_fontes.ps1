# Baixa as fontes do RAG para a pasta docs\ com os nomes de fontes.csv
# Uso (na pasta rag):  powershell -ExecutionPolicy Bypass -File baixar_fontes.ps1
$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$docs = Join-Path $PSScriptRoot "docs"
New-Item -ItemType Directory -Force -Path $docs | Out-Null
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

$pdfs = [ordered]@{
  "influencia_parental_renda_enem.pdf"   = @("https://periodicos.utfpr.edu.br/rts/article/download/20589/11491")
  "influencia_renda_enem_longitudinal.pdf" = @("https://periodicos.feevale.br/seer/index.php/revistagestaoedesenvolvimento/article/download/4318/3506/12290")
  "fatores_socioeconomicos_nota_enem.pdf" = @("https://revistas.fucamp.edu.br/index.php/cadernos/article/download/3832/2501","https://revistas.fucamp.edu.br/index.php/cadernos/article/view/3832/2501")
  "desempenho_minas_gerais_enem.pdf"     = @("https://www.redalyc.org/journal/298/29874394059/29874394059.pdf")
  "enem_norte_do_brasil.pdf"             = @("https://brsa.org.br/wp-content/uploads/wpcf7-submissions/7559/Artigo_ENEM-NO-NORTE-DO-BRASIL_-identificado.pdf")
  "nota_tecnica_14_2021_daeb.pdf"        = @("https://download.inep.gov.br/microdados/nota_tecnica_14-2021_daeb.pdf")
}

$falhas = @()
foreach ($nome in $pdfs.Keys) {
  $destino = Join-Path $docs $nome
  $ok = $false
  foreach ($url in $pdfs[$nome]) {
    try {
      Invoke-WebRequest -Uri $url -OutFile $destino -UserAgent $ua -MaximumRedirection 10 -TimeoutSec 120
      $bytes = [IO.File]::ReadAllBytes($destino)
      if ($bytes.Length -gt 4 -and [Text.Encoding]::ASCII.GetString($bytes,0,4) -eq "%PDF") { $ok = $true; break }
      Remove-Item $destino -ErrorAction SilentlyContinue
    } catch { Write-Host "  erro em $url : $($_.Exception.Message)" }
  }
  if ($ok) { Write-Host "OK     $nome" -ForegroundColor Green } else { Write-Host "FALHOU $nome" -ForegroundColor Red; $falhas += $nome }
}

# Lei 13.005/2014 (HTML -> TXT)
try {
  $r = Invoke-WebRequest -Uri "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13005.htm" -UserAgent $ua -TimeoutSec 120
  $bytes = $r.RawContentStream.ToArray()
  $html = [Text.Encoding]::GetEncoding("iso-8859-1").GetString($bytes)
  $txt = [regex]::Replace($html, "(?is)<(script|style).*?</\1>", " ")
  $txt = [regex]::Replace($txt, "(?i)<br\s*/?>|</p>|</div>|</tr>", "`n")
  $txt = [regex]::Replace($txt, "<[^>]+>", " ")
  $txt = [Net.WebUtility]::HtmlDecode($txt)
  $txt = [regex]::Replace($txt, "[ \t]+", " ")
  $txt = [regex]::Replace($txt, "(\s*\n\s*)+", "`n")
  [IO.File]::WriteAllText((Join-Path $docs "pne_lei_13005_2014.txt"), $txt, (New-Object Text.UTF8Encoding($false)))
  Write-Host "OK     pne_lei_13005_2014.txt" -ForegroundColor Green
} catch { Write-Host "FALHOU pne_lei_13005_2014.txt : $($_.Exception.Message)" -ForegroundColor Red; $falhas += "pne_lei_13005_2014.txt" }

# fontes.csv: .html -> .txt
$csv = Join-Path $PSScriptRoot "fontes.csv"
if (Test-Path $csv) {
  (Get-Content $csv -Raw -Encoding UTF8) -replace "pne_lei_13005_2014\.html","pne_lei_13005_2014.txt" | Set-Content $csv -Encoding UTF8 -NoNewline
}

Write-Host ""
if ($falhas.Count -eq 0) { Write-Host "Tudo certo. Agora rode: py construir_indice.py" -ForegroundColor Cyan }
else { Write-Host "Baixe manualmente (navegador) e salve em docs\ com estes nomes:"; $falhas | ForEach-Object { Write-Host " - $_" } }