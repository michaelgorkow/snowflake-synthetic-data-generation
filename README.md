# 🎯 Synthetic Data Generation in Snowflake

A comprehensive toolkit for generating high-quality synthetic data directly within Snowflake, featuring audio, image, and video generation capabilities.

## 🚀 Overview

This repository provides utilities and examples for creating various types of synthetic data using generative AI. Generate realistic audio conversations, synthetic images, and video content for training datasets, testing scenarios, and data augmentation.

## 📋 Contents

### 🎤 Audio Generation

**Notebook:** `src/SYNTHETIC_DATA_GENERATION_AUDIO.ipynb`

Demonstrates advanced text-to-speech capabilities for creating realistic audio content:

- **Single-Speaker Synthesis** - Generate clear narrations and announcements
- **Multi-Speaker Dialogues** - Create conversations between multiple characters with distinct voices
- **Call Center Simulations** - Build realistic customer service interactions for training
- **Random Voice Assignment** - Automatically assign diverse voices to characters
- **Snowflake Integration** - Save generated audio directly to Snowflake stages
- **Voice Variety** - Access to 60+ high-quality voices across different genders and styles

**Use Cases:** Customer service training data, accessibility features, content creation, conversational AI datasets

### 🖼️ Image Generation
*Coming Soon* - Synthetic image generation capabilities

### 🎬 Video Generation  
*Coming Soon* - Synthetic video content creation tools

## ⚡ Quick Setup

Run the following SQL commands in your Snowflake worksheet to set up the environment:

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

## 🔮 Future Additions

This repository is actively being developed. Planned additions include:

- **Image Generation** - Create synthetic images for computer vision datasets
- **Video Synthesis** - Generate video content for training and simulation
- **Multi-Modal Examples** - Combine audio, image, and video generation
- **Advanced Snowflake Integrations** - Enhanced workflows and automation

## 🎯 Applications

- **Training Data Generation** - Create diverse datasets for machine learning models
- **Testing & Simulation** - Generate realistic scenarios for system testing  
- **Content Creation** - Automated content generation for various media types
- **Data Augmentation** - Enhance existing datasets with synthetic variations
- **Privacy-Preserving Analytics** - Generate synthetic alternatives to sensitive data

---

*For detailed implementation examples and code walkthroughs, explore the individual notebooks in the `src/` directory.*