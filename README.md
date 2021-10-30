# 生物学的構造単位生成器

symmetry shift

[![IMAGE ALT TEXT HERE](src/biological_assembly.jpg)](https://youtu.be/-h38XeSu9sA)

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

### 分子生物学的な前提知識
背景でも述べたように、PDB (Protein Data Bank) ファイルには、以下のように単位構造にある全原子の座標が記載されてある。枠で囲ってある部分は、左から原子のx座標、y座標、z座標である。

![pdb_coord](https://user-images.githubusercontent.com/84301337/139531746-ee44b003-c757-45d6-8399-9bde1ea79c4c.jpg)

pdbファイルは、主にatom, structure, chain で構成されていて、biopythonパッケージがこれらの情報を活用している。

PDBファイルには単位構造のデータのみしか記載されていないため、すべての構造データを一度に得ることができない。

![pdb_compere](https://user-images.githubusercontent.com/84301337/139533463-2a4bb956-8778-46f4-9988-18bfc68a21ab.jpg)


そこで、我々はPDBファイルの中にコメントとして本来の構造に関する記述があることを用いて、原子の座標を対称操作することにした。

![matrix_shift](https://user-images.githubusercontent.com/84301337/139531506-93b5b24b-f1b0-4071-8fee-1d0d63909919.jpg)

これは BIOMT1 から BIOMT3 までが一つのセットになっており、青枠で囲った部分が回転行列で、黄色の枠で囲った部分が並進ベクトルである。
緑色の枠は、回転行列の部分は単位行列、並進ベクトル部は零ベクトルとなっている。すなわち、このPDBファイルに記載されている単位構造そのものを表している。

この回転行列と並進ベクトルを元の座標に作用させることにより、対称操作した後の座標が得られる。

つまり、元の座標を ![CodeCogsEqn](https://user-images.githubusercontent.com/84301337/139536358-9cfc096e-b0b1-4bf8-9ae4-e865a07b445d.gif)
、回転行列を ![CodeCogsEqn (1)](https://user-images.githubusercontent.com/84301337/139536218-1cd44639-d8a3-49cd-affe-e29d141ceb8b.gif)、並進ベクトルを ![CodeCogsEqn (2)](https://user-images.githubusercontent.com/84301337/139536293-a3f57a2c-ef29-4b95-a9fd-ae94061ddf26.gif) とすると、対称操作した後の座標 ![CodeCogsEqn (3)](https://user-images.githubusercontent.com/84301337/139536325-4c369b03-cb1a-47a0-8f7f-ad710679432f.gif)
は、次のように表すことができる。

![CodeCogsEqn (4)](https://user-images.githubusercontent.com/84301337/139536374-a09c3836-ec77-4425-aff9-54d224926cbc.gif)

原子1つ1つに、対称操作の数だけ作用させる。

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
