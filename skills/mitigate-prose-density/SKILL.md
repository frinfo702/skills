---
name: mitigate-prose-density
description: Control information density when writing Japanese prose documents — lead with a short abstract summary, put each paragraph's point in its first sentence, use ## headings sparingly as nouns, and avoid label-prefixed sentences and parenthetical asides. Use whenever drafting, rewriting, or reviewing a document, report, README, research note, experiment write-up, or blog post, especially when the user says 「文章を書いて」「文書にまとめて」「レポートを書いて」「書き直して」「読みやすくして」, even if they don't mention density or style.
---

文書を書くときは、情報の密度を制御することを最優先にしてください。

文書の冒頭では、全体で何が言えるのかを抽象的に、短く書きます。読み手はそこだけで
全体の形をつかめるようにします。この冒頭に見出しは付けず、本文からそのまま始めます。
各段落の中でも同じで、最初の一文でその段落の言いたいことを述べ、続く文で根拠や具体を
足していきます。すべての文が同じ密度だと、読み手はどこが要点かを毎回自分で判断する
必要があり、書いた本人でさえ内容を追えなくなります。

見出しは ## を基本にします。### は、## の節が長く複雑で、区切らないと読めないときだけ
使います。見出しは「原因」「手法」のような名詞にし、「なぜ」のような口語にはしません。
すべてのまとまりに見出しを付ける必要はありません。自然な文章は、見出しなしで始まる
ことが多いです。

「結果: 〜」「**漏れで確定した。** 〜」のように、文の頭にラベルを付ける書き方は、
見出しを付けているのと同じなので避けます。言いたいことは文として書きます。

名前を付けることは大切です。式だけを示されるより、「これは微分と呼ばれる操作だ」と
言われる方が、人は意味を持って覚えられます。ただし、名前を持つのは普遍的な概念で
あって、文書の中の一つ一つのまとまりではありません。何にでも名前を付けられると
考えないでください。

括弧で情報を補足しないでください。括弧は密度を上げるわりに、読み手にはほとんど
役に立ちません。必要な情報なら文の中に書き、必要でなければ削ります。

悪い例:
## なぜ
- **漏れで確定した。** 表 11 で、条件 5 はどの集計でも .9 を大きく超える
  （実行前の「読み方」の 1 つ目）。

良い例:
## 原因
視点に依存する関係の結果は、関係を解いた結果ではなかった。注釈者のカメラは
正解の物体を注視していて、カメラの向きだけで正解がほぼ分かってしまう。実際、
文を読まずに注視点に最も近い候補を選ぶだけで、正解率は .995 になった。
