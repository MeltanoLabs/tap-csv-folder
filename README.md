# tap-csv-folder

`tap-csv-folder` is a Singer tap for CSV files stored in a folder on a local or remote filesystem.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

<!-- TODO

Install from PyPi:

```bash
pipx install tap-csv-folder
```

-->

Install from GitHub:

```bash
pipx install git+https://github.com/MeltanoLabs/tap-csv-folder.git@main
```

Install in a Meltano project:

```bash
meltano add extractor tap-csv-folder --from-ref https://raw.githubusercontent.com/MeltanoLabs/tap-csv-folder/refs/heads/main/plugin.yml
```

## Configuration

### Accepted Config Options

| Setting                    | Required | Default | Description                                                                                                           |
| :------------------------- | :------- | :------ | :-------------------------------------------------------------------------------------------------------------------- |
| delimiter                  | False    | ,       | Field delimiter character.                                                                                            |
| quotechar                  | False    | "       | Quote character.                                                                                                      |
| escapechar                 | False    | None    | Escape character.                                                                                                     |
| doublequote                | False    | true    | Whether quotechar inside a field should be doubled.                                                                   |
| lineterminator             | False    |         |                                                                                                                       |
| Line terminator character. |          |         |                                                                                                                       |
| filesystem                 | False    | local   | The filesystem to use.                                                                                                |
| path                       | False    | None    | Path to the directory where the files are stored.                                                                     |
| read_mode                  | False    | None    | Use `one_stream_per_file` to read each file as a separate stream, or `merge` to merge all files into a single stream. |
| stream_name                | False    | files   | Name of the stream to use when `read_mode` is `merge`.                                                                |

#### Filesystem settings

The following settings are provided by the Singer SDK for filesystems and supported by the tap.

| Setting                  | Required | Default | Description                               |
| :----------------------- | :------- | :------ | :---------------------------------------- |
| ftp                      | False    | None    | FTP connection settings                   |
| ftp.host                 | True     | None    | FTP server host                           |
| ftp.port                 | False    | 21      | FTP server port                           |
| ftp.username             | False    | None    | FTP username                              |
| ftp.password             | False    | None    | FTP password                              |
| ftp.timeout              | False    | 60      | Timeout of the FTP connection in seconds  |
| ftp.encoding             | False    | utf-8   | FTP server encoding                       |
| sftp                     | False    | None    | SFTP connection settings                  |
| sftp.host                | True     | None    | SFTP server host                          |
| sftp.ssh_kwargs          | False    | None    | SSH connection settings                   |
| sftp.ssh_kwargs.port     | False    | 22      | SFTP server port                          |
| sftp.ssh_kwargs.username | True     | None    | SFTP username                             |
| sftp.ssh_kwargs.password | False    | None    | SFTP password                             |
| sftp.ssh_kwargs.pkey     | False    | None    | Private key                               |
| sftp.ssh_kwargs.timeout  | False    | 60      | Timeout of the SFTP connection in seconds |

#### Built-in Singer SDK capabilities

The following settings are provided by the Singer SDK and automatically supported by the tap.

| Setting                           | Required | Default | Description                                                                                                                                                                                                                                              |
| :-------------------------------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| stream_maps                       | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                              |
| stream_map_config                 | False    | None    | User-defined config values to be used within map expressions.                                                                                                                                                                                            |
| faker_config                      | False    | None    | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed                 | False    | None    | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                |
| faker_config.locale               | False    | None    | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                    |
| flattening_enabled                | False    | None    | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                           |
| flattening_max_depth              | False    | None    | The max depth to flatten schemas.                                                                                                                                                                                                                        |
| batch_config                      | False    | None    |                                                                                                                                                                                                                                                          |
| batch_config.encoding             | False    | None    | Specifies the format and compression of the batch files.                                                                                                                                                                                                 |
| batch_config.encoding.format      | False    | None    | Format to use for batch files.                                                                                                                                                                                                                           |
| batch_config.encoding.compression | False    | None    | Compression format to use for batch files.                                                                                                                                                                                                               |
| batch_config.storage              | False    | None    | Defines the storage layer to use when writing batch files                                                                                                                                                                                                |
| batch_config.storage.root         | False    | None    | Root path to use when writing batch files.                                                                                                                                                                                                               |
| batch_config.storage.prefix       | False    | None    | Prefix to use when writing batch files.                                                                                                                                                                                                                  |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-csv-folder --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

## Usage

You can easily run `tap-csv-folder` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-csv-folder --version
tap-csv-folder --help
tap-csv-folder --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-csv-folder` CLI interface directly using `poetry run`:

```bash
poetry run tap-csv-folder --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-csv-folder
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-csv-folder --version
# OR run a test `elt` pipeline:
meltano run tap-csv-folder target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
