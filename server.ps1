$vars = @{
  API_TYPE = "azure"; 
  API_VERSION = "2022-06-01-preview";
  API_BASE = ""; 
  API_KEY = "";
  ORIGINS = "*";
  PORT = 8080
}

# read in .env file and map to hashtable
Get-Content -Path ./server/.env | ForEach-Object {
  $vars[$_.Split("=")[0].Trim()] = $_.Split("=")[1].Trim()
}

Write-Host "Building docker image..."
docker image build -t flask-gptchat .
Write-Host "Running docker container..."
docker run -d -it `
        -e API_TYPE='$vars["API_TYPE"]' `
        -e API_BASE='$vars["API_BASE"]' `
        -e API_VERSION='$vars["API_VERSION"]' `
        -e API_KEY='$vars["API_KEY"]' `
        -e ORIGINS='$vars["ORIGINS"]' `
        -p $vars["PORT"]:5000 `
        --name flask-gptchat
# checking things in