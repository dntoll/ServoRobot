#!/bin/bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github

git add .
git commit -m "."
git push origin main
