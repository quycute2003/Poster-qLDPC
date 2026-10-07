param(
    [Parameter(Mandatory=$true)][string]$InputPptx,
    [Parameter(Mandatory=$true)][string]$OutputPdf
)
$ErrorActionPreference = 'Stop'
$posterApp = $null
$posterDeck = $null
try {
    $posterApp = New-Object -ComObject PowerPoint.Application
    $posterDeck = $posterApp.Presentations.Open((Resolve-Path -LiteralPath $InputPptx).Path, -1, 0, 0)
    if ($posterDeck.Slides.Count -ne 1) { throw 'Expected a one-slide poster' }
    $posterRange = $posterDeck.PrintOptions.Ranges.Add(1, 1)
    # PDF / print intent / slides / all slides; document tags enabled.
    # BitmapMissingFonts=false prevents text from silently becoming raster.
    # No PDF/A conversion; PowerPoint retains the source PNG images losslessly.
    $posterDeck.ExportAsFixedFormat(
        [IO.Path]::GetFullPath($OutputPdf), 2, 2, 0, 1, 1, 0,
        $posterRange, 1, '', -1, -1, -1, 0, 0
    )
} finally {
    if ($null -ne $posterDeck) {
        $posterDeck.Close()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($posterDeck)
    }
    if ($null -ne $posterApp) {
        # Do not close any presentations belonging to the user.
        if ($posterApp.Presentations.Count -eq 0) { $posterApp.Quit() }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($posterApp)
    }
}
