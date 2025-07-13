

$repo = "genai-works-org/genai-agentos"
$gh_token=$env:GITHUB_TOKEN

# Get the latest release data
$headers = @{
    Authorization = "token $gh_token"
    "User-Agent" = "PowerShell"
}

# Get the latest release data
$release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/latest" -Headers $headers

$version = $release.tag_name

$assetName = "genai-windows-$version.exe"
$output = ".\$assetName"

# Find the asset download URL
$asset = $release.assets | Where-Object { $_.name -eq $assetName }

$assetId = $asset.id
$apiDownloadUrl = "https://api.github.com/repos/$repo/releases/assets/$assetId"

$downloadHeaders = @{
    Authorization = "Bearer $gh_token"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent" = "PowerShell"
    "Accept"     = "application/octet-stream"
}

if ($asset -ne $null) {
    Invoke-WebRequest -Uri $apiDownloadUrl -Headers $downloadHeaders -OutFile $output -Method Get
    Write-Output "Downloaded to $output"
} else {
    Write-Error "Asset '$assetName' not found in the latest release."
}