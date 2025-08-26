# snowflake-synthetic-data-generation
Utility functions to create synthetic data in Snowflake

```sql
USE ROLE ACCOUNTADMIN;

-- Create a warehouse
CREATE WAREHOUSE IF NOT EXISTS AI_WH WITH WAREHOUSE_SIZE='X-SMALL';

-- Create a fresh Database
CREATE DATABASE IF NOT EXISTS AI_DEVELOPMENT;

-- Create the API integration with Github
CREATE OR REPLACE API INTEGRATION GITHUB_INTEGRATION_SYNTHETIC_DATA_GENERATION
    api_provider = git_https_api
    api_allowed_prefixes = ('https://github.com/michaelgorkow/')
    enabled = true
    comment='Git integration for Github Repository from Michael Gorkow.';

-- Create the integration with the Github demo repository
CREATE GIT REPOSITORY GITHUB_REPO_CORTEX_AGENTS_DEMO
	ORIGIN = 'https://github.com/michaelgorkow/snowflake-synthetic-data-generation' 
	API_INTEGRATION = 'GITHUB_INTEGRATION_SYNTHETIC_DATA_GENERATION' 
	COMMENT = 'Github Repository from Michael Gorkow with demos for synthetic data generation.';

-- Run the installation of the Demo
EXECUTE IMMEDIATE FROM @AI_DEVELOPMENT.PUBLIC.GITHUB_REPO_CORTEX_AGENTS_DEMO/branches/main/setup.sql;
```