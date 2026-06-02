from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parent
OUTDIR = BASE / "results" / "figures" / "tik5_report"
OUTDIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "figure.dpi": 150,
})

COL = {
    "blue": "#2F5D8C",
    "green": "#2F7D62",
    "orange": "#C26A2E",
    "red": "#B94A48",
    "gray": "#5D6670",
    "light_blue": "#DDEAF6",
    "light_green": "#DFF0E8",
    "light_orange": "#F6E5D7",
    "light_gray": "#EEF1F4",
    "dark": "#1F2933",
}


def save(fig, name):
    path = OUTDIR / name
    fig.savefig(path, bbox_inches="tight", dpi=220)
    plt.close(fig)


def add_box(ax, xy, w, h, text, fc, ec=None, fontsize=10):
    box = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.025",
        linewidth=1.2,
        edgecolor=ec or COL["gray"],
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + w / 2,
        xy[1] + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=COL["dark"],
        wrap=True,
    )


def arrow(ax, start, end, color=None, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=color or COL["gray"],
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def flow_figure(title, boxes, arrows, name, size=(11, 6)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(title, pad=12, weight="bold")
    centers = {}
    for key, x, y, w, h, text, fc in boxes:
        add_box(ax, (x, y), w, h, text, fc)
        centers[key] = (x + w / 2, y + h / 2, x, y, w, h)
    for s, e in arrows:
        sx, sy, sx0, sy0, sw, sh = centers[s]
        ex, ey, ex0, ey0, ew, eh = centers[e]
        start = (sx0 + sw, sy) if ex > sx else (sx0, sy)
        end = (ex0, ey) if ex > sx else (ex0 + ew, ey)
        if abs(ex - sx) < 0.05:
            start = (sx, sy0)
            end = (ex, ey0 + eh)
        arrow(ax, start, end)
    save(fig, name)


def make_flowcharts():
    flow_figure(
        "Ters ML Destekli Optimizasyon ve MPC Genel Sistem Yapısı",
        [
            ("syngas", .04, .58, .18, .18, "Singaz ölçümü\nH2, CO, CO2, CH4, H2O", COL["light_blue"]),
            ("inverse", .29, .58, .18, .18, "Ters ML\nsoft-sensor", COL["light_green"]),
            ("biooil", .54, .58, .18, .18, "Tahmin edilen\nbiyoyağ kompozisyonu", COL["light_orange"]),
            ("opt", .79, .58, .18, .18, "Optimizasyon /\nMPC karar bloğu", COL["light_gray"]),
            ("forward", .54, .24, .18, .18, "İleri surrogate\nmodel", COL["light_blue"]),
            ("control", .79, .24, .18, .18, "Yeni T, P, S/C\nkoşulları", COL["light_green"]),
        ],
        [("syngas", "inverse"), ("inverse", "biooil"), ("biooil", "opt"), ("biooil", "forward"), ("forward", "opt"), ("opt", "control")],
        "tik5_figure_b01_system_architecture.png",
    )

    flow_figure(
        "Önceki Dönemden Bu Döneme Geçiş Akışı",
        [
            ("prevdata", .05, .60, .20, .18, "TİK-4\nCantera veri seti", COL["light_blue"]),
            ("prevmlp", .32, .60, .20, .18, "Ters MLP modeli\nR2=0.863", COL["light_green"]),
            ("soft", .59, .60, .20, .18, "Soft-sensor\narayüzü", COL["light_orange"]),
            ("mpc", .76, .26, .20, .18, "TİK-5\noptimizasyon ve MPC", COL["light_gray"]),
            ("valid", .32, .26, .20, .18, "BiooilID bazlı\nvalidasyon", COL["light_blue"]),
            ("sur", .59, .26, .20, .18, "İleri surrogate\nmodel", COL["light_green"]),
        ],
        [("prevdata", "prevmlp"), ("prevmlp", "soft"), ("soft", "mpc"), ("prevmlp", "valid"), ("valid", "sur"), ("sur", "mpc")],
        "tik5_figure_b02_transition_flow.png",
    )

    flow_figure(
        "Ters ML Soft-Sensor Çalışma Akışı",
        [
            ("cond", .04, .60, .18, .18, "Proses koşulları\nT, P, S/C", COL["light_gray"]),
            ("gas", .04, .28, .18, .18, "Singaz bileşimi\nH2, CO, CO2, CH4, H2O", COL["light_blue"]),
            ("scale", .30, .44, .18, .18, "Ölçeklendirme\nve giriş matrisi", COL["light_orange"]),
            ("mlp", .56, .44, .18, .18, "Standart MLP\nters model", COL["light_green"]),
            ("post", .79, .44, .18, .18, "Fiziksel sınır\nve normalizasyon", COL["light_gray"]),
            ("out", .79, .12, .18, .18, "Biyoyağ\nkompozisyon tahmini", COL["light_green"]),
        ],
        [("cond", "scale"), ("gas", "scale"), ("scale", "mlp"), ("mlp", "post"), ("post", "out")],
        "tik5_figure_b03_soft_sensor_workflow.png",
    )

    flow_figure(
        "Soft-Sensor Çıktısının Optimizasyon ve MPC Bloğuna Aktarılması",
        [
            ("meas", .04, .55, .18, .18, "Ölçüm / simülasyon\nverisi", COL["light_blue"]),
            ("soft", .29, .55, .18, .18, "Soft-sensor\nbiyoyağ tahmini", COL["light_green"]),
            ("state", .54, .55, .18, .18, "Durum bilgisi\nkompozisyon", COL["light_orange"]),
            ("opt", .79, .55, .18, .18, "Optimizasyon\nT, P, S/C seçimi", COL["light_gray"]),
            ("plant", .79, .22, .18, .18, "Reformer\nuygulanan koşul", COL["light_blue"]),
            ("feedback", .29, .22, .18, .18, "Yeni singaz\ngeri besleme", COL["light_green"]),
        ],
        [("meas", "soft"), ("soft", "state"), ("state", "opt"), ("opt", "plant"), ("plant", "feedback"), ("feedback", "soft")],
        "tik5_figure_b04_soft_sensor_to_mpc.png",
    )

    flow_figure(
        "İleri Surrogate Modelin Giriş-Çıkış Yapısı",
        [
            ("bio", .05, .58, .22, .20, "Biyoyağ kompozisyonu\n6 bileşen grubu", COL["light_green"]),
            ("ctrl", .05, .24, .22, .20, "Kontrol değişkenleri\nT, P, S/C", COL["light_orange"]),
            ("model", .39, .41, .22, .20, "İleri surrogate\nçok çıkışlı regresyon", COL["light_blue"]),
            ("out", .73, .41, .22, .20, "Sentez gazı çıktıları\nH2, CO, CO2, CH4, H2O, H2/CO", COL["light_gray"]),
        ],
        [("bio", "model"), ("ctrl", "model"), ("model", "out")],
        "tik5_figure_b07_forward_surrogate_io.png",
    )

    flow_figure(
        "Optimizasyon Probleminin Blok Gösterimi",
        [
            ("bio", .04, .55, .18, .18, "Biyoyağ\nkompozisyonu", COL["light_green"]),
            ("cand", .29, .55, .18, .18, "Aday kontrol\nT, P, S/C", COL["light_orange"]),
            ("sur", .54, .55, .18, .18, "İleri surrogate\nmodel", COL["light_blue"]),
            ("obj", .79, .55, .18, .18, "Amaç fonksiyonu\nH2/CO + maliyet", COL["light_gray"]),
            ("select", .79, .22, .18, .18, "En iyi koşul\nseçimi", COL["light_green"]),
            ("grid", .29, .22, .18, .18, "Izgara tabanlı\naday tarama", COL["light_gray"]),
        ],
        [("bio", "sur"), ("cand", "sur"), ("sur", "obj"), ("obj", "select"), ("grid", "cand")],
        "tik5_figure_b09_optimization_problem.png",
    )

    flow_figure(
        "MPC Kapalı Çevrim Çalışma Döngüsü",
        [
            ("plant", .05, .57, .18, .18, "Reformer\nprosesi", COL["light_blue"]),
            ("meas", .30, .57, .18, .18, "Singaz ölçümü\nH2/CO", COL["light_gray"]),
            ("soft", .55, .57, .18, .18, "Soft-sensor\nbiyoyağ tahmini", COL["light_green"]),
            ("opt", .80, .57, .18, .18, "MPC optimizasyon\nT, P, S/C", COL["light_orange"]),
            ("apply", .80, .22, .18, .18, "İlk kontrol\nhareketi uygulanır", COL["light_blue"]),
        ],
        [("plant", "meas"), ("meas", "soft"), ("soft", "opt"), ("opt", "apply"), ("apply", "plant")],
        "tik5_figure_b11_mpc_closed_loop.png",
    )

    flow_figure(
        "TİK-5 Dönemi Nihai Sistem Özeti",
        [
            ("rev", .05, .58, .18, .18, "Ters ML\nsoft-sensor", COL["light_green"]),
            ("val", .29, .58, .18, .18, "BiooilID\nvalidasyonu", COL["light_orange"]),
            ("sur", .53, .58, .18, .18, "İleri surrogate\nmodel", COL["light_blue"]),
            ("stat", .77, .58, .18, .18, "Statik\noptimizasyon", COL["light_gray"]),
            ("mpc", .77, .24, .18, .18, "MPC ve\nbozucu etki", COL["light_green"]),
            ("next", .53, .24, .18, .18, "Sonraki dönem\nbelirsizlik ve deneysel doğrulama", COL["light_orange"]),
        ],
        [("rev", "val"), ("val", "sur"), ("sur", "stat"), ("stat", "mpc"), ("mpc", "next")],
        "tik5_figure_b13_final_system_summary.png",
    )


def make_split_comparison():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_title("Satır Bazlı Test ile BiooilID Bazlı Test Yaklaşımının Karşılaştırılması", weight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(2.4, 5.4, "Satır bazlı ayrım", ha="center", fontsize=12, weight="bold")
    for i in range(5):
        add_box(ax, (.45 + i * .75, 3.8), .55, .45, f"ID{i + 1}", COL["light_blue"], fontsize=8)
        add_box(ax, (.45 + i * .75, 2.9), .55, .45, f"ID{i + 1}", COL["light_green"], fontsize=8)
    ax.text(2.35, 4.45, "Eğitim kümesi", ha="center")
    ax.text(2.35, 2.55, "Test kümesi", ha="center")
    ax.text(2.35, 1.55, "Aynı BiooilID farklı koşullarla\nher iki kümede de bulunabilir", ha="center", fontsize=9)
    ax.text(7.35, 5.4, "BiooilID bazlı ayrım", ha="center", fontsize=12, weight="bold")
    for i in range(4):
        add_box(ax, (5.45 + i * .75, 3.8), .55, .45, f"ID{i + 1}", COL["light_blue"], fontsize=8)
    for i in range(2):
        add_box(ax, (6.20 + i * .75, 2.9), .55, .45, f"ID{i + 5}", COL["light_orange"], fontsize=8)
    ax.text(6.95, 4.45, "Eğitim kümesi", ha="center")
    ax.text(6.95, 2.55, "Test kümesi", ha="center")
    ax.text(6.95, 1.55, "Test BiooilID değerleri eğitimde\nhiç görülmez", ha="center", fontsize=9)
    ax.plot([5, 5], [.8, 5.6], color=COL["gray"], lw=1)
    save(fig, "tik5_figure_b05_split_comparison.png")


def make_metric_figures():
    bio = json.loads((BASE / "results" / "metrics" / "biooil_id_holdout_metrics.json").read_text(encoding="utf-8"))
    comp = bio["components"]
    keys = list(comp.keys())
    labels = ["Aromatikler", "Asitler", "Alkoller", "Furanlar", "Fenoller", "Aldehit-ketonlar"]
    r2 = [comp[k]["R2"] for k in keys]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = [COL["green"] if value >= 0 else COL["red"] for value in r2]
    ax.bar(labels, r2, color=colors)
    ax.axhline(0, color=COL["dark"], lw=1)
    ax.set_ylabel("R2")
    ax.set_title("BiooilID Bazlı Validasyonda Bileşen Bazlı R2 Değerleri", weight="bold")
    ax.tick_params(axis="x", rotation=20)
    for i, value in enumerate(r2):
        ax.text(i, value + (.15 if value >= 0 else -.45), f"{value:.3f}", ha="center", va="bottom" if value >= 0 else "top", fontsize=9)
    ax.set_ylim(min(r2) - .8, 1.2)
    ax.grid(axis="y", alpha=.25)
    save(fig, "tik5_figure_b06_biooilid_r2.png")

    fwd = json.loads((BASE / "results" / "metrics" / "forward_surrogate_metrics.json").read_text(encoding="utf-8"))
    metric_keys = [key for key in fwd if key != "average"]
    labels2 = ["H2", "CO", "CO2", "CH4", "H2O", "H2/CO"]
    r2s = [fwd[k]["R2"] for k in metric_keys]
    maes = [fwd[k]["MAE"] for k in metric_keys]
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(labels2))
    ax1.bar(x - .18, r2s, width=.36, color=COL["blue"], label="R2")
    ax1.set_ylim(.95, 1.005)
    ax1.set_ylabel("R2")
    ax2 = ax1.twinx()
    ax2.bar(x + .18, maes, width=.36, color=COL["orange"], label="MAE")
    ax2.set_ylabel("MAE")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels2)
    ax1.set_title("İleri Surrogate Model Performans Özeti", weight="bold")
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels_extra = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels_extra, loc="upper left")
    ax1.grid(axis="y", alpha=.25)
    save(fig, "tik5_figure_b08_forward_surrogate_metrics.png")


def make_case_study_figures():
    static = pd.read_csv(BASE / "results" / "tables" / "static_optimization_cases.csv")
    case_labels = static["case"].map({"aromatic_rich": "Aromatik", "acid_rich": "Asit", "balanced": "Dengeli"}) + "\nHedef " + static["target_h2_co"].astype(str)
    fig, ax = plt.subplots(figsize=(11, 5.8))
    x = np.arange(len(static))
    w = .36
    ax.bar(x - w / 2, static["baseline_H2_CO_Ratio"], width=w, label="Başlangıç", color=COL["gray"])
    ax.bar(x + w / 2, static["H2_CO_Ratio"], width=w, label="Optimize", color=COL["green"])
    for i, target in enumerate(static["target_h2_co"]):
        ax.hlines(target, i - .45, i + .45, color=COL["red"], linestyles="--", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels(case_labels)
    ax.set_ylabel("H2/CO oranı")
    ax.set_title("Statik Optimizasyon Senaryolarında Başlangıç ve Optimize Edilmiş H2/CO Oranları", weight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=.25)
    save(fig, "tik5_figure_b10_static_optimization_h2co.png")

    mpc = pd.read_csv(BASE / "results" / "tables" / "mpc_case_study.csv")
    fig, axes = plt.subplots(4, 1, figsize=(10.5, 9), sharex=True)
    steps = mpc["step"]
    axes[0].plot(steps, mpc["measured_H2_CO_Ratio"], marker="o", color=COL["blue"], label="Ölçülen H2/CO")
    axes[0].plot(steps, mpc["next_predicted_H2_CO_Ratio"], marker="s", color=COL["orange"], label="Sonraki tahmin")
    axes[0].axhline(2.0, color=COL["red"], linestyle="--", label="Hedef")
    axes[0].set_ylabel("H2/CO")
    axes[0].legend(loc="upper right", ncol=3, fontsize=8)
    axes[0].grid(alpha=.25)
    axes[1].plot(steps, mpc["applied_Reformer_Temperature_C"], marker="o", color=COL["red"])
    axes[1].set_ylabel("T (°C)")
    axes[1].grid(alpha=.25)
    axes[2].plot(steps, mpc["applied_Reformer_Pressure_bar"], marker="o", color=COL["green"])
    axes[2].set_ylabel("P (bar)")
    axes[2].grid(alpha=.25)
    axes[3].plot(steps, mpc["applied_Steam_to_Carbon_Ratio"], marker="o", color=COL["gray"])
    axes[3].set_ylabel("S/C")
    axes[3].set_xlabel("Zaman adımı")
    axes[3].grid(alpha=.25)
    for ax in axes:
        ax.axvline(5, color=COL["orange"], linestyle=":", lw=1.5)
    axes[0].text(5.08, 2.35, "Bozucu etki", color=COL["orange"], fontsize=9)
    fig.suptitle("MPC Zaman Serisi, H2/CO Oranı ve Kontrol Değişkenleri", weight="bold", y=.995)
    save(fig, "tik5_figure_b12_mpc_timeseries.png")


def main():
    make_flowcharts()
    make_split_comparison()
    make_metric_figures()
    make_case_study_figures()
    for path in sorted(OUTDIR.glob("tik5_figure_b*.png")):
        print(path)


if __name__ == "__main__":
    main()
