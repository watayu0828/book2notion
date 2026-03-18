# Book2Notion

[![CI](https://github.com/watayu0828/book2notion/actions/workflows/ci.yml/badge.svg)](https://github.com/watayu0828/book2notion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Import your Kindle highlights into a Notion database with one click.

## Features

- Parse Kindle highlight export HTML files
- Automatically create Notion database entries for each highlight
- Supports **Japanese** and **English** Kindle exports (auto-detected)
- Simple GUI — just select a file and import

## Prerequisites

- Python 3.10 or later
- A Notion account with an integration token

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/watayu0828/book2notion.git
cd book2notion
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Notion integration

1. Duplicate [this database template](https://www.notion.so/3d443390a32544e9825255cd6aa5010e) to your Notion workspace.
2. Create a Notion integration and obtain the integration token. See the [Notion integration guide](https://developers.notion.com/docs/create-a-notion-integration) for instructions.
3. Connect the integration to your duplicated database.

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```text
TOKEN='secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
DATA_SOURCE_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

- **TOKEN**: Your Notion integration token (starts with `secret_`).
- **DATA_SOURCE_ID**: Navigate to your database URL to get the database ID, then call the [Retrieve a database](https://developers.notion.com/reference/retrieve-a-database) API to get a list of `data_sources`. Use the `id` of the desired data source. Alternatively, in the Notion app, open the database settings menu → **Manage data sources** → **Copy data source ID**.

### 5. Run

```bash
python -m book2notion
```

Select your Kindle export HTML file in the dialog, and your highlights will be imported into Notion.

## Export Kindle Highlights

1. Open the Kindle app and go to the **Annotations** page of a book.
2. Tap the **Export** button.
3. Choose **Email** and send the export to yourself.
4. Download the attached HTML file to your PC.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

[MIT](LICENSE)

## Support

Book2Notion is free and open source. If you find it useful, consider supporting the project:

<a href="https://www.buymeacoffee.com/watayu0828" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
