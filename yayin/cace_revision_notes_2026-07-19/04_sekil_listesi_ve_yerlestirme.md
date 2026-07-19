# Şekil Listesi ve Yerleştirme Planı

Mevcut `taslak_en.docx` içinde 11 şekil başlığı var; ancak DOCX paketinde yalnızca 1 gömülü görsel tespit edildi. Aşağıdaki şekiller proje genelinde bulundu. Şekilleri Word'e sen elle yapıştıracağın için bu dosya yerleştirme listesi olarak hazırlandı.

## Ana makale için önerilen minimum şekil seti

Bu 6 şekil C&CE için daha güçlü ve daha odaklı bir ana makale verir. Diğer şekiller supplementary olabilir.

| Önerilen no | Önerilen başlık | Kullanılacak dosya | Neden gerekli |
|---|---|---|---|
| Figure 1 | Overall inverse soft-sensor workflow | `C:\@biyokomurlestirme\diagram-1-ana-sistem.png` veya `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b03_soft_sensor_workflow.png` | Makalenin ana fikrini gösterir |
| Figure 2 | Cantera-based steam reforming data generation | `C:\@biyokomurlestirme\diagram-2-cantera-simulasyon.png` | Simülasyon veri üretimini açıklar |
| Figure 3 | Surrogate reforming process and hydrogen production stages | `C:\@biyokomurlestirme\diagram-8-hidrojen-uretim-prosesi.png` | Kimya mühendisliği proses bağlamını verir |
| Figure 4 | MLP architecture for inverse bio-oil composition prediction | `C:\@biyokomurlestirme\diagram-3-mlp-mimarisi.png` | Model yapısını gösterir |
| Figure 5 | Model comparison and ensemble behavior | `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\model_comparison_r2.png` veya `C:\@biyokomurlestirme\diagram-6-performans-ensemble.png` | Ana performans sonucunu gösterir |
| Figure 6 | Generalization audit with BiooilID holdout | `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b05_split_comparison.png` ve/veya `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b06_biooilid_r2.png` | Reviewer'ın data leakage sorusunu karşılar |

## Mevcut TİK4/taslak figür başlıkları ve bulunan olası dosyalar

| Taslaktaki başlık | Bulunan olası dosya | Durum |
|---|---|---|
| Figure 1. Methodology flowchart. | `C:\@biyokomurlestirme\diagram-1-ana-sistem.png` | Kullanılabilir |
| Figure 2. Data generation with Cantera. | `C:\@biyokomurlestirme\diagram-2-cantera-simulasyon.png` | Kullanılabilir |
| Figure 3. Schematic view of the hydrogen production process stages. | `C:\@biyokomurlestirme\diagram-8-hidrojen-uretim-prosesi.png` | Kullanılabilir |
| Figure 4. Cantera simulation process. | Net ayrı dosya bulunamadı; `diagram-2-cantera-simulasyon.png` ile birleştirilebilir | Eksik/tekrar olabilir |
| Figure 5. Data preparation. | `C:\@biyokomurlestirme\diagram-4-egitim-sureci.png` olabilir | Başlık-dosya uyumu kontrol edilmeli |
| Figure 6. MLP model architecture. | `C:\@biyokomurlestirme\diagram-3-mlp-mimarisi.png` | Kullanılabilir |
| Figure 7. Model training results. | Net ayrı dosya bulunamadı; metrik grafikleri kullanılabilir | Eksik |
| Figure 8. Feature importance analysis results. | `C:\@biyokomurlestirme\diagram-7-ozellik-onemi.png` veya `...\output\figures\feature_importance.png` | Kullanılabilir |
| Figure 9. Model performance and ensemble comparison. | `C:\@biyokomurlestirme\diagram-6-performans-ensemble.png` veya `...\output\figures\model_comparison_r2.png` | Kullanılabilir |
| Figure 10. Summary workflow of the inverse prediction method. | `C:\@biyokomurlestirme\diagram-5-ters-tahmin.png` | Kullanılabilir |
| Figure 11. Inverse prediction usage flow and summary of results obtained with standard MLP. | Net birebir dosya bulunamadı; `diagram-5` veya TİK5 final summary ile değiştirilebilir | Eksik/yeniden çizilmeli |

## Kök dizinde bulunan TİK4 ile ilişkili şekiller

| Dosya | Boyut | Önerilen kullanım |
|---|---:|---|
| `C:\@biyokomurlestirme\diagram-1-ana-sistem.png` | 2048 x 3052 | Ana metodoloji / soft-sensor iş akışı |
| `C:\@biyokomurlestirme\diagram-2-cantera-simulasyon.png` | 2048 x 2578 | Cantera simülasyon veri üretimi |
| `C:\@biyokomurlestirme\diagram-3-mlp-mimarisi.png` | 2048 x 2064 | MLP mimarisi |
| `C:\@biyokomurlestirme\diagram-4-egitim-sureci.png` | 2048 x 3246 | Eğitim/veri hazırlama süreci |
| `C:\@biyokomurlestirme\diagram-5-ters-tahmin.png` | 2048 x 2064 | Ters tahmin akışı |
| `C:\@biyokomurlestirme\diagram-6-performans-ensemble.png` | 2048 x 2064 | Ensemble/model performans karşılaştırması |
| `C:\@biyokomurlestirme\diagram-7-ozellik-onemi.png` | 2048 x 2064 | Özellik önemi |
| `C:\@biyokomurlestirme\diagram-8-hidrojen-uretim-prosesi.png` | 2048 x 2948 | Hidrojen üretim prosesi |

## ML çıktı klasöründe bulunan daha yayınlık grafikler

Bu dosyalar TİK çizimlerinden daha yüksek çözünürlüklü ve sonuç figürü olarak daha uygun olabilir.

| Dosya | Boyut | Önerilen kullanım |
|---|---:|---|
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\correlation_matrix.png` | 2913 x 2366 | Supplementary veya feature discussion |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\feature_importance.png` | 2971 x 1760 | Ana makale Figure 5/6 adayı |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\feature_importance_heatmap.png` | 3346 x 1765 | Supplementary |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\model_comparison_avg_metrics.png` | 4471 x 1481 | Ana model karşılaştırması |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\model_comparison_r2.png` | 4170 x 2065 | Ana model karşılaştırması |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\predicted_vs_actual_random_forest.png` | 4468 x 2998 | RF özel olduğu için ana makalede düşük öncelik |
| `C:\@biyokomurlestirme\reverse_ml_biooil_to_product\ml_reverse_prediction\output\figures\residuals_random_forest.png` | 4471 x 2998 | Supplementary |

## TİK5 şekilleri: genelleme, soft-sensor ve MPC için adaylar

| Dosya | Boyut | Önerilen kullanım |
|---|---:|---|
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b01_system_architecture.png` | 1919 x 1128 | Geniş sistem mimarisi |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b02_transition_flow.png` | 1919 x 1134 | TİK4'ten TİK5'e geçiş; makalede düşük öncelik |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b03_soft_sensor_workflow.png` | 1919 x 1128 | Ana workflow için güçlü aday |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b04_soft_sensor_to_mpc.png` | 1919 x 1129 | MPC bağlantısı anlatılacaksa kullanılabilir |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b05_split_comparison.png` | 1748 x 1025 | Row-wise vs BiooilID split tartışması için gerekli |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b06_biooilid_r2.png` | 1856 x 1157 | BiooilID holdout performansı için gerekli |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b07_forward_surrogate_io.png` | 1919 x 1135 | İleri surrogate eklenirse kullanılabilir |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b08_forward_surrogate_metrics.png` | 2009 x 1082 | İleri surrogate sonuçları; bu makalenin kapsamı genişletilirse |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b09_optimization_problem.png` | 1919 x 1129 | Optimizasyon/MPC makalesine daha uygun |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b10_static_optimization_h2co.png` | 2001 x 1159 | Optimizasyon sonucu; C&CE için ikinci makale adayı olabilir |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b11_mpc_closed_loop.png` | 1919 x 1129 | Kontrol/MPC vurgusu yapılırsa |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b12_mpc_timeseries.png` | 1964 x 1887 | MPC sonuç figürü; mevcut ters ML makalesinde supplementary olabilir |
| `C:\@biyokomurlestirme\tik5\figures\tik5_figure_b13_final_system_summary.png` | 1919 x 1128 | Graphical abstract veya final workflow adayı |

## Şekil hazırlama notları

- C&CE görsellerin ayrı dosya olarak yüklenmesini istiyor.
- Dosya adlarını `Figure_1.png`, `Figure_2.png` gibi yeniden adlandır.
- Üçüncü taraf veya AI-generated görsel kullanma; proje verilerinden üretilmiş grafik/diagram kullan.
- Görsel içindeki yazıların İngilizce olduğundan emin ol.
- Çizimlerde renk körlüğü erişilebilirliği için kırmızı-yeşil ayrımına dikkat et.
- Şekil altyazıları ayrı bir `figure_captions` dosyasında da bulunmalı.

