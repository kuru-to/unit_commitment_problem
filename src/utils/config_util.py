"""config に関する便利ツールを集めたスクリプト"""

import configparser
import os

default_section = "DEFAULT"
test_section = "TEST"


def config_set() -> configparser.ConfigParser:
    """ConfigParserクラスをインスタンス化して出力
    config ファイルでの大文字・小文字の区別をつけておきたいので, 設定をする
    """
    config = configparser.ConfigParser()
    # mypy がエラーを返すため, エラー回避のためのコメントを入れておく
    config.optionxform = str  # type: ignore
    return config


def read_config_from_config_parser(config: configparser.ConfigParser, section: str) -> configparser.SectionProxy:
    """ConfigParser から対象のセクションの読み込み
    指定したセクションが対象のファイルになければデフォルトを読み込む
    """
    if not config.has_section(section):
        return config[default_section]
    return config[section]


def read_config(
    file_name: str = "config/config_path_and_name.ini", section: str = default_section
) -> configparser.SectionProxy:
    """`config.ini` から設定を読み込む

    実行ディレクトリはルートを想定

    Args:
        file_name (str, optional): ファイル名. Defaults to "config.ini".
        section (str, optional):: config ファイルのどのセクションを使用するか

    Returns:
        configparser.SectionProxy: セクションごとに設定された値を格納したconfig
    """
    config = config_set()
    config.read(file_name, encoding="utf-8")
    return read_config_from_config_parser(config, section)


def read_config_from_config_key(config_key: str, section: str = default_section) -> configparser.SectionProxy:
    """config ファイル内に書き出されているパスとファイル名から読み込みたいファイルがある場合,
    config ファイルのみ参照して読み込む
    """
    config_path_and_name = read_config(section=section)
    path_config = config_path_and_name.get("PATH_CONFIG")
    return read_config(path_config + config_path_and_name.get(config_key), section)


def write_config(file_name: str, contents: dict[str, str], section: str = default_section):
    """config ディレクトリ配下のファイルに内容を書き出す. すでにファイルが存在する場合は内容を書き換え

    Args:
        file_name (str): ファイル名
        contents (dict[str, str]): ファイルに書き加える内容の辞書
        section (str, optional): どのセクションに書き加えるか. Defaults to "DEFAULT".
    """
    config = config_set()

    # すでにファイルが存在する場合は既存の内容を読み込み
    if os.path.exists(file_name):
        config.read(file_name, encoding="utf-8")

    # 新規追加するセクションの場合, 追加する必要あり
    # デフォルトセクションは `has_section` で認識されないが, `add_section` でエラー
    # そのため, 別途判定する必要あり
    if not config.has_section(section) and section != default_section:
        config.add_section(section)

    # 値の追加
    for key, val in contents.items():
        config.set(section, key, val)

    # 指定したconfigファイルを書き込み
    with open(file_name, "w") as configfile:
        config.write(configfile)
