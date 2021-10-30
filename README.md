# 生物学的構造単位生成器

symmetry shift

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2021/07/JPHACKS2021_ogp.jpg)](https://www.youtube.com/watch?v=LUPQFB4QyVo)


## Quick install and use guide

Installation needs distributed biopython we modified.

```sh
pip install git+https://github.com/flat35hd99/biopython
pip install symmetryshift
```

and then, simply

```sh
symmetry 1KZU # Argument is pdb id.
```

Please check the `out.pdb` on your structure viewer and compare between `out.pdb` and `kz/pdb1kzu.ent`.(The latter is downloaded by biopython.)

## 製品概要
### 背景(製品開発のきっかけ、課題等）

PDBファイルという生物学・生化学分野における、タンパク質の結晶構造を記すデファクトスタンダードなファイル形式が存在する。

このファイルは、

1. X線結晶構造解析やクライオ電顕などでタンパク質の結晶構造が解明され論文化されるとき、ほぼ確実に作成・公開される。
2. 分子動力学シミュレーションはこのデータをもとにシミュレーションを行う。
3. その他立体構造の解析では必ず利用されるといっても過言ではない。

PDBファイルは解析におけるほぼすべての情報を保持できるという強力な特性があるが、それゆえファイルサイズは肥大化しがちである。

そのため、回転対称性・並進対称性が構造内に存在する場合には、その対称性を利用してファイルサイズを節約する戦略が取られる。すなわち、回転対称性のある原子群（正確には主鎖ごと）について、単位（ユニット）になる原子の座標のみを記録しておき、残りの原子はどのように回転・並進させれば座標を再現できるか記すのである。

このようにして、生物学的構造単位（生物学的に意味のある分子集団）を再現する。

### 製品説明（具体的な製品の説明）

本プロダクトは、この回転・並進の作業をほぼ全てのPDBファイルに対して自動化する。

具体的な説明を行う。以下は開発した生物学的構造単位生成器、もとい symmetry shift のワークフロー図である。赤色が今回私たちが開発、または、機能追加した箇所である。黄緑（緑系）で示した箇所は`Bio.PDP`パッケージがあらかじめ備えていた機能である。

![symmetryshiftのワークフロー図](src/workflow.drawio.svg)

ユーザーは生物学的構造単位（生物学的に意味のある構造）を取得したいPDB IDをCLIから指定する。これ以上のユーザーからのインプットはない。すべてsymmetry shift内で完結する。

```sh
symmetry 5V8K # PDB ID is 5V8K
```

symmetry shiftは受け取ったPDB IDを`Bio.PDB`を用いてPDB fileをサーバーから取得する（PDB fileは無償で公開されている）

### 特長

- biopython.PDBという既存OSSを全面的に利用、また、内部の演算子をオーバーライドするなどの簡単な処理を行った。biopythonは情報の提供を責務として開発されているため、今回の対称性から原子座標を計算することは責務の範囲外にあたる。この切り分けを行った。
- 確認できるすべてのファイルに対して正常に動作する。zero configuration.

### 解決出来ること

- PDB idを入れればやってくれるので、今後回転対称性・並進対称性を使って新しくPDBファイルを作る作業はやらなくてよくなる。すなわち、全ての生化学分野のアカデミアンの時間を節約する。
  - ほんとに使い勝手がいいので、布教予定。

### 今後の展望

- CLIツールにする
- package化してPYPIで配布する

### 注力したこと（こだわり等）

* biopythonが解決すべきことかしないことかを考えた。
  * 実装すべきかどうかも考えた。
  * 実装すべきものは今後の本家へのPRも考慮して、（忙しくないときは）コミットメッセージをわかりやすく書いた。
* biopythonが解決すべきだと判断したときは、biopythonのユーザーが純粋に使いやすくなるように考慮して実装した。
* 自分たちのやりたかったことはその延長線上にあるようにした。

## 開発技術

PDBファイルから生物学的構造単位を生成、保存すること。

#### API・データ
* Protein Data Bank

#### フレームワーク・ライブラリ・モジュール
* [biopython(本家)](https://github.com/biopython/biopython) (forkは[こちら](https://github.com/flat35hd99/biopython))
* 発表、動画、説明の画像には[PyMOL](https://pymol.org/2/)を利用した。

### 独自技術
#### ハッカソンで開発した独自機能・技術
* 回転・並進対称性のある結晶構造が記されたPDBファイルについて、これをPDBファイル内のヘッダーを解析して生物学的構造単位を生成・保存する技術
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。


開発における注力ポイントと、なにをしているのかを説明する。

- biopythonのシンプルさを殺さずにそれぞれの機能を小さく実装した。
- symmetryshiftはbiopythonの機能を使うこととユーザーからのインプットを捌くインターフェースとした。

以下に具体的に説明する。

biopythonはバイオインフォマティクスの分野で特に活用されている、バイオインフォマ研究者向けのpythonインターフェースである。その中の`Bio.PDB`パッケージを利用・機能追加を行った。

`Bio.PDB`の中で私たちが利用したのは

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
* Protein Data Bank
* biopython

### 謝辞
* We appriciate for A. Kimura to suggest this theme and teach how to read PDB files. 
