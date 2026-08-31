.PHONY: harmonise summary clean single

HARMONISED_WIDE := outputs/finscope_harmonised.csv
HARMONISED_LONG := outputs/finscope_harmonised_long.csv
PUBLIC_DATA := docs/public_data/finscope_harmonised.csv

harmonise:
	python scripts/harmonise.py --output $(HARMONISED_WIDE) --long-output $(HARMONISED_LONG)
	cp $(HARMONISED_WIDE) $(PUBLIC_DATA)
	python scripts/build_homepage_summary.py --input $(HARMONISED_WIDE) --mapping-file mappings/harmonised_questions.csv --output docs/assets/data/harmonised-summary.json

summary:
	python scripts/summary_table.py --input $(HARMONISED_WIDE) --long-output $(HARMONISED_LONG)

single:
	@read -p "Year: " YEAR; \
	python scripts/clean_year.py $$YEAR --output-dir outputs

clean:
	rm -f $(HARMONISED_WIDE) $(HARMONISED_LONG)
