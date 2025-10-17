#!/usr/bin/env bash

# 1 - Download alle data via MaSS API (https://mass.cultureelerfgoed.nl/api/) 

mkdir -p "cache"
python3 mass_download.py

# 2 - Haal wat data uit de lijst die niet in de details zit

java -jar sparql-anything-v1.0.0.jar -q mass-list.rq -format nt > all_mass.nt
 
# 3 - Converteer alle JSON bestanden narr RDF met sparql-anything

for json in cache/*.json; do
  java -jar sparql-anything-v1.0.0.jar \
    -q mass-get.rq \
    -v location="file:$(realpath "$json")" \
    -f nt
done >> all_mass.nt

sort -u all_mass.nt > all_mass_unique.nt
