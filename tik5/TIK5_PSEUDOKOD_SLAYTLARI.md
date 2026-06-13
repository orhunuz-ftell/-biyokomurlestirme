# TİK-5: Teknik Pseudokod Sunum Taslağı

## Slayt 1 — Genel Akış
```text
for each scenario in [static_cases, mpc_case]:
    yükle ölçüm/proses verisi
    biooil_hat = reverse_ml.predict(T,P,S/C,H2,CO,CO2,CH4,H2O)
    x = filter_and_normalize(biooil_hat)
    çöz = solve_optimization(x, T,P,S/C bounds)
    kaydet(çöz, metrikler, senaryo)
```

## Slayt 2 — 1) Veri ve Özellik Hazırlığı
```text
X_raw <- okuyucu(simülasyon + deney logları + önceki sonuçlar)
X_clean <- replace_nan(X_raw), remove_outliers(X_raw), unit_harmonize(X_clean)
X_proc <- scale/minmax_features(X_clean, selected_cols)
y_proc <- select_cols([T,P,S/C,H2,CO,CO2,CH4,H2O])
save_schema(X_proc, y_proc, feature_order)
```

## Slayt 3 — 2) Ters ML Soft-Sensor Bloğu
```text
def reverse_predict(T,P,S/C,H2,CO,CO2,CH4,H2O):
    x <- vectorize(y_proc, order=feature_order)
    y_hat <- model_rev.predict(x)
    return clip_components(y_hat, biooil_lower, biooil_upper)
biooil_hat <- reverse_predict(...)
```

## Slayt 4 — 3) Fiziksel Filtre + Normalizasyon
```text
biooil_hat = clip(biooil_hat, min=0, max=100)          # kütle yüzdesi sınırı
biooil_sum = sum(biooil_hat)
biooil_hat = biooil_hat / biooil_sum * 100               # kütle dengesi düzeltmesi
biooil_norm = (biooil_hat - mu) / sigma                  # optimizasyon girdisi ölçekleme
```

## Slayt 5 — 4) İleri Vekil Model
```text
def forward_surrogate(u_T,u_P,u_SC,biooil_norm):
    x_adv <- concat(u_T,u_P,u_SC,biooil_norm)
    y_sim <- model_adv.predict(x_adv)
    return dict(H2=y_sim[0], CO=y_sim[1], CO2=y_sim[2],
                CH4=y_sim[3], H2O=y_sim[4], H2CO=y_sim[5])
y_hat = forward_surrogate(...)
```

## Slayt 6 — 5) Optimizasyon ve Çözücü
```text
J = |y_hat.H2CO - target| + λ1*norm(u_T) + λ2*norm(u_P) + λ3*norm(u_SC)
konstraints: 650<=T<=850, 5<=P<=30, 2<=S/C<=6
u_opt = scipy.optimize.minimize(J(T,P,S/C), method="SLSQP", bounds=konstraints)
u* = u_opt.x ; save(u*, J(u*))
```

## Slayt 7 — 6) Statik Case-Study Akışı
```text
for each biooil_id in [66,70,60]:
    for target in [2.0,2.5]:
        biooil0 = dataset[biooil_id]
        biooil_n = normalize(biooil0)
        result_static <- optimize(biooil_n, target)
        raporla(result_static, T,P,S/C,H2CO,ceza)
```

## Slayt 8 — 7) MÖK-benzeri Kapalı Çevrim + Bozucu Etki
```text
state <- init_case(biooil_balanced, u_init=[750,15,4])
for k in 1..10:
    y_meas <- propagate_gas(state) or use_sim_sample(k)
    if k==5: y_meas <- apply_disturbance(y_meas)   # bozucu etki
    biooil_hat <- reverse_predict(y_meas)
    u_k <- optimize( filter_and_normalize(biooil_hat), target=2.5 )
    state <- apply_control(state,u_k); log(k,u_k,y_meas,y_target)
```
