Python script for post-DNS zone migration validation.

- Place zone files (with .zone extension) in the same directory as this script
- Run script before and after migrations to produce outputs for pre/post diff checks
- The script will identify CNAMEs from the selected zone file and validate the contents of the records
- Complete diff checks to validate pre/post migration states
