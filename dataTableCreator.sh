#!/bin/bash
for year in {2025..2099}; do
  echo "~~~$year~~~" >> dataTable.txt
  for month in {1..12}; do
    echo "---$month---" >> dataTable.txt
    curl "https://www.timeanddate.com/sun/sao-tome-and-principe/sao-tome?month=$month&year=$year" 2>/dev/null | grep -E -o "c sep-l\">[0-9]+:[0-9]+ [apAP][mM] <span" | grep -E -o "[0-9]+:[0-9]+ [apAP][mM]" >> dataTable.txt
  done
done
