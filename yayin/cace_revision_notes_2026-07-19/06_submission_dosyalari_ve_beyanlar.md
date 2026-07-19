# Submission Dosyaları ve Beyanlar

Bu dosya C&CE gönderimi için hazırlanması gereken dosyaları ve taslak beyan metinlerini listeler. Author bilgileri, funding ve data repository DOI/URL kullanıcı tarafından kesinleştirilmeli.

## C&CE yükleme dosyaları

- `Manuscript.docx`: ana makale, single-column Word formatında.
- `Title_page.docx`: başlık, yazarlar, kurumlar, corresponding author bilgisi.
- `Highlights.docx`: 3-5 madde, her madde en fazla 85 karakter.
- `Figure_captions.docx`: tüm şekil altyazıları.
- `Figure_1.png`, `Figure_2.png`, ...: her şekil ayrı dosya.
- `Table` içerikleri: ana makale içinde editable text olarak veya ayrı editable dosya.
- `Graphical_abstract`: C&CE için teşvik ediliyor, zorunlu değil; AI-generated olmamalı.
- `Supplementary_material.docx` veya `.xlsx`: veri temizleme, ek metrikler, BiooilID holdout ayrıntıları.
- `Declaration_of_interest.docx`: Elsevier declaration tool çıktısı veya metin.
- `Cover_letter.docx`: editöre kısa kapak yazısı.

## Title page için doldurulacak alanlar

- Article title:
- Author names and order:
- Affiliations:
- Corresponding author:
- E-mail:
- Full postal address:
- Phone:
- Present/permanent address, varsa:

## Data availability taslakları

Seçenek A, veri deposu açılırsa:

> Data associated with this study, including the cleaned Cantera-derived reforming dataset, model-ready bio-oil composition table, metric files, and selected scripts, are available at [repository name] under DOI/URL: [insert DOI/URL].

Seçenek B, veri şu an yalnızca yerel depoda kalacaksa:

> The data that support the findings of this study are available from the corresponding author upon reasonable request. A curated dataset and the main scripts are being prepared for repository deposition.

C&CE veri beyanı istediği için bu bölüm boş bırakılmamalı.

## Declaration of competing interest taslağı

> The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Funding taslakları

Fon yoksa:

> This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

Fon varsa:

> This work was supported by [funder name] [grant number]. The funder had no role in study design, data collection, analysis, interpretation, manuscript preparation, or the decision to submit the article for publication.

## CRediT author statement taslağı

Bu alan yazar listesine göre güncellenmeli.

> Orhun Uzdiyem: Conceptualization, Data curation, Methodology, Software, Formal analysis, Investigation, Validation, Visualization, Writing - original draft.

> [Co-author name]: Supervision, Methodology, Project administration, Writing - review and editing.

> [Co-author name]: Supervision, Resources, Writing - review and editing.

## Generative AI beyanı

Eğer AI araçları yalnızca taslak düzenleme, dil iyileştirme veya submission notlarını organize etmek için kullanıldıysa:

> During the preparation of this work, the authors used AI-assisted tools to organize draft notes, improve readability, and prepare submission-support material. After using these tools, the authors reviewed, verified, and edited the content and take full responsibility for the content of the published article.

Eğer yalnızca temel yazım-denetim araçları kullanıldıysa C&CE/Elsevier yönergesine göre beyan gerekmeyebilir; ancak bu karar gönderim öncesi netleştirilmeli.

Önemli: Elsevier, submitted manuscript içindeki şekil ve graphical abstract üretiminde generative AI kullanımına izin vermiyor. Şekiller proje verilerinden ve manuel çizimlerden gelmeli.

## Cover letter için kısa iskelet

Dear Editor,

We submit the manuscript entitled "[title]" for consideration as a full-length article in Computers & Chemical Engineering. The manuscript presents a Cantera-assisted inverse machine-learning workflow for estimating six-class bio-oil composition from steam reforming syngas and operating conditions. The work is aligned with the journal's scope in modeling, simulation, intelligent systems, process monitoring, and chemical engineering applications.

The main contribution is the formulation and evaluation of a simulation-domain inverse soft sensor for bio-oil steam reforming. The study compares classical machine-learning, deep-learning, constrained-output, and ensemble models, and explicitly distinguishes row-wise interpolation performance from BiooilID-based generalization limits.

The manuscript has not been published previously and is not under consideration elsewhere. All authors have approved the submission.

Sincerely,

[Corresponding author name]

