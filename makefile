.PHONY: export-all


export-all:
	@mkdir -p z_project_list
	@echo "Exporting project files to z_project_list/listing.txt..."
	@rm -f z_project_list/listing.txt
	@for f in $$(find . -type f \
		-not -path '*/\.*' \
		-not -path './venv/*' \
		-not -path '*/__pycache__/*' \
		-not -path '*.egg-info/*' \
		-not -path './z_project_list/*' \
		-not -name "poetry.lock" \
		-not -name ".gitkeep" \
		| sort); do \
			echo "=== $$f ===" >> z_project_list/listing.txt; \
			cat $$f >> z_project_list/listing.txt; \
			echo "\n" >> z_project_list/listing.txt; \
	done
	@echo "Export complete."