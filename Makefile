.PHONY: harmonise summary clean single

HARMONISED_WIDE := outputs/finscope_harmonised.csv
HARMONISED_LONG := outputs/finscope_harmonised_long.csv

harmonise:
	python scripts/harmonise.py --output $(HARMONISED_WIDE) --long-output $(HARMONISED_LONG)

summary:
	python scripts/summary_table.py --input $(HARMONISED_WIDE) --long-output $(HARMONISED_LONG)

single:
	@read -p "Year: " YEAR; \
	python scripts/clean_year.py $$YEAR --output-dir outputs

clean:
	rm -f $(HARMONISED_WIDE) $(HARMONISED_LONG)
