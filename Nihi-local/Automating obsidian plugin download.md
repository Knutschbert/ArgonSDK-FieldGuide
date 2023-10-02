
```bash
curl -s https://api.github.com/repos/vslinko/obsidian-outliner/releases/latest | grep "browser_download_url" |  cut -d : -f 2,3 | tr -d \" | xargs -n 1 curl -LO
```

