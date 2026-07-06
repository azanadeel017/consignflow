# scanner.ps1
# Import mock sales data from CSV
$csvPath = Join-Path $PSScriptRoot "mock_sales.csv"

if (-not (Test-Path $csvPath)) {
    Write-Error "mock_sales.csv not found at $csvPath"
    exit 1
}

Write-Host "Reading sales data from: $csvPath`n" -ForegroundColor Cyan

# Load the CSV
$sales = Import-Csv -Path $csvPath

# Filter items where 'Item Title' starts with 'M1'
$m1Items = $sales | Where-Object { $_.'Item Title' -like 'M1*' }

# Output results nicely formatted
Write-Host "--- Scanning for items starting with 'M1' ---" -ForegroundColor Green
if ($null -eq $m1Items -or $m1Items.Count -eq 0) {
    Write-Host "No matching items found." -ForegroundColor Yellow
} else {
    $m1Items | Format-Table -AutoSize
    Write-Host "Total matching items found: $($m1Items.Count)" -ForegroundColor Green
}
