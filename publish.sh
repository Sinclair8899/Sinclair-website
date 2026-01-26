#!/bin/bash
cd ~/Desktop/Sinclair-website
rm -rf public/ docs/
hugo
git add -A
git commit -m "Update site"
git push origin main
echo "Done!"
